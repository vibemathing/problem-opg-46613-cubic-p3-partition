"""从三张事实表的一致快照确定性派生 ResearchBundle。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .obligations import (
    ObligationError,
    derive_obligation_closure,
    load_obligation_state,
)
from .store import ResearchStore


class BundleError(RuntimeError):
    """ResearchBundle 无法安全派生。"""


class BundleConflict(BundleError):
    """同一问题同时存在已准入的证明和反例。"""


def _validate_bundle(project_root: Path, bundle: dict[str, Any]) -> None:
    schema_path = project_root / "research/schema/research-bundle.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BundleError(f"无法读取 ResearchBundle schema：{schema_path}") from exc
    errors = sorted(Draft202012Validator(schema).iter_errors(bundle), key=lambda item: list(item.path))
    if errors:
        raise BundleError(f"ResearchBundle schema 无效：{errors[0].message}")


def _derive_from_snapshot(
    project_root: Path,
    problem_id: str,
    snapshot: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    from validate_research_spaces import (
        EXPECTED_SOLUTION_OUTCOME,
        accepted_independent_capabilities,
        has_direct_solution_evidence,
        qualifies_as_solution,
    )

    problem = next(
        (item for item in snapshot["problems"] if item["problem_id"] == problem_id),
        None,
    )
    if problem is None:
        raise BundleError(f"Problem 不存在：{problem_id}")

    attempts = sorted(
        (item for item in snapshot["attempts"] if item["problem_id"] == problem_id),
        key=lambda item: item["attempt_id"],
    )
    attempt_ids = {item["attempt_id"] for item in attempts}
    attempts_by_id = {item["attempt_id"]: item for item in attempts}
    results = sorted(
        (
            item
            for item in snapshot["results"]
            if item["problem_id"] == problem_id and item["attempt_id"] in attempt_ids
        ),
        key=lambda item: item["result_id"],
    )
    admitted = [
        item
        for item in results
        if qualifies_as_solution(item, attempts_by_id, project_root=project_root)
        and item["outcome"] == EXPECTED_SOLUTION_OUTCOME[item["kind"]]
    ]
    admitted_kinds = {item["kind"] for item in admitted}
    if {"proof", "counterexample"}.issubset(admitted_kinds):
        raise BundleConflict(
            f"{problem_id}: 同时存在通过准入的 proof 与 counterexample"
        )
    disposition = (
        "solved"
        if "proof" in admitted_kinds
        else "refuted"
        if "counterexample" in admitted_kinds
        else "open"
    )

    obligations: list[dict[str, Any]] = []
    if disposition == "open":
        closing_candidates = [
            item for item in results if item["kind"] in {"proof", "counterexample"}
        ]
        if not closing_candidates:
            obligations.append(
                {"code": "no_closing_candidate", "result_id": None, "missing": []}
            )
        for result in closing_candidates:
            attempt = attempts_by_id[result["attempt_id"]]
            capabilities = accepted_independent_capabilities(
                result,
                attempt["generator"],
                project_root=project_root,
            )
            missing: list[str] = []
            if not has_direct_solution_evidence(result["kind"], capabilities):
                missing.append("direct_solution_evidence")
            if "statement_faithfulness" not in capabilities:
                missing.append("statement_faithfulness")
            if result["outcome"] != EXPECTED_SOLUTION_OUTCOME[result["kind"]]:
                missing.append("expected_outcome")
            obligations.append(
                {
                    "code": "incomplete_closing_candidate",
                    "result_id": result["result_id"],
                    "missing": sorted(missing),
                }
            )

    evidence = sorted(
        (
            {"result_id": result["result_id"], "receipt": receipt}
            for result in results
            for receipt in result["evidence"]
        ),
        key=lambda item: (item["result_id"], item["receipt"]["evidence_id"]),
    )
    try:
        obligation_state = load_obligation_state(project_root)
        obligation_graphs: list[dict[str, Any]] = []
        for graph_id in sorted(set(obligation_state["current_graph_by_attempt"].values())):
            graph = obligation_state["graphs"][graph_id]
            if graph["problem_id"] != problem_id:
                continue
            closure = derive_obligation_closure(
                project_root,
                graph_id,
                state=obligation_state,
            )
            if closure["conflicting_obligation_ids"]:
                raise BundleConflict(
                    f"{problem_id}: ObligationGraph 同时闭合 proof 与 counterexample"
                )
            obligation_graphs.append(
                {
                    "graph": graph,
                    "candidates": sorted(
                        (
                            candidate
                            for candidate in obligation_state["candidates"].values()
                            if candidate["graph_id"] == graph_id
                        ),
                        key=lambda item: item["candidate_id"],
                    ),
                    "evidence_links": sorted(
                        (
                            link
                            for link in obligation_state["links"]
                            if link["graph_id"] == graph_id
                        ),
                        key=lambda item: item["evidence_link_id"],
                    ),
                    "closure": closure,
                }
            )
    except ObligationError as exc:
        raise BundleError(f"ObligationGraph 无法派生：{exc}") from exc
    bundle = {
        "schema_version": "1.0.0",
        "problem": problem,
        "attempts": attempts,
        "results": results,
        "evidence": evidence,
        "obligation_graphs": obligation_graphs,
        "disposition": disposition,
        "solution_view": sorted(item["result_id"] for item in admitted),
        "unresolved_obligations": obligations,
    }
    _validate_bundle(project_root, bundle)
    return bundle


def derive_research_bundle(project_root: Path, problem_id: str) -> dict[str, Any]:
    """读取一个已校验的一致快照并派生单个问题的响应视图。"""
    root = project_root.resolve()
    return _derive_from_snapshot(root, problem_id, ResearchStore(root).snapshot())
