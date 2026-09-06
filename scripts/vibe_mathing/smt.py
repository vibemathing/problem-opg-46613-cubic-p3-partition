"""固定 SymPy SAT/QF-LRA fixture 的有限 theory verifier。"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.logic.inference import satisfiable

from .evidence import create_evidence_receipt
from .runtime import now


EXPECTED_SYMPY_VERSION = "1.14.0"
EXPECTED_STATEMENT = "对所有实数 x，若 0 <= x <= 1，则 x <= 0。"
BACKEND = "sympy-1.14-sat-qf-lra"


def _write_output(
    project_root: Path, run_key: str, name: str, payload: dict[str, Any]
) -> str:
    relative = f"research/artifacts/outputs/{run_key}/{name}.json"
    path = project_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path.is_file():
        if path.read_text(encoding="utf-8") != encoded:
            raise RuntimeError(f"SMT verifier 输出已存在且内容不同：{relative}")
        return relative
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


def _serialize_model(model: dict[Any, Any] | bool) -> dict[str, bool] | bool:
    if model is False:
        return False
    return {str(key): bool(value) for key, value in sorted(model.items(), key=lambda item: str(item[0]))}


def verify_smt_fixture(
    *,
    project_root: Path,
    fixture_root: Path,
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    """验证固定命题 SAT、QF-LRA 与精确 witness，返回两类独立证据。"""
    if sp.__version__ != EXPECTED_SYMPY_VERSION:
        raise RuntimeError(
            f"SymPy 版本漂移：expected={EXPECTED_SYMPY_VERSION} actual={sp.__version__}"
        )
    try:
        fixture = json.loads((fixture_root / "case.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("无法读取 SMT/LRA fixture") from exc
    statement = fixture.get("statement")
    witness_spec = fixture.get("witness", {})
    if (
        fixture.get("schema_version") != "1.0.0"
        or statement != EXPECTED_STATEMENT
        or not isinstance(witness_spec.get("numerator"), int)
        or not isinstance(witness_spec.get("denominator"), int)
        or witness_spec["denominator"] == 0
    ):
        raise RuntimeError("SMT/LRA fixture 契约漂移")

    p, q = sp.symbols("p q", boolean=True)
    propositional_sat = satisfiable(
        sp.And(sp.Or(p, q), sp.Or(sp.Not(p), q), sp.Or(p, sp.Not(q))),
        algorithm="dpll2",
    )
    propositional_unsat = satisfiable(sp.And(p, sp.Not(p)), algorithm="dpll2")

    x = sp.symbols("x", real=True)
    lra_formula = sp.And(x >= 0, x <= 1, x > 0)
    lra_contradiction = sp.And(x > 1, x < 0)
    lra_sat = satisfiable(lra_formula, use_lra_theory=True)
    lra_unsat = satisfiable(lra_contradiction, use_lra_theory=True)
    witness = sp.Rational(witness_spec["numerator"], witness_spec["denominator"])
    exact_witness_ok = bool(witness >= 0 and witness <= 1 and witness > 0)
    counterexample_ok = bool(
        propositional_sat is not False
        and propositional_unsat is False
        and lra_sat is not False
        and lra_unsat is False
        and exact_witness_ok
    )
    faithfulness_ok = statement == EXPECTED_STATEMENT
    run_key = result["result_id"].removeprefix("result:")
    solver_locator = _write_output(
        project_root,
        run_key,
        "smt-counterexample",
        {
            "backend": BACKEND,
            "sympy_version": sp.__version__,
            "propositional_sat": _serialize_model(propositional_sat),
            "propositional_unsat": propositional_unsat is False,
            "qf_lra_formula": str(lra_formula),
            "qf_lra_sat": _serialize_model(lra_sat),
            "qf_lra_contradiction_unsat": lra_unsat is False,
            "witness": str(witness),
            "exact_witness_ok": exact_witness_ok,
            "verdict": "accept" if counterexample_ok else "reject",
        },
    )
    faithfulness_locator = _write_output(
        project_root,
        run_key,
        "smt-statement-faithfulness",
        {
            "expected": EXPECTED_STATEMENT,
            "actual": statement,
            "match": faithfulness_ok,
        },
    )
    checked_at = now()
    return [
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="smt-generator",
            evidence_id=f"evidence:{run_key}.smt-counterexample",
            capability="counterexample_check",
            verdict="accept" if counterexample_ok else "reject",
            verifier="sympy-smt-verifier",
            checked_at=checked_at,
            output_locator=solver_locator,
            command=["internal-verifier", BACKEND],
            executor="in_process",
            notes="SymPy 命题 SAT、QF-LRA 与精确有理数 witness 复核",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="smt-generator",
            evidence_id=f"evidence:{run_key}.faithfulness",
            capability="statement_faithfulness",
            verdict="accept" if faithfulness_ok else "reject",
            verifier="smt-statement-faithfulness-verifier",
            checked_at=checked_at,
            output_locator=faithfulness_locator,
            command=["internal-verifier", "smt-statement-fixture-v1"],
            executor="in_process",
            notes="固定 SMT fixture 的陈述逐字契约",
        ),
    ]
