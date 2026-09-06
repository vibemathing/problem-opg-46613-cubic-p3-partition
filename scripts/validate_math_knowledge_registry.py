#!/usr/bin/env python3
"""Validate fail-closed mathematical knowledge source and operator registries."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def validate(source_registry: dict[str, Any], operator_registry: dict[str, Any], source_schema: dict[str, Any], operator_schema: dict[str, Any], skills_root: Path) -> list[str]:
    errors = [f"source schema: {message}" for message in schema_errors(source_registry, source_schema)]
    errors.extend(f"operator schema: {message}" for message in schema_errors(operator_registry, operator_schema))

    sources = source_registry.get("sources", [])
    source_ids = [item.get("source_id") for item in sources if isinstance(item, dict)]
    if len(source_ids) != len(set(source_ids)):
        errors.append("duplicate mathematical knowledge source_id")
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id")
        maturity = source.get("maturity")
        status = source.get("operational_status")
        ceiling = source.get("evidence_ceiling")
        license_data = source.get("license", {})
        controls = set(source.get("required_controls", []))
        if status == "design_only" and maturity not in {"surveyed", "source_locked"}:
            errors.append(f"design-only source overstates maturity: {source_id}")
        if status in {"quarantined", "suspended"} and "fresh_replay" not in controls and ceiling == "verifier_input":
            errors.append(f"quarantined verifier input lacks fresh_replay control: {source_id}")
        if license_data.get("status") != "reviewed" and "redistribution" in license_data.get("allowed_uses", []):
            errors.append(f"unreviewed license permits redistribution: {source_id}")
        if not license_data.get("bulk_cache", False) and "bulk_snapshot" in source.get("access_modes", []):
            errors.append(f"source offers bulk_snapshot while bulk_cache is false: {source_id}")
        if ceiling in {"computation_evidence", "verifier_input"} and status == "design_only" and "consumer_required" not in controls:
            errors.append(f"design-only high-ceiling source lacks consumer_required: {source_id}")

    operators = operator_registry.get("operators", [])
    operator_ids = [item.get("operator_id") for item in operators if isinstance(item, dict)]
    if len(operator_ids) != len(set(operator_ids)):
        errors.append("duplicate mathematical knowledge operator_id")
    for operator in operators:
        if not isinstance(operator, dict):
            continue
        operator_id = operator.get("operator_id")
        owner = operator.get("owner_skill")
        if not (skills_root / str(owner) / "SKILL.md").is_file():
            errors.append(f"operator owner Skill does not exist: {operator_id} -> {owner}")
        effect = operator.get("external_effect")
        ceiling = operator.get("evidence_ceiling")
        controls = set(operator.get("requires", [])) | set(operator.get("fail_closed_on", []))
        if effect == "read_network" and ceiling not in {"discovery_only", "candidate_only"}:
            errors.append(f"network search operator exceeds candidate ceiling: {operator_id}")
        if effect in {"bounded_candidate_build", "bounded_candidate_compute"} and "timeout" not in set(operator.get("fail_closed_on", [])):
            errors.append(f"bounded execution operator lacks timeout failure: {operator_id}")
        if ceiling == "verifier_receipt" and "verifier_registry" not in controls and "review_policy" not in controls:
            errors.append(f"verifier-receipt operator lacks verifier/review policy: {operator_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mathematical knowledge source/operator registries.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    control = root / "governance/control-plane"
    try:
        source = json.loads((control / "math-knowledge-source.v1.json").read_text(encoding="utf-8"))
        operators = json.loads((control / "math-knowledge-operators.v1.json").read_text(encoding="utf-8"))
        source_schema = json.loads((control / "math-knowledge-source.schema.json").read_text(encoding="utf-8"))
        operator_schema = json.loads((control / "math-knowledge-operators.schema.json").read_text(encoding="utf-8"))
        errors = validate(source, operators, source_schema, operator_schema, root / ".codex/skills")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        source = {"sources": []}
        operators = {"operators": []}
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "sources": len(source.get("sources", [])),
        "operators": len(operators.get("operators", [])),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"math knowledge registry: {report['decision']} sources={report['sources']} operators={report['operators']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
