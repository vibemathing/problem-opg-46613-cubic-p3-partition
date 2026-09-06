"""确定性 SymPy 候选生成、独立验证与 Result 晋升流水线。"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from sympy import Rational

from .evidence import create_evidence_receipt
from .runtime import InjectedInterruption, create_run, locked_run, now, stable_run_id, transition
from .store import ResearchStore, StoreError


SYMPY_ADAPTER = "sympy-counterexample-v1"
EXPECTED_STATEMENT = "对所有实数 x，x^2 >= x。"


def _artifact(project_root: Path, run_id: str, name: str, payload: dict[str, Any]) -> str:
    relative = f"research/artifacts/outputs/{run_id.removeprefix('run:')}/{name}.json"
    path = project_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path.is_file() and path.read_text(encoding="utf-8") == encoded:
        return relative
    if path.is_file():
        raise StoreError(f"确定性 artifact 内容漂移：{relative}")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return relative


def _problem(store: ResearchStore, problem_id: str) -> dict[str, Any]:
    for item in store.read("problems"):
        if item["problem_id"] == problem_id:
            return item
    raise StoreError(f"Problem 不存在：{problem_id}")


def run_sympy_pipeline(
    project_root: Path,
    problem_id: str,
    *,
    fail_after: str | None = None,
) -> dict[str, Any]:
    run_id = stable_run_id(problem_id, SYMPY_ADAPTER)
    with locked_run(project_root, run_id):
        return _run_sympy_pipeline_locked(
            project_root, problem_id, fail_after=fail_after
        )


def _run_sympy_pipeline_locked(
    project_root: Path,
    problem_id: str,
    *,
    fail_after: str | None,
) -> dict[str, Any]:
    store = ResearchStore(project_root)
    problem = _problem(store, problem_id)
    if problem["lifecycle"] != "active":
        raise StoreError("只有 lifecycle=active 的 ProblemContract 可以运行")
    constraints = problem["constraints"]
    if SYMPY_ADAPTER not in constraints["allowed_adapters"]:
        raise StoreError(f"ProblemContract 未允许 adapter={SYMPY_ADAPTER}")
    if "computation" not in constraints["allowed_methods"]:
        raise StoreError("ProblemContract 未允许 computation 研究方法")
    state = create_run(
        project_root,
        problem_id,
        SYMPY_ADAPTER,
        budgets=constraints["runtime"],
    )
    if state["status"] in {"accepted", "rejected"}:
        if state["status"] == "accepted":
            run_suffix = state["run_id"].removeprefix("run:")
            result_id = f"result:{run_suffix}"
            if result_id not in store.rebuild_solution_view():
                raise StoreError(
                    f"运行曾被接受，但当前 Result 已失效：{result_id}"
                )
        return state
    if problem["statement"]["text"] != EXPECTED_STATEMENT:
        raise StoreError("SymPy fixture adapter 拒绝未注册的问题陈述")
    if state["status"] == "planned":
        state = transition(project_root, state, "routed")
    if state["status"] == "routed":
        state = transition(project_root, state, "running")
    run_suffix = state["run_id"].removeprefix("run:")
    attempt_id = f"attempt:{run_suffix}"
    result_id = f"result:{run_suffix}"
    existing_attempts = [
        item for item in store.read("attempts") if item["problem_id"] == problem_id
    ]
    if not any(item["attempt_id"] == attempt_id for item in existing_attempts) and len(
        existing_attempts
    ) >= constraints["max_attempts"]:
        raise StoreError("ProblemContract 的 max_attempts 预算耗尽")
    if state["status"] == "running":
        candidate_locator = _artifact(
            project_root,
            state["run_id"],
            "candidate",
            {"candidate": {"x": "1/2"}, "claim": "x^2 < x"},
        )
        started = state["created_at"]
        attempt = {
            "attempt_id": attempt_id,
            "problem_id": problem_id,
            "generator": "sympy-generator",
            "objective": "寻找全称命题的精确反例",
            "method": "computation",
            "lifecycle": "completed",
            "started_at": started,
            "completed_at": started,
            "inputs": [problem_id],
            "claims": ["x=1/2 是候选反例"],
            "artifacts": [candidate_locator],
        }
        store.upsert("attempts", attempt)
        state = transition(project_root, state, "candidate_ready")
        if fail_after == "candidate_ready":
            raise InjectedInterruption("故障注入：candidate_ready")
    if state["status"] == "candidate_ready":
        state = transition(project_root, state, "verifying")
    if state["status"] == "verifying":
        verification_at = state["updated_at"]
        x = Rational(1, 2)
        counterexample_ok = x**2 < x
        check_locator = _artifact(
            project_root,
            state["run_id"],
            "counterexample-check",
            {"x": str(x), "x_squared": str(x**2), "x_squared_lt_x": bool(counterexample_ok)},
        )
        faithfulness_ok = problem["statement"]["text"] == EXPECTED_STATEMENT
        faithfulness_locator = _artifact(
            project_root,
            state["run_id"],
            "statement-faithfulness",
            {"expected": EXPECTED_STATEMENT, "actual": problem["statement"]["text"], "match": faithfulness_ok},
        )
        result = {
            "result_id": result_id,
            "problem_id": problem_id,
            "attempt_id": attempt_id,
            "kind": "counterexample",
            "claim": "x=1/2 时 x^2=1/4<1/2，因此原全称命题为假。",
            "scope": "实数域上的精确有理数反例",
            "outcome": "refuted",
            "evidence": [],
            "created_at": verification_at,
        }
        if not (counterexample_ok and faithfulness_ok):
            result["outcome"] = "inconclusive"
        result["evidence"] = [
            create_evidence_receipt(
                project_root=project_root,
                result=result,
                generator="sympy-generator",
                evidence_id=f"evidence:{run_suffix}.counterexample",
                capability="counterexample_check",
                verdict="accept" if counterexample_ok else "reject",
                verifier="sympy-counterexample-verifier",
                checked_at=verification_at,
                output_locator=check_locator,
                command=["internal-verifier", "sympy-exact-rational-v1"],
                executor="in_process",
                notes="SymPy exact Rational 独立复算",
            ),
            create_evidence_receipt(
                project_root=project_root,
                result=result,
                generator="sympy-generator",
                evidence_id=f"evidence:{run_suffix}.faithfulness",
                capability="statement_faithfulness",
                verdict="accept" if faithfulness_ok else "reject",
                verifier="statement-faithfulness-verifier",
                checked_at=verification_at,
                output_locator=faithfulness_locator,
                command=["internal-verifier", "fixture-statement-contract-v1"],
                executor="in_process",
                notes="固定 fixture 的陈述逐字契约",
            ),
        ]
        store.upsert("results", result)
        if fail_after == "result_written":
            raise InjectedInterruption("故障注入：result_written")
        solution_ids = store.rebuild_solution_view()
        state = transition(
            project_root,
            state,
            "accepted" if result_id in solution_ids else "rejected",
        )
    return state


def invalidate_sympy_result(project_root: Path, run_id: str) -> list[str]:
    store = ResearchStore(project_root)
    result_id = f"result:{run_id.removeprefix('run:')}"
    result = next(item for item in store.read("results") if item["result_id"] == result_id)
    invalidation_id = f"evidence:{run_id.removeprefix('run:')}.invalidation"
    if any(item["evidence_id"] == invalidation_id for item in result["evidence"]):
        return store.rebuild_solution_view()
    target = result["evidence"][0]["evidence_id"]
    invalidation_locator = _artifact(
        project_root,
        run_id,
        "invalidation",
        {"invalidates": [target], "reason": "regression-test"},
    )
    result["evidence"].append(
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="sympy-generator",
            evidence_id=invalidation_id,
            capability="counterexample_check",
            verdict="reject",
            verifier="sympy-counterexample-verifier",
            checked_at=now(),
            output_locator=invalidation_locator,
            command=["internal-verifier", "append-only-invalidation-v1"],
            executor="in_process",
            notes="append-only 失效记录",
            invalidates=[target],
        )
    )
    result["outcome"] = "withdrawn"
    store.replace_result(result)
    return store.rebuild_solution_view()
