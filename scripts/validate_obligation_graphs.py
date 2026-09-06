#!/usr/bin/env python3
"""Validate obligation truth ledgers and optionally emit deterministic closure views."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from vibe_mathing.obligations import (
    ObligationError,
    derive_all_obligation_closures,
    load_obligation_state,
    validate_obligation_records,
)


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    errors = validate_obligation_records(root)
    if errors:
        payload = {"decision": "BLOCK", "errors": errors}
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
        else:
            for error in errors:
                print(f"BLOCK: {error}")
        return 1
    try:
        state = load_obligation_state(root)
        closures = derive_all_obligation_closures(root)
    except ObligationError as exc:
        print(f"BLOCK: {exc}")
        return 1
    payload = {
        "decision": "PASS",
        "graphs": len(state["graphs"]),
        "candidates": len(state["candidates"]),
        "evidence_links": len(state["links"]),
        "closures": closures,
    }
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(
            "obligation harness: PASS "
            f"graphs={payload['graphs']} candidates={payload['candidates']} "
            f"evidence_links={payload['evidence_links']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
