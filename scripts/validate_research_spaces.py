#!/usr/bin/env python3
# 做什么：校验 Problem、Attempt、Result 引用与二维状态，并重算完整解索引。
# 怎么运行：python3 scripts/validate_research_spaces.py [--write-index]
# 需要什么：Python 3、jsonschema；默认只读，--write-index 只更新派生索引。

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from vibe_mathing.evidence import (
    EvidenceError,
    load_verifier_registry,
    verify_evidence_receipt,
)
from vibe_mathing.obligations import (
    ObligationError,
    obligation_result_gate,
    validate_obligation_records,
)
from vibe_mathing.store import ResearchStore

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_PATH = ROOT / "problem-library" / "records" / "canonical-problems.jsonl"
PROBLEM_SCHEMA_PATH = ROOT / "problem-library" / "schema" / "canonical-problem.schema.json"
SOURCE_RECORDS_PATH = ROOT / "problem-library" / "records" / "problems.jsonl"
ATTEMPTS_PATH = ROOT / "research" / "records" / "attempts.jsonl"
ATTEMPT_SCHEMA_PATH = ROOT / "research" / "schema" / "attempt.schema.json"
RESULTS_PATH = ROOT / "result-library" / "records" / "results.jsonl"
RESULT_SCHEMA_PATH = ROOT / "result-library" / "schema" / "result.schema.json"
SOLUTIONS_PATH = ROOT / "result-library" / "indexes" / "solutions.json"
VERIFIER_REGISTRY_PATH = ROOT / "research" / "verifiers.json"
VERIFIER_SCHEMA_PATH = ROOT / "research" / "schema" / "verifier-registry.schema.json"
RECEIPT_SCHEMA_PATH = ROOT / "research" / "schema" / "evidence-receipt.schema.json"

SOLUTION_KINDS = {"proof", "counterexample"}
NON_CLOSING_KINDS = {
    "partial_result",
    "conditional_result",
    "numerical_evidence",
    "symbolic_evidence",
    "failed_approach",
}
EXPECTED_SOLUTION_OUTCOME = {"proof": "established", "counterexample": "refuted"}
ALLOWED_OUTCOMES = {
    "proof": {"undetermined", "supported", "established", "inconclusive", "withdrawn"},
    "counterexample": {"undetermined", "supported", "refuted", "inconclusive", "withdrawn"},
    "partial_result": {"undetermined", "supported", "inconclusive", "withdrawn"},
    "conditional_result": {"undetermined", "supported", "inconclusive", "withdrawn"},
    "numerical_evidence": {"undetermined", "supported", "inconclusive", "withdrawn"},
    "symbolic_evidence": {"undetermined", "supported", "inconclusive", "withdrawn"},
    "failed_approach": {"inconclusive", "withdrawn"},
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: JSON 无效：{exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: 记录不是对象。")
            records.append(record)
    return records


def validate_records(
    path: Path,
    schema_path: Path,
    id_field: str,
    errors: list[str],
) -> tuple[list[dict[str, Any]], set[str]]:
    records = load_jsonl(path)
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    ids: set[str] = set()
    for position, record in enumerate(records, 1):
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
            location = ".".join(str(item) for item in error.path) or "<root>"
            errors.append(f"{path.relative_to(ROOT)}:{position}:{location}: {error.message}")
        record_id = record.get(id_field)
        if isinstance(record_id, str):
            if record_id in ids:
                errors.append(f"{path.relative_to(ROOT)}: 重复 ID：{record_id}")
            ids.add(record_id)
    return records, ids


def load_source_record_ids(project_root: Path = ROOT) -> set[str]:
    source_records_path = (
        project_root / "problem-library" / "records" / "problems.jsonl"
    )
    if not source_records_path.is_file():
        return set()
    return {
        record["id"]
        for record in load_jsonl(source_records_path)
        if isinstance(record.get("id"), str)
    }


def accepted_independent_capabilities(
    result: dict[str, Any],
    generator: str,
    *,
    project_root: Path = ROOT,
    errors: list[str] | None = None,
) -> set[str]:
    validated: list[tuple[dict[str, Any], str]] = []
    for item in result.get("evidence", []):
        try:
            capability = verify_evidence_receipt(
                project_root=project_root,
                result=result,
                evidence=item,
                generator=generator,
            )
        except EvidenceError as exc:
            if errors is not None:
                errors.append(
                    f"{result.get('result_id')}: 证据 {item.get('evidence_id')} 无效：{exc}"
                )
            continue
        validated.append((item, capability))
    validated_by_id = {item.get("evidence_id"): (item, capability) for item, capability in validated}
    invalidated_ids: set[str] = set()
    for item, capability in validated:
        if item.get("verdict") != "reject" or item.get("independent") is not True:
            continue
        for evidence_id in item.get("invalidates", []):
            target = validated_by_id.get(evidence_id)
            if target is not None and target[1] == capability:
                invalidated_ids.add(evidence_id)
    return {
        capability
        for item, capability in validated
        if item.get("verdict") == "accept"
        and item.get("independent") is True
        and item.get("evidence_id") not in invalidated_ids
    }


def has_direct_solution_evidence(kind: str, capabilities: set[str]) -> bool:
    if kind == "proof":
        return "human_review" in capabilities or {
            "kernel_check",
            "axiom_escape_audit",
        }.issubset(capabilities)
    if kind == "counterexample":
        return bool(
            capabilities.intersection({"counterexample_check", "human_review"})
        ) or {"kernel_check", "axiom_escape_audit"}.issubset(capabilities)
    return False


def qualifies_as_solution(
    result: dict[str, Any],
    attempts_by_id: dict[str, dict[str, Any]],
    *,
    project_root: Path = ROOT,
    errors: list[str] | None = None,
) -> bool:
    kind = result.get("kind")
    if kind not in SOLUTION_KINDS:
        return False
    attempt = attempts_by_id.get(result.get("attempt_id"))
    if attempt is None or attempt.get("problem_id") != result.get("problem_id"):
        return False
    generator = attempt.get("generator")
    if not isinstance(generator, str) or not generator:
        return False
    capabilities = accepted_independent_capabilities(
        result, generator, project_root=project_root, errors=errors
    )
    try:
        obligation_gate = obligation_result_gate(project_root, result, attempt)
    except ObligationError as exc:
        if errors is not None:
            errors.append(f"{result.get('result_id')}: Obligation closure gate：{exc}")
        return False
    capabilities.update(obligation_gate["capabilities"])
    return (
        has_direct_solution_evidence(kind, capabilities)
        and "statement_faithfulness" in capabilities
    )


def derive_solution_ids(
    results: list[dict[str, Any]],
    attempts_by_id: dict[str, dict[str, Any]],
    *,
    project_root: Path = ROOT,
) -> list[str]:
    return sorted(
        result["result_id"]
        for result in results
        if qualifies_as_solution(result, attempts_by_id, project_root=project_root)
        and result.get("outcome") == EXPECTED_SOLUTION_OUTCOME[result["kind"]]
    )


def validate_evidence_ledger(result: dict[str, Any], errors: list[str]) -> None:
    result_id = result.get("result_id")
    seen: dict[str, dict[str, Any]] = {}
    for item in result.get("evidence", []):
        evidence_id = item.get("evidence_id")
        if evidence_id in seen:
            errors.append(f"{result_id}: 重复 evidence_id {evidence_id}")
        for invalidated_id in item.get("invalidates", []):
            if item.get("verdict") != "reject":
                errors.append(
                    f"{result_id}: 只有 verdict=reject 的受信证据可以执行失效：{evidence_id}"
                )
            if invalidated_id == evidence_id:
                errors.append(f"{result_id}: 证据不能使自身失效：{evidence_id}")
            elif invalidated_id not in seen:
                errors.append(
                    f"{result_id}: 只能使账本中更早的证据失效：{invalidated_id}"
                )
            elif seen[invalidated_id].get("capability") != item.get("capability"):
                errors.append(
                    f"{result_id}: 失效记录只能撤销同 capability 证据：{invalidated_id}"
                )
        if isinstance(evidence_id, str):
            seen[evidence_id] = item


def validate_cross_references(
    problems: list[dict[str, Any]],
    problem_ids: set[str],
    attempts: list[dict[str, Any]],
    attempt_ids: set[str],
    results: list[dict[str, Any]],
    errors: list[str],
    *,
    project_root: Path = ROOT,
) -> None:
    source_record_ids = load_source_record_ids(project_root)
    problems_by_id = {
        problem["problem_id"]: problem
        for problem in problems
        if isinstance(problem.get("problem_id"), str)
    }
    for problem in problems:
        for source in problem.get("sources", []):
            source_record_id = source.get("source_record_id")
            if source_record_ids and source_record_id and source_record_id not in source_record_ids:
                errors.append(
                    f"{problem.get('problem_id')}: 引用不存在的来源记录 {source_record_id}"
                )

    attempts_by_id = {
        attempt["attempt_id"]: attempt
        for attempt in attempts
        if isinstance(attempt.get("attempt_id"), str)
    }
    attempt_counts: dict[str, int] = {}
    for attempt in attempts:
        attempt_id = attempt.get("attempt_id")
        problem_id = attempt.get("problem_id")
        if problem_id not in problem_ids:
            errors.append(
                f"{attempt_id}: 引用不存在的 Problem {problem_id}"
            )
        else:
            problem = problems_by_id[problem_id]
            constraints = problem.get("constraints", {})
            allowed_methods = constraints.get("allowed_methods", [])
            if attempt.get("method") not in allowed_methods:
                errors.append(
                    f"{attempt_id}: method={attempt.get('method')} 未被 ProblemContract 允许"
                )
            attempt_counts[problem_id] = attempt_counts.get(problem_id, 0) + 1
            max_attempts = constraints.get("max_attempts")
            if isinstance(max_attempts, int) and attempt_counts[problem_id] > max_attempts:
                errors.append(
                    f"{problem_id}: Attempt 数量超过 ProblemContract.max_attempts={max_attempts}"
                )
            if problem.get("lifecycle") == "draft":
                errors.append(
                    f"{attempt_id}: draft ProblemContract 不允许存在 Attempt"
                )
        completed_at = attempt.get("completed_at")
        if attempt.get("lifecycle") in {"completed", "blocked", "failed"} and completed_at is None:
            errors.append(f"{attempt_id}: 终态 Attempt 缺少 completed_at")
        if attempt.get("lifecycle") in {"planned", "running"} and completed_at is not None:
            errors.append(f"{attempt_id}: 非终态 Attempt 不应设置 completed_at")

    admitted_kinds: dict[str, set[str]] = {}
    for result in results:
        result_id = result.get("result_id")
        kind = result.get("kind")
        outcome = result.get("outcome")
        if result.get("problem_id") not in problem_ids:
            errors.append(f"{result_id}: 引用不存在的 Problem {result.get('problem_id')}")
        attempt_id = result.get("attempt_id")
        if attempt_id not in attempt_ids:
            errors.append(f"{result_id}: 引用不存在的 Attempt {result.get('attempt_id')}")
        else:
            attempt = attempts_by_id[attempt_id]
            if result.get("problem_id") != attempt.get("problem_id"):
                errors.append(
                    f"{result_id}: Result 与 Attempt 必须引用同一个 Problem"
                )
            generator = attempt.get("generator")
            for item in result.get("evidence", []):
                if (
                    item.get("verdict") == "accept"
                    and item.get("independent") is True
                    and item.get("verifier") == generator
                ):
                    errors.append(
                        f"{result_id}: 独立证据的 verifier 不能等于 Attempt.generator"
                    )
        if kind in ALLOWED_OUTCOMES and outcome not in ALLOWED_OUTCOMES[kind]:
            errors.append(f"{result_id}: {kind} 不允许 outcome={outcome}")

        validate_evidence_ledger(result, errors)
        qualified = qualifies_as_solution(
            result,
            attempts_by_id,
            project_root=project_root,
            errors=errors,
        )
        expected_outcome = EXPECTED_SOLUTION_OUTCOME.get(kind)
        if qualified and outcome != expected_outcome:
            errors.append(
                f"{result_id}: 当前有效证据已满足完整解条件，outcome 必须是 {expected_outcome}"
            )
        if outcome in {"established", "refuted"} and not qualified:
            errors.append(
                f"{result_id}: outcome={outcome} 缺少独立直接验证、适用的 axiom/escape audit 或 statement faithfulness 证据"
            )
        if kind in NON_CLOSING_KINDS and outcome in {"established", "refuted"}:
            errors.append(f"{result_id}: {kind} 不能成为原问题的完整结论")
        if qualified and outcome == EXPECTED_SOLUTION_OUTCOME.get(kind):
            admitted_kinds.setdefault(result.get("problem_id"), set()).add(kind)

    for problem_id, kinds in admitted_kinds.items():
        if {"proof", "counterexample"}.issubset(kinds):
            errors.append(
                f"{problem_id}: 同时存在通过准入的 proof 与 counterexample，必须先解决契约或验证链冲突"
            )


def write_solution_index(solution_ids: list[str]) -> None:
    rebuilt = ResearchStore(ROOT).rebuild_solution_view()
    if rebuilt != solution_ids:
        raise ValueError("唯一 writer 重算结果与 validator 预期不一致")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Vibe Mathing 研究空间")
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="按当前 Result 重写完整解派生索引",
    )
    args = parser.parse_args()

    required_paths = [
        PROBLEMS_PATH,
        PROBLEM_SCHEMA_PATH,
        ATTEMPTS_PATH,
        ATTEMPT_SCHEMA_PATH,
        RESULTS_PATH,
        RESULT_SCHEMA_PATH,
        SOLUTIONS_PATH,
        VERIFIER_REGISTRY_PATH,
        VERIFIER_SCHEMA_PATH,
        RECEIPT_SCHEMA_PATH,
        ROOT / "research" / "schema" / "obligation-graph.schema.json",
        ROOT / "research" / "schema" / "candidate-artifact.schema.json",
        ROOT / "research" / "schema" / "evidence-link.schema.json",
        ROOT / "research" / "schema" / "semantic-review.schema.json",
    ]
    missing = [path.relative_to(ROOT) for path in required_paths if not path.is_file()]
    if missing:
        for path in missing:
            print(f"ERROR: 缺少必需文件：{path}", file=sys.stderr)
        return 1

    errors: list[str] = []
    try:
        load_verifier_registry(ROOT)
        Draft202012Validator.check_schema(load_json(RECEIPT_SCHEMA_PATH))
        problems, problem_ids = validate_records(
            PROBLEMS_PATH, PROBLEM_SCHEMA_PATH, "problem_id", errors
        )
        attempts, attempt_ids = validate_records(
            ATTEMPTS_PATH, ATTEMPT_SCHEMA_PATH, "attempt_id", errors
        )
        results, _ = validate_records(
            RESULTS_PATH, RESULT_SCHEMA_PATH, "result_id", errors
        )
        errors.extend(
            f"Obligation harness：{error}"
            for error in validate_obligation_records(ROOT)
        )
        validate_cross_references(
            problems, problem_ids, attempts, attempt_ids, results, errors
        )
        attempts_by_id = {
            attempt["attempt_id"]: attempt
            for attempt in attempts
            if isinstance(attempt.get("attempt_id"), str)
        }
        expected_solution_ids = derive_solution_ids(results, attempts_by_id)
        if args.write_index and not errors:
            write_solution_index(expected_solution_ids)
        index = load_json(SOLUTIONS_PATH)
        if index.get("schema_version") != "2.0.0":
            errors.append("solutions.json schema_version 必须为 2.0.0")
        if index.get("result_ids") != expected_solution_ids:
            errors.append(
                "solutions.json 与当前 Result 派生结果不一致；运行 "
                "python3 scripts/validate_research_spaces.py --write-index"
            )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"研究空间校验失败：{len(errors)} 个问题。", file=sys.stderr)
        return 1

    print(
        "研究空间校验通过："
        f"Problem {len(problems)}；Attempt {len(attempts)}；"
        f"Result {len(results)}；Solution {len(expected_solution_ids)}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
