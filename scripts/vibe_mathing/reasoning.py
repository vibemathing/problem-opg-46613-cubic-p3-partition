"""Generated inheritance overlays for immutable scoped Agent instructions."""
from __future__ import annotations

import os
from pathlib import Path

REASONING_MARKER = "MATHEMATICAL_REASONING_DISCIPLINE_V1"
REASONING_STANDARD = "governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md"
REASONING_AGENT_OVERLAY = f"""

## Mandatory mathematical reasoning discipline

<!-- {REASONING_MARKER} -->

This scoped instruction file inherits `{REASONING_STANDARD}`. Its local rules may only tighten that standard; they cannot omit, replace, or weaken definition/quantifier freeze, traceable dependencies, valid induction and contraposition, explicit witnesses, counterexample pressure tests, invariants, termination, extremal/symmetry/probability/scale checks, or honest evidence ceilings.
""".encode("utf-8")


def apply_reasoning_agent_overlays(output: Path) -> None:
    """Append a reversible policy overlay to Agent files copied from immutable data."""
    for path in sorted(output.rglob("AGENTS.md")):
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"unsafe Agent instruction surface: {path}")
        data = path.read_bytes()
        if REASONING_MARKER.encode("utf-8") in data:
            if REASONING_STANDARD.encode("utf-8") not in data:
                raise RuntimeError(f"reasoning marker without standard link: {path}")
            continue
        path.write_bytes(data + REASONING_AGENT_OVERLAY)
        os.chmod(path, 0o644)


def strip_reasoning_agent_overlay(path: str, data: bytes) -> bytes:
    """Recover immutable source bytes when validating a generated Skill tree."""
    if path.endswith("AGENTS.md") and data.endswith(REASONING_AGENT_OVERLAY):
        return data[: -len(REASONING_AGENT_OVERLAY)]
    return data
