#!/usr/bin/env python3
"""Run the bounded Lean obligation verifier; never append truth ledgers itself."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath

from vibe_mathing.lean_obligation import LeanObligationError, verify_lean_obligation


ROOT = Path(__file__).resolve().parents[1]


def _safe_path(root: Path, locator: str) -> Path:
    pure = PurePosixPath(locator)
    if pure.is_absolute() or ".." in pure.parts or "\\" in locator:
        raise ValueError(f"非法 project-relative path：{locator}")
    path = root.joinpath(*pure.parts)
    path.resolve(strict=False).relative_to(root.resolve())
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("request", help="project-relative Lean obligation request JSON")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument(
        "--packet-out",
        help="optional project-relative research/artifacts output; EvidenceLinks are still uncommitted",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    try:
        request_path = _safe_path(root, args.request)
        request = json.loads(request_path.read_text(encoding="utf-8"))
        result = verify_lean_obligation(project_root=root, request=request)
        encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.packet_out:
            if not args.packet_out.startswith("research/artifacts/"):
                raise ValueError("packet-out 必须位于 research/artifacts/")
            output = _safe_path(root, args.packet_out)
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_name(f".{output.name}.{os.getpid()}.tmp")
            try:
                temporary.write_text(encoded, encoding="utf-8")
                os.replace(temporary, output)
            finally:
                temporary.unlink(missing_ok=True)
        print(encoded, end="")
        return 0 if all(result["decisions"].values()) else 2
    except (OSError, ValueError, json.JSONDecodeError, LeanObligationError) as exc:
        print(json.dumps({"decision": "BLOCK", "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
