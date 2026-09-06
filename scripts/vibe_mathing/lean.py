"""固定 Lean/Mathlib fixture 的 kernel、逃逸和公理审计 adapter。"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .evidence import create_evidence_receipt
from .runtime import execute_bounded, now


ESCAPE_PATTERN = re.compile(r"\b(?:sorry|admit|unsafe)\b")
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.33.0"
EXPECTED_VERSION_FRAGMENT = "version 4.33.0"
EXPECTED_MATHLIB_REV = "db584cd6d46c92f209a44c0f1c829460d327499d"
EXPECTED_DECLARATION = "theorem two_add_two : (2 : ℕ) + 2 = 4"
EXPECTED_AXIOM_AUDIT = "#print axioms VibeMathingFixture.two_add_two"


def _resolve_tool(name: str) -> str:
    """从 PATH 或 elan 官方默认目录解析 Lean 工具，不修改进程环境。"""
    resolved = shutil.which(name)
    if resolved:
        return resolved
    elan_tool = Path.home() / ".elan" / "bin" / name
    if elan_tool.is_file() and os.access(elan_tool, os.X_OK):
        return str(elan_tool)
    raise RuntimeError(
        f"找不到 {name}；请安装 elan/Lean，或将 ~/.elan/bin 加入 PATH"
    )


def _write_output(project_root: Path, run_key: str, name: str, payload: dict[str, Any]) -> str:
    relative = f"research/artifacts/outputs/{run_key}/{name}.json"
    path = project_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path.is_file():
        if path.read_text(encoding="utf-8") != encoded:
            raise RuntimeError(f"Lean verifier 输出已存在且内容不同：{relative}")
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


def verify_lean_fixture(
    *, project_root: Path, fixture_root: Path, result: dict[str, Any]
) -> list[dict[str, Any]]:
    """运行真实 Lean 命令并返回可被 Result 消费的三类证据。"""
    source = fixture_root / "VibeMathingFixture.lean"
    axiom_audit = fixture_root / "AxiomAudit.lean"
    toolchain = (fixture_root / "lean-toolchain").read_text(encoding="utf-8").strip()
    lakefile = (fixture_root / "lakefile.toml").read_text(encoding="utf-8")
    manifest = json.loads((fixture_root / "lake-manifest.json").read_text(encoding="utf-8"))
    source_text = source.read_text(encoding="utf-8")
    axiom_audit_text = axiom_audit.read_text(encoding="utf-8")
    mathlib_revisions = {
        item.get("rev") for item in manifest.get("packages", []) if item.get("name") == "mathlib"
    }
    if (
        toolchain != EXPECTED_TOOLCHAIN
        or EXPECTED_MATHLIB_REV not in lakefile
        or mathlib_revisions != {EXPECTED_MATHLIB_REV}
        or EXPECTED_AXIOM_AUDIT not in axiom_audit_text
    ):
        raise RuntimeError("Lean/Mathlib 固定版本契约漂移")
    escapes = ESCAPE_PATTERN.findall(source_text)
    declaration_match = EXPECTED_DECLARATION in source_text
    budgets = {"timeout_seconds": 600, "max_output_bytes": 2_000_000}
    lake = _resolve_tool("lake")
    version = execute_bounded(
        [lake, "env", "lean", "--version"], cwd=fixture_root, **budgets
    )
    build = execute_bounded([lake, "--quiet", "build"], cwd=fixture_root, **budgets)
    axioms = execute_bounded(
        [lake, "env", "lean", "AxiomAudit.lean"],
        cwd=fixture_root,
        **budgets,
    )
    version_text = version["stdout"] + version["stderr"]
    if (
        version["exit_code"] != 0
        or EXPECTED_VERSION_FRAGMENT not in version_text
        or build["exit_code"] != 0
        or axioms["exit_code"] != 0
    ):
        raise RuntimeError("Lean 工具链或 fixture 构建失败")
    axiom_text = axioms["stdout"] + axioms["stderr"]
    axiom_clean = "does not depend on any axioms" in axiom_text
    run_key = result["result_id"].removeprefix("result:")
    kernel_locator = _write_output(
        project_root,
        run_key,
        "lean-kernel",
        {"toolchain": toolchain, "version": version, "build": build},
    )
    audit_locator = _write_output(
        project_root,
        run_key,
        "lean-axiom-audit",
        {"escapes": escapes, "axiom_output": axiom_text, "axiom_clean": axiom_clean},
    )
    faithfulness_locator = _write_output(
        project_root,
        run_key,
        "lean-statement-faithfulness",
        {"expected_declaration": EXPECTED_DECLARATION, "match": declaration_match},
    )
    checked_at = now()
    return [
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.kernel",
            capability="kernel_check",
            verdict="accept",
            verifier="lean-kernel",
            checked_at=checked_at,
            output_locator=kernel_locator,
            command=[lake, "--quiet", "build"],
            notes="固定 Lean/Mathlib 的真实 kernel build",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.axioms",
            capability="axiom_escape_audit",
            verdict="accept" if not escapes and axiom_clean else "reject",
            verifier="lean-axiom-auditor",
            checked_at=checked_at,
            output_locator=audit_locator,
            command=[lake, "env", "lean", "AxiomAudit.lean"],
            notes="源码逃逸扫描与已编译模块上的 #print axioms",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.faithfulness",
            capability="statement_faithfulness",
            verdict="accept" if declaration_match else "reject",
            verifier="lean-faithfulness-reviewer",
            checked_at=checked_at,
            output_locator=faithfulness_locator,
            command=["vibe-mathing", "verify-lean-statement-contract"],
            executor="in_process",
            notes="fixture 陈述与固定 Problem Contract 对应",
        ),
    ]
