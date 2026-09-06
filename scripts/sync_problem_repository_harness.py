#!/usr/bin/env python3
"""Diff or apply a deterministic Harness refresh to one problem repository."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from vibe_mathing.web_channel import load_json, sha256_file

ROOT = Path(__file__).resolve().parents[1]


def copy_atomic(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise RuntimeError(f"source is not a regular file: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(source.read_bytes())
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(temporary, 0o755 if source.stat().st_mode & 0o111 else 0o644)
    os.replace(temporary, target)


def by_path(snapshot: dict[str, Any], owner: str = "harness") -> dict[str, dict[str, Any]]:
    return {
        item["path"]: item
        for item in snapshot.get("files", [])
        if isinstance(item, dict) and item.get("owner") == owner and isinstance(item.get("path"), str)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or apply a problem-repository Harness snapshot refresh.")
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--target-root", type=Path, required=True)
    parser.add_argument("--allow-dirty-source", action="store_true", help="synthetic/local testing only")
    parser.add_argument("--allow-draft-problem", action="store_true", help="preview/local testing only")
    parser.add_argument("--allow-unadmitted-problem", action="store_true", help="preview/local testing only")
    parser.add_argument("--allow-planned-repository-identity", action="store_true", help="preview/local testing only")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.check == args.apply:
        print("BLOCK: choose exactly one of --check or --apply", file=sys.stderr)
        return 1
    source_root = args.source_root.resolve()
    target = args.target_root.resolve()
    try:
        old = load_json(target / "HARNESS_SNAPSHOT.json")
        repository = old["repository"]
        problem_file = target / "problem-library/records/canonical-problems.jsonl"
        with tempfile.TemporaryDirectory(prefix="vibe-web-harness-sync-") as temporary:
            built = Path(temporary) / "repo"
            command = [
                sys.executable,
                str(source_root / "scripts/build_problem_repository.py"),
                "--project-root", str(source_root),
                "--problem-file", str(problem_file),
                "--repository", repository,
                "--default-branch", str(old.get("repository_identity", {}).get("default_branch", "main")),
                "--output", str(built),
                "--attempts-file", str(target / "research/records/attempts.jsonl"),
                "--failed-routes-file", str(target / "research/records/failed-routes.jsonl"),
                "--obligation-graphs-file", str(target / "research/records/obligation-graphs.jsonl"),
                "--json",
            ]
            if args.allow_dirty_source:
                command.append("--allow-dirty-source")
            if args.allow_draft_problem:
                command.append("--allow-draft-problem")
            if args.allow_unadmitted_problem:
                command.append("--allow-unadmitted-problem")
            identity = old.get("repository_identity", {})
            if identity.get("binding_state") == "verified":
                command.extend([
                    "--repository-database-id", str(identity["database_id"]),
                    "--repository-node-id", str(identity["node_id"]),
                ])
            elif args.allow_planned_repository_identity:
                command.append("--allow-planned-repository-identity")
            else:
                raise RuntimeError("target snapshot lacks verified repository identity")
            result = subprocess.run(command, cwd=source_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or "replacement Harness build failed")
            new = load_json(built / "HARNESS_SNAPSHOT.json")
            old_files = by_path(old)
            new_files = by_path(new)
            added = sorted(set(new_files) - set(old_files))
            removed = sorted(set(old_files) - set(new_files))
            changed = sorted(path for path in set(old_files) & set(new_files) if old_files[path]["sha256"] != new_files[path]["sha256"] or old_files[path]["mode"] != new_files[path]["mode"])
            generated = ["WEB_BOOTSTRAP.md", "WEB_CONTEXT_BUNDLE.md", "WEB_CHANNEL_PROFILE.json", "WEB_ACTIVE_SKILLS.json", "WEB_OUTPUT_CONTRACT.json", "HARNESS_SNAPSHOT.json"]
            changed_generated = sorted(path for path in generated if not (target / path).is_file() or sha256_file(target / path) != sha256_file(built / path))
            drift = bool(added or removed or changed or changed_generated)
            if args.apply:
                for path in removed + changed:
                    target_path = target / path
                    if target_path.is_symlink() or not target_path.is_file():
                        raise RuntimeError(f"cannot safely replace/remove old Harness path: {path}")
                    if sha256_file(target_path) != old_files[path]["sha256"]:
                        raise RuntimeError(f"refuse to replace/remove locally modified Harness file: {path}")
                for path in added + changed:
                    copy_atomic(built / path, target / path)
                for path in changed_generated:
                    copy_atomic(built / path, target / path)
                for path in removed:
                    (target / path).unlink()
                # Validate after update; rollback is deliberately not automated.
                validation = subprocess.run(
                    [sys.executable, str(target / "scripts/validate_web_problem_harness.py"), "--project-root", str(target)],
                    cwd=target,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                if validation.returncode != 0:
                    raise RuntimeError(validation.stderr.strip() or validation.stdout.strip() or "post-sync Harness validation failed")
            report = {
                "decision": "PASS" if args.apply or not drift else "DRIFT",
                "mode": "apply" if args.apply else "check",
                "old_tree_sha256": old.get("tree_sha256"),
                "new_tree_sha256": new.get("tree_sha256"),
                "added": added,
                "changed": changed,
                "removed": removed,
                "changed_generated": changed_generated,
            }
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"problem Harness sync: {report['decision']} mode={report['mode']} added={len(report['added'])} changed={len(report['changed'])} removed={len(report['removed'])}")
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
