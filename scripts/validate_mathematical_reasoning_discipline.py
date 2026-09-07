#!/usr/bin/env python3
"""Validate the mandatory mathematical-reasoning policy and Agent inheritance surfaces."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vibe_mathing.web_channel import load_json, validate_schema

POLICY_PATH = Path("governance/control-plane/mathematical-reasoning-discipline.v1.json")
SCHEMA_PATH = Path("governance/control-plane/mathematical-reasoning-discipline.schema.json")
EXPECTED_SEQUENCE = [
    "definition_and_scope_freeze",
    "traceable_dependency_chain",
    "explicit_construction_or_witness",
    "counterexample_pressure_test",
    "invariant_analysis",
    "monovariant_and_termination",
    "extremal_symmetry_probability_checks",
    "scale_and_boundary_checks",
    "verifiable_evidence_and_honest_conclusion",
]
REQUIRED_STANDARD_SNIPPETS = [
    "定义与范围冻结",
    "可追踪依赖链",
    "显式构造或 witness",
    "反例压力测试",
    "不变量",
    "单调量与终止",
    "极值 / 对称 / 概率检查",
    "尺度与极端边界",
    "可复查证据与诚实结论",
    "证明 base case",
    "假设 `P(n)`",
    "推出 `P(n+1)`",
    "`P -> Q`",
    "`not Q -> not P`",
    "有限枚举、随机测试、数值实验和 SAT/SMT 搜索只在其精确范围内提供支持",
    "kernel check 不替代 statement-faithfulness",
]


def regular_inside(root: Path, relative: str) -> Path | None:
    candidate = root / relative
    try:
        candidate.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        return None
    if candidate.is_symlink() or not candidate.is_file():
        return None
    return candidate


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    policy_file = regular_inside(root, POLICY_PATH.as_posix())
    schema_file = regular_inside(root, SCHEMA_PATH.as_posix())
    if policy_file is None:
        errors.append(f"required regular file missing: {POLICY_PATH.as_posix()}")
        return errors
    if schema_file is None:
        errors.append(f"required regular file missing: {SCHEMA_PATH.as_posix()}")
        return errors
    try:
        policy = load_json(policy_file)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"reasoning policy invalid: {exc}"]
    errors.extend(f"reasoning policy schema: {message}" for message in validate_schema(policy, schema_file))

    marker = policy.get("marker")
    if policy.get("required_sequence") != EXPECTED_SEQUENCE:
        errors.append("reasoning policy sequence drift")
    standard_relative = policy.get("normative_standard_path")
    if not isinstance(marker, str) or not marker:
        errors.append("reasoning policy marker missing")
        marker = "MATHEMATICAL_REASONING_DISCIPLINE_V1"
    if not isinstance(standard_relative, str):
        errors.append("reasoning policy standard path missing")
        standard = None
    else:
        standard = regular_inside(root, standard_relative)
        if standard is None:
            errors.append(f"reasoning standard missing or unsafe: {standard_relative}")
    if standard is not None:
        text = standard.read_text(encoding="utf-8")
        if text.count(marker) < 2:
            errors.append("reasoning standard lacks paired policy markers")
        for snippet in REQUIRED_STANDARD_SNIPPETS:
            if snippet not in text:
                errors.append(f"reasoning standard lacks required rule: {snippet}")

    surfaces = policy.get("required_agent_surfaces", [])
    if not isinstance(surfaces, list):
        return errors + ["reasoning policy agent surfaces must be an array"]
    for relative in surfaces:
        if not isinstance(relative, str):
            errors.append("reasoning policy contains a non-string Agent surface")
            continue
        surface = regular_inside(root, relative)
        if surface is None:
            errors.append(f"required reasoning Agent surface missing or unsafe: {relative}")
            continue
        text = surface.read_text(encoding="utf-8")
        if marker not in text:
            errors.append(f"Agent surface does not inherit reasoning discipline: {relative}")
        if standard_relative not in text:
            errors.append(f"Agent surface does not link normative reasoning standard: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mathematical-reasoning discipline inheritance.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(args.project_root)
    report = {"decision": "PASS" if not errors else "BLOCK", "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"mathematical reasoning discipline: {report['decision']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
