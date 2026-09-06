#!/usr/bin/env python3
"""Trusted importer from a validated Web attempt packet to Candidate records only."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from vibe_mathing.web_channel import (
    canonical_json_sha256,
    candidate_media_type,
    find_graph,
    find_obligation,
    load_jsonl,
    sha256_file,
    validate_packet,
    validate_schema,
)

VERSION = "1.0.0"


def relative_to_root(root: Path, path: Path) -> str:
    resolved = path.resolve(strict=True)
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError("packet must be inside the problem repository") from exc


def source_ref_text(ref: dict[str, Any]) -> str:
    relation = ref.get("relation", "unknown")
    return f"{ref['repository']}@{ref['revision']}:{ref['path']}#{relation}"


def build_candidates(root: Path, packet: dict[str, Any]) -> list[dict[str, Any]]:
    graph = find_graph(root, packet["graph_id"])
    if graph is None:
        raise RuntimeError("ObligationGraph disappeared after packet validation")
    obligation = find_obligation(graph, packet["obligation_id"])
    if obligation is None:
        raise RuntimeError("obligation disappeared after packet validation")
    statement_digest = obligation["statement_sha256"]
    source_refs = [source_ref_text(ref) for ref in packet["source_refs"]]
    records: list[dict[str, Any]] = []
    for candidate in packet["candidate_artifacts"]:
        locator = candidate["locator"]
        artifact_path = root / locator
        record = {
            "schema_version": "1.0.0",
            "candidate_id": candidate["candidate_id"],
            "graph_id": packet["graph_id"],
            "obligation_id": packet["obligation_id"],
            "problem_id": packet["problem_id"],
            "attempt_id": packet["attempt_id"],
            "statement_sha256": statement_digest,
            "kind": candidate["kind"],
            "generator": "chatgpt-web-github",
            "artifact": {
                "locator": locator,
                "sha256": candidate["sha256"],
                "media_type": candidate_media_type(artifact_path),
            },
            "source_refs": source_refs,
            "created_at": packet["created_at"],
        }
        records.append(record)
    return records


def write_pending(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def import_packet(root: Path, packet_path: Path) -> dict[str, Any]:
    root = root.resolve()
    packet, errors = validate_packet(root, packet_path)
    if packet is None or errors:
        raise RuntimeError("packet validation failed: " + "; ".join(errors))
    packet_relative = relative_to_root(root, packet_path)
    packet_sha = sha256_file(packet_path)
    receipt_id = f"web-import:{packet_sha}"
    receipt_dir = root / "research/artifacts/receipts/web-import"
    receipt_path = receipt_dir / f"{packet_sha}.json"
    pending_path = receipt_dir / f".{packet_sha}.pending"
    ledger_path = root / "research/records/candidate-artifacts.jsonl"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    script_path = Path(__file__).resolve()
    candidates = build_candidates(root, packet)
    candidate_schema = root / "research/schema/candidate-artifact.schema.json"
    for record in candidates:
        schema_errors = validate_schema(record, candidate_schema)
        if schema_errors:
            raise RuntimeError(f"Candidate schema failed for {record['candidate_id']}: {schema_errors[0]}")

    imported_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": receipt_id,
        "decision": "candidate_only",
        "channel": packet["channel"],
        "repository": packet["repository"],
        "packet": {"path": packet_relative, "sha256": packet_sha},
        "harness_snapshot_sha256": packet["harness_snapshot_sha256"],
        "problem_id": packet["problem_id"],
        "attempt_id": packet["attempt_id"],
        "route_id": packet["route_id"],
        "graph_id": packet["graph_id"],
        "obligation_id": packet["obligation_id"],
        "candidate_records": [
            {
                "candidate_id": record["candidate_id"],
                "record_sha256": canonical_json_sha256(record),
                "artifact_sha256": record["artifact"]["sha256"],
                "artifact_path": record["artifact"]["locator"],
            }
            for record in candidates
        ],
        "append_target": "research/records/candidate-artifacts.jsonl",
        "importer": {"principal": "trusted-web-attempt-importer", "version": VERSION, "script_sha256": sha256_file(script_path)},
        "imported_at": imported_at,
    }
    receipt_errors = validate_schema(receipt, root / "research/schema/web-import-receipt.schema.json")
    if receipt_errors:
        raise RuntimeError(f"import receipt schema failed: {receipt_errors[0]}")

    lock_path = ledger_path.with_suffix(ledger_path.suffix + ".lock")
    lock_path.touch(mode=0o600, exist_ok=True)
    with lock_path.open("r+") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        existing = load_jsonl(ledger_path)
        by_id = {record.get("candidate_id"): record for record in existing}
        if receipt_path.exists():
            old_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if old_receipt.get("packet", {}).get("sha256") != packet_sha:
                raise RuntimeError("existing import receipt identity mismatch")
            missing = [record["candidate_id"] for record in candidates if record["candidate_id"] not in by_id]
            if missing:
                raise RuntimeError(f"existing receipt has missing Candidate records: {missing}")
            return {"decision": "PASS", "idempotent": True, "receipt": receipt_path.relative_to(root).as_posix(), "candidates": len(candidates)}
        if pending_path.exists():
            raise RuntimeError(f"stale pending import requires review: {pending_path.relative_to(root)}")
        collisions = [record["candidate_id"] for record in candidates if record["candidate_id"] in by_id]
        if collisions:
            raise RuntimeError(f"Candidate ID already exists without matching receipt: {collisions}")
        write_pending(pending_path, receipt)
        try:
            with ledger_path.open("a", encoding="utf-8") as ledger:
                for record in candidates:
                    ledger.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                ledger.flush()
                os.fsync(ledger.fileno())
            os.replace(pending_path, receipt_path)
            os.chmod(receipt_path, 0o600)
            directory_fd = os.open(receipt_dir, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except BaseException:
            # Keep the pending receipt as a recovery marker; never silently retry.
            raise
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
    return {"decision": "PASS", "idempotent": False, "receipt": receipt_path.relative_to(root).as_posix(), "candidates": len(candidates)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a validated Web packet as Candidate records only.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    packet_path = args.packet if args.packet.is_absolute() else root / args.packet
    try:
        report = import_packet(root, packet_path)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) if args.json else (
        f"web attempt import: PASS candidates={report['candidates']} idempotent={report['idempotent']}"
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
