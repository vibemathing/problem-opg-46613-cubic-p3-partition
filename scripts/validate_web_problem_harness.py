#!/usr/bin/env python3
"""Validate a self-contained Web GPT problem-repository Harness snapshot."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from vibe_mathing.web_channel import (
    canonical_json_sha256,
    load_json,
    load_problem,
    scan_private_text,
    sha256_file,
    snapshot_file_sha256,
    validate_schema,
)

REQUIRED_CONTROL_FILES = {
    ".gitignore",
    "README.md",
    "Makefile",
    "requirements.txt",
    "requirements-web-harness.txt",
    "AGENTS.md",
    ".github/AGENTS.md",
    ".github/workflows/web-candidate-gate.yml",
    "governance/harness/PROJECT_AGENTS.md",
    "WEB_BOOTSTRAP.md",
    "WEB_CONTEXT_BUNDLE.md",
    "WEB_CHANNEL_PROFILE.json",
    "WEB_ACTIVE_SKILLS.json",
    "WEB_OUTPUT_CONTRACT.json",
    "HARNESS_SNAPSHOT.json",
    ".codex/AGENTS.md",
    ".codex/skills/README.md",
    "problem-library/records/canonical-problems.jsonl",
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
    "governance/control-plane/math-knowledge-source.v1.json",
    "governance/control-plane/math-knowledge-operators.v1.json",
    "governance/control-plane/harness-source-manifest.v1.json",
    "governance/control-plane/harness-source-manifest.v1.schema.json",
    "governance/control-plane/container-skill-source-lock.v1.json",
    "governance/control-plane/container-skill-source-lock.v1.schema.json",
    "governance/control-plane/harness-snapshot-manifest.v1.schema.json",
    "scripts/build_problem_repository.py",
    "scripts/build_web_context_bundle.py",
    "scripts/sync_problem_repository_harness.py",
    "scripts/validate_math_knowledge_registry.py",
    "scripts/validate_web_problem_harness.py",
    "scripts/validate_web_attempt.py",
    "scripts/validate_web_pr_diff.py",
    "scripts/import_web_attempt.py",
}
FORBIDDEN_PARTS = {".private", ".lake", "sessions", "vendor"}
FORBIDDEN_LOCAL_RUNTIME_FILES = {
    "persistent-worker-checkpoint.schema.json",
    "research-execution-scope.v1.schema.json",
    "resume-session-receipt.schema.json",
}
REQUIRED_EXCLUDED_CONTAINER_SKILLS = {"auto-goal", "auto-tmux", "nvidia-private-compute"}
PRIVATE_REPOSITORY_LOCATOR = re.compile(
    r"\b(?:vibemathing|tradecatlabs)/[A-Za-z0-9_.-]*internal[A-Za-z0-9_.-]*\b"
)
MUTABLE_RECORDS = {
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
}


def tree_digest(files: list[dict[str, Any]]) -> str:
    payload = [
        {key: item[key] for key in ("path", "bytes", "mode", "sha256", "layer", "owner")}
        for item in sorted(files, key=lambda item: item["path"])
    ]
    return canonical_json_sha256(payload)


def content_snapshot(root: Path) -> dict[str, Any]:
    files = [path for path in sorted(root.rglob("*")) if path.is_file() and not path.is_symlink()]
    rows = [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in files
    ]
    return {
        "files": len(rows),
        "bytes": sum(item["bytes"] for item in rows),
        "tree_sha256": canonical_json_sha256(rows),
    }


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative in sorted(REQUIRED_CONTROL_FILES):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"required regular file missing: {relative}")

    try:
        snapshot = load_json(root / "HARNESS_SNAPSHOT.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load Harness snapshot: {exc}"]
    schema_path = root / "governance/control-plane/harness-snapshot-manifest.v1.schema.json"
    if not schema_path.is_file():
        errors.append("missing Harness snapshot schema")
    else:
        errors.extend(f"snapshot schema: {message}" for message in validate_schema(snapshot, schema_path))

    listed = snapshot.get("files", [])
    if not isinstance(listed, list):
        return errors + ["snapshot files must be an array"]
    paths = [item.get("path") for item in listed if isinstance(item, dict)]
    if paths != sorted(paths):
        errors.append("snapshot file list is not sorted")
    if len(paths) != len(set(paths)):
        errors.append("snapshot file list contains duplicates")
    if set(paths) & MUTABLE_RECORDS:
        errors.append("mutable record ledger must not be owned by Harness snapshot")

    for item in listed:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        relative = item["path"]
        path = root / relative
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            errors.append(f"snapshot path missing or escapes root: {relative}")
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"snapshot path is not a regular file: {relative}")
            continue
        actual_mode = "0755" if path.stat().st_mode & 0o111 else "0644"
        if item.get("mode") != actual_mode:
            errors.append(f"mode mismatch: {relative}")
        if item.get("bytes") != path.stat().st_size:
            errors.append(f"size mismatch: {relative}")
        if item.get("sha256") != sha256_file(path):
            errors.append(f"digest mismatch: {relative}")
    if listed and snapshot.get("tree_sha256") != tree_digest(listed):
        errors.append("Harness tree digest mismatch")
    repository_identity = snapshot.get("repository_identity", {})
    if repository_identity.get("full_name") != snapshot.get("repository"):
        errors.append("snapshot repository identity/full name mismatch")
    if repository_identity.get("binding_state") == "verified":
        if not isinstance(repository_identity.get("database_id"), int) or not repository_identity.get("node_id"):
            errors.append("verified repository identity lacks database/node ID")

    try:
        problem = load_problem(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        problem = None
    if problem is not None:
        problem_schema = root / "problem-library/schema/canonical-problem.schema.json"
        if problem_schema.is_file():
            errors.extend(f"ProblemContract schema: {message}" for message in validate_schema(problem, problem_schema))
        contract_digest = canonical_json_sha256(problem)
        if snapshot.get("problem", {}).get("problem_id") != problem.get("problem_id"):
            errors.append("snapshot Problem ID mismatch")
        if snapshot.get("problem", {}).get("contract_sha256") != contract_digest:
            errors.append("snapshot ProblemContract digest mismatch")
        if snapshot.get("problem", {}).get("lifecycle") != problem.get("lifecycle"):
            errors.append("snapshot Problem lifecycle mismatch")

    try:
        profile = load_json(root / "WEB_CHANNEL_PROFILE.json")
        profile_schema = root / "governance/control-plane/web-research-channel.schema.json"
        errors.extend(f"web profile schema: {message}" for message in validate_schema(profile, profile_schema))
        output_contract = load_json(root / "WEB_OUTPUT_CONTRACT.json")
        if output_contract.get("channel") != profile.get("channel_id"):
            errors.append("WEB_OUTPUT_CONTRACT channel mismatch")
        if output_contract.get("allowed_write_paths") != profile.get("allowed_repository_write_paths"):
            errors.append("WEB_OUTPUT_CONTRACT allowed paths drift")
        if output_contract.get("prohibited_write_paths") != profile.get("prohibited_repository_write_paths"):
            errors.append("WEB_OUTPUT_CONTRACT prohibited paths drift")
        if output_contract.get("autonomy_policy") != profile.get("autonomy_policy"):
            errors.append("WEB_OUTPUT_CONTRACT autonomy policy drift")
        if output_contract.get("repository_scope_policy") != profile.get("repository_scope_policy"):
            errors.append("WEB_OUTPUT_CONTRACT repository scope policy drift")
        required_operations = {
            "issue_create", "candidate_branch_create", "candidate_file_create", "candidate_file_update",
            "candidate_file_delete", "commit_create", "pull_request_create", "pull_request_review",
            "actions_read", "actions_rerun_existing_candidate_run", "pull_request_merge", "checkpoint",
        }
        if set(output_contract.get("allowed_github_operations", [])) != required_operations:
            errors.append("WEB_OUTPUT_CONTRACT lacks AI-native candidate operations")
        if profile.get("github_permissions", {}).get("actions") != "write":
            errors.append("AI-native candidate workflow requires Actions write for rerun")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"web control JSON invalid: {exc}")
        profile = {}

    try:
        source_manifest = load_json(root / "governance/control-plane/harness-source-manifest.v1.json")
        source_manifest_schema = root / "governance/control-plane/harness-source-manifest.v1.schema.json"
        errors.extend(f"source manifest: {message}" for message in validate_schema(source_manifest, source_manifest_schema))
        excluded_container_skills = set(source_manifest.get("excluded_container_skill_ids", []))
        if not REQUIRED_EXCLUDED_CONTAINER_SKILLS.issubset(excluded_container_skills):
            errors.append("source manifest must exclude auto-goal, auto-tmux and nvidia-private-compute")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"source manifest invalid: {exc}")
        excluded_container_skills = set(REQUIRED_EXCLUDED_CONTAINER_SKILLS)

    try:
        container_lock = load_json(root / "governance/control-plane/container-skill-source-lock.v1.json")
        lock_schema = root / "governance/control-plane/container-skill-source-lock.v1.schema.json"
        errors.extend(f"container Skill lock: {message}" for message in validate_schema(container_lock, lock_schema))
        if not REQUIRED_EXCLUDED_CONTAINER_SKILLS.issubset(set(container_lock.get("excluded_skill_ids", []))):
            errors.append("container Skill lock lacks required Web exclusions")
        locked_skills = {item.get("skill_id"): item for item in container_lock.get("skills", []) if isinstance(item, dict)}
        expected_locked = {"solve": "active", "math-toolchain": "constrained"}
        if {key: value.get("web_status") for key, value in locked_skills.items()} != expected_locked:
            errors.append("container Skill lock must admit exactly solve=active and math-toolchain=constrained")
        for skill_id, expected_status in expected_locked.items():
            skill_root = root / ".codex/skills" / skill_id
            if not skill_root.is_dir() or skill_root.is_symlink():
                errors.append(f"distributed container Skill missing: {skill_id}")
                continue
            observed = content_snapshot(skill_root)
            expected_snapshot = locked_skills.get(skill_id, {}).get("distributed_snapshot", {})
            for field in ("files", "bytes", "tree_sha256"):
                if observed.get(field) != expected_snapshot.get(field):
                    errors.append(f"distributed container Skill {field} mismatch: {skill_id}")
            version_path = skill_root / "VERSION"
            if version_path.is_file() and version_path.read_text(encoding="utf-8").strip() != expected_snapshot.get("version"):
                errors.append(f"distributed container Skill version mismatch: {skill_id}")
            if locked_skills.get(skill_id, {}).get("evidence_ceiling") != "candidate_only":
                errors.append(f"container Skill evidence ceiling must be candidate_only: {skill_id}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"container Skill lock invalid: {exc}")

    for stem in ("math-knowledge-source", "math-knowledge-operators"):
        config_path = root / f"governance/control-plane/{stem}.v1.json"
        registry_schema = root / f"governance/control-plane/{stem}.schema.json"
        try:
            config = load_json(config_path)
            errors.extend(f"{stem}: {message}" for message in validate_schema(config, registry_schema))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{stem} invalid: {exc}")

    try:
        active = load_json(root / "WEB_ACTIVE_SKILLS.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"WEB_ACTIVE_SKILLS invalid: {exc}")
        active = {"skills": []}
    snapshot_skills = {item.get("skill_id"): item for item in snapshot.get("active_skills", []) if isinstance(item, dict)}
    expected_skill_status = {
        "vibe-mathing-router": "active",
        "math-discovery": "active",
        "math-derivation": "active",
        "math-computation": "constrained",
        "math-proof": "active",
        "math-formalization": "constrained",
        "solve": "active",
        "math-toolchain": "constrained",
    }
    expected_skill_ids = set(expected_skill_status)
    actual_skill_ids = {item.get("skill_id") for item in active.get("skills", []) if isinstance(item, dict)}
    if actual_skill_ids != expected_skill_ids:
        errors.append(f"WEB_ACTIVE_SKILLS must contain exactly the 8 admitted Web research Skills: {sorted(actual_skill_ids)}")
    for item in active.get("skills", []):
        if isinstance(item, dict) and item.get("skill_id") in expected_skill_status:
            if item.get("web_status") != expected_skill_status[item["skill_id"]]:
                errors.append(f"WEB Skill status mismatch: {item.get('skill_id')}")
    if (root / ".codex/skills/nvidia-private-compute").exists():
        errors.append("nvidia-private-compute is host-only and must not enter Web problem repositories")
    for item in active.get("skills", []):
        if not isinstance(item, dict):
            errors.append("WEB_ACTIVE_SKILLS contains non-object")
            continue
        skill_id = item.get("skill_id")
        entry = root / str(item.get("entry", ""))
        if not entry.is_file() or entry.is_symlink():
            errors.append(f"active Skill entry missing: {skill_id}")
            continue
        if item.get("entry_sha256") != sha256_file(entry):
            errors.append(f"active Skill digest mismatch: {skill_id}")
        if snapshot_skills.get(skill_id) != item:
            errors.append(f"active Skill does not match snapshot: {skill_id}")

    bootstrap = root / "WEB_BOOTSTRAP.md"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        try:
            expected_snapshot_sha = snapshot_file_sha256(root)
            if expected_snapshot_sha not in text:
                errors.append("WEB_BOOTSTRAP does not bind Harness snapshot digest")
        except ValueError as exc:
            errors.append(str(exc))
        if snapshot.get("repository") not in text:
            errors.append("WEB_BOOTSTRAP repository mismatch")
        if f"Repository binding: `{repository_identity.get('binding_state')}`" not in text:
            errors.append("WEB_BOOTSTRAP repository binding mismatch")
        expected_database_id = repository_identity.get("database_id") if repository_identity.get("database_id") is not None else "pending"
        expected_node_id = repository_identity.get("node_id") or "pending"
        if f"Repository database ID: `{expected_database_id}`" not in text:
            errors.append("WEB_BOOTSTRAP repository database ID mismatch")
        if f"Repository node ID: `{expected_node_id}`" not in text:
            errors.append("WEB_BOOTSTRAP repository node ID mismatch")
        if f"Default branch: `{repository_identity.get('default_branch')}`" not in text:
            errors.append("WEB_BOOTSTRAP default branch mismatch")
        if f"Visibility: `{repository_identity.get('visibility')}`" not in text:
            errors.append("WEB_BOOTSTRAP visibility mismatch")
        if snapshot.get("problem", {}).get("problem_id") not in text:
            errors.append("WEB_BOOTSTRAP Problem mismatch")
        if f"Problem lifecycle: `{snapshot.get('problem', {}).get('lifecycle')}`" not in text:
            errors.append("WEB_BOOTSTRAP Problem lifecycle mismatch")
        if f"Problem admission: `{snapshot.get('problem', {}).get('admission')}`" not in text:
            errors.append("WEB_BOOTSTRAP Problem admission mismatch")

    for path in sorted(root.rglob("*")):
        if path == root / ".git" or ".git" in path.relative_to(root).parts:
            continue
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            errors.append(f"forbidden Harness path: {relative.as_posix()}")
            continue
        if relative.name in FORBIDDEN_LOCAL_RUNTIME_FILES:
            errors.append(f"local runtime contract forbidden in Web problem repository: {relative.as_posix()}")
            continue
        if excluded_container_skills.intersection(relative.parts):
            errors.append(f"excluded container Skill path: {relative.as_posix()}")
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden in problem repository: {relative.as_posix()}")
        elif path.exists() and not path.is_dir() and not path.is_file():
            errors.append(f"non-regular repository member: {relative.as_posix()}")
        elif repository_identity.get("visibility") == "public" and path.is_file():
            try:
                public_text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
            else:
                if PRIVATE_REPOSITORY_LOCATOR.search(public_text):
                    errors.append(f"public repository exposes a private repository locator: {relative.as_posix()}")

    scan_roots = [
        root / "research/artifacts/web-inbox",
        root / "research/artifacts/candidates",
        root / "research/artifacts/source-notes",
    ]
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"binary web artifact forbidden: {path.relative_to(root).as_posix()}")
                continue
            for label in scan_private_text(text):
                errors.append(f"privacy finding {label}: {path.relative_to(root).as_posix()}")

    workflow = root / ".github/workflows/web-candidate-gate.yml"
    if workflow.is_file():
        workflow_text = workflow.read_text(encoding="utf-8")
        if "pull_request_target" in workflow_text:
            errors.append("candidate workflow must not use pull_request_target")
        if "contents: read" not in workflow_text or "persist-credentials: false" not in workflow_text:
            errors.append("candidate workflow lacks read-only checkout controls")
        if "pip install --require-hashes -r requirements-web-harness.txt" not in workflow_text:
            errors.append("candidate workflow dependencies are not hash-pinned")
        if "cache-dependency-path: requirements-web-harness.txt" not in workflow_text:
            errors.append("candidate workflow lacks an explicit pip cache dependency path")
        required_check_jobs = set(profile.get("branch_policy", {}).get("required_checks", []))
        for check_name in sorted(required_check_jobs):
            job_pattern = rf"(?m)^  {re.escape(check_name)}:\s*$"
            name_pattern = rf"(?m)^    name:\s*{re.escape(check_name)}\s*$"
            if not re.search(job_pattern, workflow_text) or not re.search(name_pattern, workflow_text):
                errors.append(f"candidate workflow lacks required status-check job: {check_name}")
        if "${{ secrets." in workflow_text:
            errors.append("candidate workflow must not receive secrets")
        for action_ref in re.findall(r"uses:\s*[^@\s]+@([^\s#]+)", workflow_text):
            if not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                errors.append(f"candidate workflow action is not commit-pinned: {action_ref}")

    makefile = root / "Makefile"
    if makefile.is_file():
        for script in re.findall(r"python3\s+(scripts/[A-Za-z0-9_./-]+\.py)", makefile.read_text(encoding="utf-8")):
            if not (root / script).is_file():
                errors.append(f"Makefile references missing script: {script}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Web GPT problem repository Harness.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(args.project_root)
    report = {"decision": "PASS" if not errors else "BLOCK", "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"web problem Harness validation: {report['decision']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
