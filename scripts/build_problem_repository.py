#!/usr/bin/env python3
"""Build a deterministic, self-contained Web GPT problem repository snapshot."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from build_web_context_bundle import render_context
from vibe_mathing.web_channel import canonical_json_sha256, sha256_file

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / "governance/tasks/0027-web-gpt-github-chat-research-harness"
DEFAULT_MANIFEST = TASK / "harness-source-manifest.v1.json"
DEFAULT_TEMPLATE = TASK / "problem-repository-template"
BUILDER_VERSION = "1.2.3"
IDENTITY_EXCLUDES = {"HARNESS_SNAPSHOT.json", "HARNESS_SNAPSHOT_HISTORY.json", "WEB_BOOTSTRAP.md"}
MUTABLE_GENERATED = {
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
}
PRELOADED_RECORDS = {
    "research/records/attempts.jsonl": "attempts_file",
    "research/records/failed-routes.jsonl": "failed_routes_file",
    "research/records/obligation-graphs.jsonl": "obligation_graphs_file",
}
DEFAULT_CANONICAL_LEDGER = Path("problem-library/records/canonical-problems.jsonl")


def run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "command failed")
    return result.stdout.strip()


def safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value or not value:
        raise ValueError(f"unsafe manifest path: {value!r}")
    return Path(*path.parts)


def excluded(relative: Path, patterns: list[str]) -> bool:
    text = relative.as_posix()
    for pattern in patterns:
        if "/" in pattern and fnmatch.fnmatchcase(text, pattern):
            return True
        if any(fnmatch.fnmatchcase(part, pattern) for part in relative.parts):
            return True
    return False


def copy_regular(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise RuntimeError(f"Harness source must be a regular file: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    mode = 0o755 if source.stat().st_mode & 0o111 else 0o644
    os.chmod(temporary, mode)
    os.replace(temporary, target)


def validate_json(instance: Any, schema_path: Path, label: str) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        raise RuntimeError(f"{label} schema validation failed: {errors[0].message}")


def source_repository(root: Path) -> str:
    try:
        remote = run(["git", "remote", "get-url", "origin"], root)
    except RuntimeError:
        return "local/unbound"
    if remote.endswith(".git"):
        remote = remote[:-4]
    match = re.search(r"github\.com[/:]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)$", remote)
    return match.group(1) if match else "local/unbound"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    os.chmod(path, 0o644)


def filtered_jsonl(source: Path, problem_id: str) -> str:
    if not source.exists():
        return ""
    values: list[dict[str, Any]] = []
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise RuntimeError(f"expected object at {source}:{number}")
        if value.get("problem_id") == problem_id:
            values.append(value)
    return "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values)


def problem_is_admitted(problem: dict[str, Any], ledger_path: Path) -> bool:
    if not ledger_path.is_file():
        return False
    expected_id = problem.get("problem_id")
    expected_digest = canonical_json_sha256(problem)
    matches = 0
    for number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise RuntimeError(f"canonical ledger record must be an object: {ledger_path}:{number}")
        if value.get("problem_id") == expected_id:
            matches += 1
            if canonical_json_sha256(value) != expected_digest:
                raise RuntimeError(f"ProblemContract differs from canonical ledger: {expected_id}")
    if matches > 1:
        raise RuntimeError(f"duplicate canonical ProblemContract in ledger: {expected_id}")
    return matches == 1


def inventory_entry(root: Path, path: Path, layer: str, owner: str) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    mode = "0755" if path.stat().st_mode & 0o111 else "0644"
    return {
        "path": relative,
        "bytes": path.stat().st_size,
        "mode": mode,
        "sha256": sha256_file(path),
        "layer": layer,
        "owner": owner,
    }


def tree_digest(files: list[dict[str, Any]]) -> str:
    payload = [
        {key: item[key] for key in ("path", "bytes", "mode", "sha256", "layer", "owner")}
        for item in sorted(files, key=lambda item: item["path"])
    ]
    return canonical_json_sha256(payload)


def read_problem(path: Path, root: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise RuntimeError("Problem file is empty")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        lines = [line for line in raw.splitlines() if line.strip()]
        if len(lines) != 1:
            raise RuntimeError("Problem input must be one JSON object or one JSONL record")
        parsed = json.loads(lines[0])
    if isinstance(parsed, list):
        if len(parsed) != 1 or not isinstance(parsed[0], dict):
            raise RuntimeError("Problem JSON array must contain exactly one object")
        problem = parsed[0]
    else:
        problem = parsed
    if not isinstance(problem, dict):
        raise RuntimeError("Problem input must be an object")
    validate_json(problem, root / "problem-library/schema/canonical-problem.schema.json", "ProblemContract")
    return problem


def build(args: argparse.Namespace) -> dict[str, Any]:
    root = args.project_root.resolve()
    output = args.output.resolve()
    manifest_path = args.source_manifest.resolve()
    template = args.template.resolve()
    try:
        commit = run(["git", "rev-parse", "HEAD"], root)
        dirty = bool(run(["git", "status", "--porcelain"], root))
        built_at = run(["git", "show", "-s", "--format=%cI", "HEAD"], root)
    except RuntimeError:
        commit = "0" * 40
        dirty = True
        built_at = "1970-01-01T00:00:00Z"
    source_repo = source_repository(root)
    if dirty and not args.allow_dirty_source:
        raise RuntimeError("source worktree is dirty; production Harness snapshots require an immutable committed source")
    if source_repo == "local/unbound" and not args.allow_dirty_source:
        raise RuntimeError("source repository identity is unbound; production Harness snapshots require an exact GitHub source")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_json(manifest, TASK / "harness-source-manifest.v1.schema.json", "source manifest")
    problem = read_problem(args.problem_file.resolve(), root)
    if problem.get("lifecycle") != "active" and not args.allow_draft_problem:
        raise RuntimeError("ProblemContract is not active; production problem repositories require lifecycle=active")
    canonical_ledger = args.canonical_ledger.resolve() if args.canonical_ledger else root / DEFAULT_CANONICAL_LEDGER
    admitted = problem_is_admitted(problem, canonical_ledger)
    if not admitted and not args.allow_unadmitted_problem:
        raise RuntimeError("ProblemContract is not an exact record in the canonical ledger")
    problem_admission = "canonical_admitted" if admitted else "preview_unadmitted"
    if (args.repository_database_id is None) != (args.repository_node_id is None):
        raise RuntimeError("repository database ID and node ID must be supplied together")
    repository_binding = "verified" if args.repository_database_id is not None else "planned"
    if repository_binding != "verified" and not args.allow_planned_repository_identity:
        raise RuntimeError("repository identity is not verified; create/read the private repository before production build")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"output must not exist or must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    manifest_digest = sha256_file(manifest_path)
    file_policy: dict[str, tuple[str, str]] = {}

    excluded_skill_ids = {str(item) for item in manifest["excluded_container_skill_ids"]}
    required_exclusions = {"auto-goal", "auto-tmux", "nvidia-private-compute"}
    if not required_exclusions.issubset(excluded_skill_ids):
        raise RuntimeError("source manifest must exclude auto-goal, auto-tmux and nvidia-private-compute")
    global_excludes = [str(item) for item in manifest["global_excludes"]]
    for entry in manifest["entries"]:
        source = root / safe_relative(entry["source_path"])
        target_base = output / safe_relative(entry["target_path"])
        excludes = global_excludes + [str(item) for item in entry.get("excludes", [])]
        if excluded_skill_ids.intersection(safe_relative(entry["target_path"]).parts):
            raise RuntimeError(f"excluded container Skill target in source manifest: {entry['target_path']}")
        if entry["kind"] == "file":
            if not source.exists():
                if entry["required"]:
                    raise RuntimeError(f"required Harness source is missing: {source}")
                continue
            copy_regular(source, target_base)
            file_policy[target_base.relative_to(output).as_posix()] = (entry["layer"], entry["owner"])
        else:
            if not source.is_dir() or source.is_symlink():
                if entry["required"]:
                    raise RuntimeError(f"required Harness tree is missing or unsafe: {source}")
                continue
            copied = 0
            for candidate in sorted(source.rglob("*")):
                relative = candidate.relative_to(source)
                if excluded(relative, excludes):
                    continue
                if candidate.is_symlink():
                    raise RuntimeError(f"symlink in Harness source tree: {candidate}")
                if candidate.is_dir():
                    continue
                if not candidate.is_file():
                    raise RuntimeError(f"non-regular Harness source: {candidate}")
                target = target_base / relative
                if excluded_skill_ids.intersection(target.relative_to(output).parts):
                    raise RuntimeError(f"excluded container Skill in Harness source tree: {target.relative_to(output)}")
                copy_regular(candidate, target)
                file_policy[target.relative_to(output).as_posix()] = (entry["layer"], entry["owner"])
                copied += 1
            if entry["required"] and copied == 0:
                raise RuntimeError(f"required Harness tree copied no files: {source}")

    for candidate in sorted(template.rglob("*")):
        if candidate.is_dir():
            continue
        if candidate.is_symlink() or not candidate.is_file():
            raise RuntimeError(f"unsafe problem repository template member: {candidate}")
        relative = candidate.relative_to(template)
        if excluded_skill_ids.intersection(relative.parts):
            raise RuntimeError(f"excluded container Skill in problem repository template: {relative}")
        if relative.as_posix() == "WEB_BOOTSTRAP.md.in":
            continue
        target = output / relative
        if target.exists():
            raise RuntimeError(f"template target collides with Harness source: {relative}")
        copy_regular(candidate, target)
        file_policy[relative.as_posix()] = ("web_channel", "harness")

    canonical_path = output / "problem-library/records/canonical-problems.jsonl"
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_path.write_text(json.dumps(problem, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    file_policy[canonical_path.relative_to(output).as_posix()] = ("problem_instance", "problem")

    for relative in sorted(MUTABLE_GENERATED):
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        source_argument = PRELOADED_RECORDS.get(relative)
        if source_argument:
            configured = getattr(args, source_argument)
            source = configured.resolve() if configured else root / relative
            path.write_text(filtered_jsonl(source, problem["problem_id"]), encoding="utf-8")
        else:
            path.write_text("", encoding="utf-8")
        os.chmod(path, 0o644)
    for directory in (
        "research/artifacts/web-inbox",
        "research/artifacts/candidates",
        "research/artifacts/source-notes",
        "research/artifacts/receipts/web-import",
        "result-library/indexes",
    ):
        (output / directory).mkdir(parents=True, exist_ok=True)

    profile = json.loads((root / "governance/control-plane/web-research-channel.v1.json").read_text(encoding="utf-8"))
    write_json(output / "WEB_CHANNEL_PROFILE.json", profile)
    file_policy["WEB_CHANNEL_PROFILE.json"] = ("web_channel", "harness")

    web_status = {
        "vibe-mathing-router": "active",
        "math-discovery": "active",
        "math-derivation": "active",
        "math-proof": "active",
        "math-computation": "constrained",
        "math-formalization": "constrained",
        "solve": "active",
        "math-toolchain": "constrained",
    }
    skills: list[dict[str, Any]] = []
    for version_path in sorted((output / ".codex/skills").glob("*/VERSION")):
        skill_id = version_path.parent.name
        entry = version_path.parent / "SKILL.md"
        if not entry.is_file():
            raise RuntimeError(f"Skill has VERSION but no SKILL.md: {skill_id}")
        skills.append({
            "skill_id": skill_id,
            "version": version_path.read_text(encoding="utf-8").strip(),
            "entry": entry.relative_to(output).as_posix(),
            "entry_sha256": sha256_file(entry),
            "web_status": web_status.get(skill_id, "inactive"),
        })
    active = {"schema_version": "1.0.0", "skills": skills}
    write_json(output / "WEB_ACTIVE_SKILLS.json", active)
    file_policy["WEB_ACTIVE_SKILLS.json"] = ("web_channel", "harness")

    (output / "WEB_CONTEXT_BUNDLE.md").write_text(render_context(output), encoding="utf-8")
    os.chmod(output / "WEB_CONTEXT_BUNDLE.md", 0o644)

    output_contract = {
        "schema_version": "1.0.0",
        "channel": profile["channel_id"],
        "bootstrap_ack_schema": "research/schema/web-bootstrap-ack.schema.json",
        "attempt_packet_schema": "research/schema/web-attempt-packet.schema.json",
        "allowed_write_paths": profile["allowed_repository_write_paths"],
        "prohibited_write_paths": profile["prohibited_repository_write_paths"],
        "autonomy_policy": profile["autonomy_policy"],
        "repository_scope_policy": profile["repository_scope_policy"],
        "harness_maintenance_policy": {
            "branch_prefix": "maintenance/harness-",
            "trusted_actors": ["vibemathing"],
            "exact_regenerated_snapshot_delta_required": True,
            "mathematical_state_changes_allowed": False,
        },
        "state_freshness_policy": {
            "authoritative_state": "fresh_default_branch_and_live_github_objects",
            "historical_chat_is_authoritative": False,
            "design_time_revisions_may_advance": True,
            "audit_maturity_is_repository_admission": False,
            "round_end_is_permission_failure": False,
            "issue_identity_fields": ["problem_id", "attempt_id", "route_id", "obligation_id"],
            "issue_creation": "search_twice_then_create_or_reuse_unique",
        },
        "allowed_github_operations": [
            "issue_create", "candidate_branch_create", "candidate_file_create",
            "candidate_file_update", "candidate_file_delete", "commit_create",
            "pull_request_create", "pull_request_review", "actions_read",
            "actions_rerun_existing_candidate_run", "pull_request_merge", "checkpoint",
        ],
        "prohibited_github_operations": [
            "repository_create", "direct_default_branch_write", "force_push",
            "protected_ref_rewrite", "workflow_write", "actions_cancel", "actions_dispatch",
        ],
        "limits": {
            "max_packet_bytes": 262144,
            "max_files_per_pull_request": 64,
            "max_file_bytes": 1048576,
            "max_total_changed_bytes": 8388608,
        },
        "verdict": "candidate_only",
        "forbidden_claims": ["established", "refuted", "independent", "kernel_checked", "result_admitted"],
        "save_hidden_chain_of_thought": False,
    }
    write_json(output / "WEB_OUTPUT_CONTRACT.json", output_contract)
    file_policy["WEB_OUTPUT_CONTRACT.json"] = ("web_channel", "harness")

    builder_path = root / "scripts/build_problem_repository.py"

    listed_files: list[dict[str, Any]] = []
    for relative, (layer, owner) in sorted(file_policy.items()):
        if relative in IDENTITY_EXCLUDES or relative in MUTABLE_GENERATED:
            continue
        path = output / relative
        listed_files.append(inventory_entry(output, path, layer, owner))

    contract_digest = canonical_json_sha256(problem)
    snapshot = {
        "schema_version": "1.1.0",
        "snapshot_id": f"harness-snapshot:{problem['problem_id'].split(':', 1)[1]}",
        "harness_version": manifest["harness_version"],
        "profile": manifest["profile"],
        "repository": args.repository,
        "repository_identity": {
            "binding_state": repository_binding,
            "full_name": args.repository,
            "database_id": args.repository_database_id,
            "node_id": args.repository_node_id,
            "default_branch": args.default_branch,
            "visibility": args.visibility,
        },
        "source": {
            "repository": source_repo if args.visibility == "private" else "reviewed-public-export",
            "commit": commit if args.visibility == "private" else manifest_digest[:40],
            "worktree_dirty": dirty,
            "source_manifest_sha256": manifest_digest,
        },
        "builder": {"id": "build-problem-repository", "version": BUILDER_VERSION, "sha256": sha256_file(builder_path)},
        "problem": {
            "problem_id": problem["problem_id"],
            "contract_sha256": contract_digest,
            "lifecycle": problem["lifecycle"],
            "admission": problem_admission,
        },
        "active_skills": skills,
        "files": sorted(listed_files, key=lambda item: item["path"]),
        "digest_excludes": sorted(IDENTITY_EXCLUDES),
        "excludes": manifest["global_excludes"],
        "tree_sha256": tree_digest(listed_files),
        "built_at": built_at,
    }
    validate_json(snapshot, TASK / "harness-snapshot-manifest.v1.schema.json", "Harness snapshot")
    write_json(output / "HARNESS_SNAPSHOT.json", snapshot)
    snapshot_sha = sha256_file(output / "HARNESS_SNAPSHOT.json")
    history = {
        "schema_version": "1.0.0",
        "repository": args.repository,
        "repository_identity": {
            "database_id": args.repository_database_id,
            "node_id": args.repository_node_id,
            "default_branch": args.default_branch,
            "visibility": args.visibility,
        },
        "entries": [{
            "harness_snapshot_sha256": snapshot_sha,
            "harness_version": snapshot["harness_version"],
            "tree_sha256": snapshot["tree_sha256"],
            "source_manifest_sha256": snapshot["source"]["source_manifest_sha256"],
            "importer_policy_sha256": sha256_file(output / "scripts/import_web_attempt.py"),
        }],
    }
    validate_json(
        history,
        TASK / "harness-snapshot-history.v1.schema.json",
        "Harness snapshot history",
    )
    write_json(output / "HARNESS_SNAPSHOT_HISTORY.json", history)

    bootstrap_template = (template / "WEB_BOOTSTRAP.md.in").read_text(encoding="utf-8")
    replacements = {
        "{{REPOSITORY}}": args.repository,
        "{{REPOSITORY_BINDING}}": repository_binding,
        "{{REPOSITORY_DATABASE_ID}}": str(args.repository_database_id) if args.repository_database_id is not None else "pending",
        "{{REPOSITORY_NODE_ID}}": args.repository_node_id or "pending",
        "{{DEFAULT_BRANCH}}": args.default_branch,
        "{{VISIBILITY}}": args.visibility,
        "{{PROBLEM_ID}}": problem["problem_id"],
        "{{CONTRACT_SHA256}}": contract_digest,
        "{{PROBLEM_LIFECYCLE}}": problem["lifecycle"],
        "{{PROBLEM_ADMISSION}}": problem_admission,
        "{{SUITE_ID}}": manifest["manifest_id"],
        "{{SUITE_VERSION}}": manifest["harness_version"],
        "{{SUITE_MANIFEST_SHA256}}": manifest_digest,
        "{{HARNESS_SNAPSHOT_SHA256}}": snapshot_sha,
    }
    bootstrap = bootstrap_template
    for token, value in replacements.items():
        bootstrap = bootstrap.replace(token, value)
    if "{{" in bootstrap or "}}" in bootstrap:
        raise RuntimeError("unresolved WEB_BOOTSTRAP template placeholder")
    (output / "WEB_BOOTSTRAP.md").write_text(bootstrap, encoding="utf-8")
    os.chmod(output / "WEB_BOOTSTRAP.md", 0o644)

    report = {
        "decision": "PASS",
        "output": str(output),
        "repository": args.repository,
        "repository_binding": repository_binding,
        "repository_database_id": args.repository_database_id,
        "repository_node_id": args.repository_node_id,
        "default_branch": args.default_branch,
        "visibility": args.visibility,
        "problem_id": problem["problem_id"],
        "contract_sha256": contract_digest,
        "problem_lifecycle": problem["lifecycle"],
        "problem_admission": problem_admission,
        "snapshot_sha256": snapshot_sha,
        "tree_sha256": snapshot["tree_sha256"],
        "files": len(snapshot["files"]),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained Web GPT problem repository.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--problem-file", type=Path, required=True)
    parser.add_argument("--repository", required=True, help="GitHub OWNER/REPO identity")
    parser.add_argument("--repository-database-id", type=int)
    parser.add_argument("--repository-node-id")
    parser.add_argument("--default-branch", default="main")
    parser.add_argument("--visibility", choices=("private", "public"), default="private")
    parser.add_argument("--allow-planned-repository-identity", action="store_true", help="preview/local testing only")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-dirty-source", action="store_true", help="synthetic/local testing only")
    parser.add_argument("--allow-draft-problem", action="store_true", help="preview/local testing only")
    parser.add_argument("--allow-unadmitted-problem", action="store_true", help="preview/local testing only")
    parser.add_argument("--canonical-ledger", type=Path)
    parser.add_argument("--attempts-file", type=Path)
    parser.add_argument("--failed-routes-file", type=Path)
    parser.add_argument("--obligation-graphs-file", type=Path)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repository):
        print("BLOCK: invalid repository identity", file=sys.stderr)
        return 1
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", args.default_branch) or args.default_branch.startswith("/") or ".." in args.default_branch:
        print("BLOCK: invalid default branch", file=sys.stderr)
        return 1
    if args.repository_database_id is not None and args.repository_database_id < 1:
        print("BLOCK: invalid repository database ID", file=sys.stderr)
        return 1
    try:
        report = build(args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) if args.json else (
        f"problem repository build: PASS problem={report['problem_id']} files={report['files']} tree={report['tree_sha256']}"
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
