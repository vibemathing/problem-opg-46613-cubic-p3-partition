"""可信证据产物、回执和 verifier registry 的唯一实现。"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


MAX_VERIFIER_JSON_BYTES = 2_000_000


class EvidenceError(ValueError):
    """证据无法在当前信任策略下成立。"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _trusted_file(project_root: Path, locator: str) -> Path:
    if not locator or Path(locator).is_absolute():
        raise EvidenceError("证据 locator 必须是非空仓库相对路径")
    relative = Path(locator)
    if ".." in relative.parts:
        raise EvidenceError("证据 locator 禁止路径逃逸")
    if relative.parts[:2] != ("research", "artifacts"):
        raise EvidenceError(f"证据文件不在可信根：{locator}")
    resolved_project_root = project_root.resolve()
    trusted_root = resolved_project_root / "research" / "artifacts"
    if trusted_root.is_symlink():
        raise EvidenceError("可信证据根不能是 symlink")
    lexical = resolved_project_root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise EvidenceError(f"可信证据路径禁止 symlink：{locator}")
    candidate = resolved_project_root / relative
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise EvidenceError(f"证据文件不存在：{locator}") from exc
    try:
        resolved.relative_to(trusted_root)
    except ValueError as exc:
        raise EvidenceError(f"证据文件不在可信根：{locator}") from exc
    if not resolved.is_file():
        raise EvidenceError(f"证据 locator 不是普通文件：{locator}")
    return resolved


def load_verifier_registry(project_root: Path) -> dict[str, dict[str, Any]]:
    path = project_root / "research" / "verifiers.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"无法读取 verifier registry：{path}") from exc
    _validate_schema(
        project_root / "research" / "schema" / "verifier-registry.schema.json",
        payload,
        "verifier registry",
    )
    entries: dict[str, dict[str, Any]] = {}
    for entry in payload.get("principals", []):
        principal_id = entry.get("id")
        if not isinstance(principal_id, str) or not principal_id or principal_id in entries:
            raise EvidenceError("verifier registry 含无效或重复 principal ID")
        if entry.get("role") not in {"generator", "verifier"}:
            raise EvidenceError(f"{principal_id}: role 无效")
        if not isinstance(entry.get("trust_domain"), str) or not entry["trust_domain"]:
            raise EvidenceError(f"{principal_id}: 缺少 trust_domain")
        capabilities = entry.get("capabilities")
        if not isinstance(capabilities, list) or not all(
            isinstance(item, str) and item for item in capabilities
        ):
            raise EvidenceError(f"{principal_id}: capabilities 无效")
        if entry["role"] == "verifier" and not isinstance(entry.get("policy"), str):
            raise EvidenceError(f"{principal_id}: verifier 缺少 policy")
        if entry["role"] == "generator" and entry.get("policy") is not None:
            raise EvidenceError(f"{principal_id}: generator 不应声明 verifier policy")
        entries[principal_id] = entry
    return entries


def _validate_schema(schema_path: Path, value: dict[str, Any], label: str) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"无法读取 {label} schema：{schema_path}") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
        key=lambda item: list(item.path),
    )
    if errors:
        raise EvidenceError(f"{label} schema 无效：{errors[0].message}")


def _load_output_json(path: Path) -> dict[str, Any]:
    if path.stat().st_size > MAX_VERIFIER_JSON_BYTES:
        raise EvidenceError("verifier JSON 输出超过 2 MiB 上限")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError("verifier 输出必须是有效 JSON") from exc
    if not isinstance(payload, dict):
        raise EvidenceError("verifier 输出必须是 JSON object")
    return payload


def _validate_output_policy(
    *,
    policy: str,
    output_path: Path,
    verdict: str,
    capability: str,
    invalidates: list[str],
) -> None:
    output = _load_output_json(output_path)
    if verdict != "accept":
        if invalidates:
            if output.get("invalidates") != invalidates:
                raise EvidenceError("verifier 输出与回执 invalidates 不一致")
        elif output.get("verdict") != verdict:
            raise EvidenceError("非 accept 输出缺少对应 verdict")
        return
    valid = False
    if policy == "sympy-counterexample-fixture-v1":
        valid = output == {
            "x": "1/2",
            "x_squared": "1/4",
            "x_squared_lt_x": True,
        }
    elif policy == "sympy-statement-fixture-v1":
        valid = (
            output.get("expected") == "对所有实数 x，x^2 >= x。"
            and output.get("actual") == output.get("expected")
            and output.get("match") is True
        )
    elif policy == "sympy-smt-counterexample-fixture-v1":
        valid = (
            output.get("backend") == "sympy-1.14-sat-qf-lra"
            and output.get("sympy_version") == "1.14.0"
            and isinstance(output.get("propositional_sat"), dict)
            and bool(output["propositional_sat"])
            and output.get("propositional_unsat") is True
            and isinstance(output.get("qf_lra_sat"), dict)
            and bool(output["qf_lra_sat"])
            and output.get("qf_lra_contradiction_unsat") is True
            and output.get("witness") == "1/2"
            and output.get("exact_witness_ok") is True
            and output.get("verdict") == "accept"
        )
    elif policy == "smt-statement-fixture-v1":
        valid = (
            output.get("expected")
            == "对所有实数 x，若 0 <= x <= 1，则 x <= 0。"
            and output.get("actual") == output.get("expected")
            and output.get("match") is True
        )
    elif policy == "lean-kernel-fixture-v1":
        version = output.get("version", {})
        build = output.get("build", {})
        valid = (
            output.get("toolchain") == "leanprover/lean4:v4.33.0"
            and version.get("exit_code") == 0
            and "version 4.33.0" in version.get("stdout", "")
            and build.get("exit_code") == 0
        )
    elif policy == "lean-axiom-fixture-v1":
        valid = (
            output.get("escapes") == []
            and output.get("axiom_clean") is True
            and "does not depend on any axioms" in output.get("axiom_output", "")
        )
    elif policy == "lean-statement-fixture-v1":
        valid = (
            output.get("expected_declaration")
            == "theorem two_add_two : (2 : ℕ) + 2 = 4"
            and output.get("match") is True
        )
    elif policy == "lean-obligation-kernel-v1":
        valid = (
            output.get("capability") == "kernel_check"
            and output.get("verdict") == "accept"
            and output.get("native_status") == "accepted"
            and output.get("toolchain_admission_status") == "admitted"
            and output.get("build", {}).get("exit_code") == 0
            and output.get("axiom_command", {}).get("exit_code") == 0
        )
    elif policy == "lean-obligation-axiom-v1":
        valid = (
            output.get("capability") == "axiom_escape_audit"
            and output.get("verdict") == "accept"
            and output.get("native_status") == "accepted"
            and output.get("toolchain_admission_status") == "admitted"
            and output.get("escapes") == []
            and output.get("unauthorized_axioms") == []
            and output.get("axiom_parse_status") == "parsed"
        )
    elif policy == "lean-obligation-statement-v1":
        valid = (
            output.get("capability") == "statement_identity"
            and output.get("verdict") == "accept"
            and output.get("native_status") == "accepted"
            and output.get("toolchain_admission_status") == "admitted"
            and output.get("declaration_identity") is True
            and output.get("statement_sha256_match") is True
        )
    elif policy == "structured-semantic-review-v1":
        valid = (
            output.get("verdict") == "accept"
            and output.get("issues") == []
            and isinstance(output.get("checks"), dict)
            and all(value == "accept" for value in output["checks"].values())
        )
    elif policy == "test-fixture-v1":
        valid = output.get("capability") == capability and output.get("verdict") == verdict
    else:
        raise EvidenceError(f"未知 verifier policy：{policy}")
    if not valid:
        raise EvidenceError(f"verifier 输出不满足 policy={policy}")


def create_evidence_receipt(
    *,
    project_root: Path,
    result: dict[str, Any],
    generator: str,
    evidence_id: str,
    capability: str,
    verdict: str,
    verifier: str,
    checked_at: str,
    output_locator: str,
    command: list[str],
    notes: str,
    executor: str = "subprocess",
    invalidates: list[str] | None = None,
) -> dict[str, Any]:
    """为已存在的 verifier 输出生成可现场重算的 Result evidence 项。"""
    if invalidates and verdict != "reject":
        raise EvidenceError("只有 verdict=reject 的证据可以声明 invalidates")
    registry = load_verifier_registry(project_root)
    principal = registry.get(verifier)
    if principal is None or principal.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{verifier}")
    if capability not in principal["capabilities"]:
        raise EvidenceError(f"{verifier} 未注册 capability={capability}")
    if executor not in {"subprocess", "in_process"}:
        raise EvidenceError(f"未知 verifier executor：{executor}")
    output_path = _trusted_file(project_root, output_locator)
    _validate_output_policy(
        policy=principal["policy"],
        output_path=output_path,
        verdict=verdict,
        capability=capability,
        invalidates=invalidates or [],
    )
    generator_entry = registry.get(generator)
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{generator}")
    independent = principal["trust_domain"] != generator_entry["trust_domain"]
    receipt_locator = (
        f"research/artifacts/receipts/{result['result_id'].removeprefix('result:')}/"
        f"{evidence_id.removeprefix('evidence:')}.json"
    )
    receipt = {
        "schema_version": "1.0.0",
        "evidence_id": evidence_id,
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "checked_at": checked_at,
        "subject": {
            "problem_id": result["problem_id"],
            "attempt_id": result["attempt_id"],
            "result_id": result["result_id"],
        },
        "output": {
            "locator": output_locator,
            "sha256": sha256_file(output_path),
        },
        "command": {"executor": executor, "argv": command, "exit_code": 0},
    }
    receipt_path = project_root / receipt_locator
    encoded = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if receipt_path.is_file():
        if receipt_path.read_bytes() != encoded:
            raise EvidenceError(f"证据回执已存在且内容不同：{receipt_locator}")
    else:
        _write_atomic(receipt_path, encoded)
    return {
        "evidence_id": evidence_id,
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "independent": independent,
        "locator": receipt_locator,
        "sha256": sha256_file(receipt_path),
        "checked_at": checked_at,
        "invalidates": invalidates or [],
        "notes": notes,
    }


def create_obligation_evidence_receipt(
    *,
    project_root: Path,
    graph: dict[str, Any],
    candidate: dict[str, Any],
    evidence_id: str,
    capability: str,
    verdict: str,
    verifier: str,
    checked_at: str,
    output_locator: str,
    command: list[str],
    command_exit_code: int = 0,
    executor: str = "subprocess",
    native_status: str | None = None,
    inputs: list[dict[str, str]] | None = None,
    toolchain: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create an immutable receipt whose subject is one obligation candidate."""
    registry = load_verifier_registry(project_root)
    principal = registry.get(verifier)
    if principal is None or principal.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{verifier}")
    if capability not in principal.get("capabilities", []):
        raise EvidenceError(f"{verifier} 未注册 capability={capability}")
    generator_entry = registry.get(candidate.get("generator"))
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{candidate.get('generator')}")
    if executor not in {"subprocess", "in_process"}:
        raise EvidenceError(f"未知 verifier executor：{executor}")
    for key in ("problem_id", "attempt_id", "graph_id"):
        if candidate.get(key) != graph.get(key):
            raise EvidenceError(f"Candidate 与 ObligationGraph 的 {key} 不一致")
    output_path = _trusted_file(project_root, output_locator)
    _validate_output_policy(
        policy=principal["policy"],
        output_path=output_path,
        verdict=verdict,
        capability=capability,
        invalidates=[],
    )
    receipt_locator = (
        "research/artifacts/receipts/obligations/"
        f"{candidate['candidate_id'].removeprefix('candidate:')}/"
        f"{evidence_id.removeprefix('evidence:')}.json"
    )
    receipt = {
        "schema_version": "1.0.0",
        "evidence_id": evidence_id,
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "checked_at": checked_at,
        "subject": {
            "problem_id": candidate["problem_id"],
            "attempt_id": candidate["attempt_id"],
            "graph_id": candidate["graph_id"],
            "obligation_id": candidate["obligation_id"],
            "candidate_id": candidate["candidate_id"],
        },
        "output": {
            "locator": output_locator,
            "sha256": sha256_file(output_path),
        },
        "command": {
            "executor": executor,
            "argv": command,
            "exit_code": command_exit_code,
        },
    }
    if native_status is not None:
        receipt["native_status"] = native_status
    if inputs is not None:
        receipt["inputs"] = inputs
    if toolchain is not None:
        receipt["toolchain"] = toolchain
    _validate_schema(
        project_root / "research" / "schema" / "evidence-receipt.schema.json",
        receipt,
        "义务证据回执",
    )
    receipt_path = project_root / receipt_locator
    encoded = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if receipt_path.is_file():
        if receipt_path.read_bytes() != encoded:
            raise EvidenceError(f"证据回执已存在且内容不同：{receipt_locator}")
    else:
        _write_atomic(receipt_path, encoded)
    return {
        "locator": receipt_locator,
        "sha256": sha256_file(receipt_path),
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "independent": principal["trust_domain"] != generator_entry["trust_domain"],
    }


def verify_obligation_evidence_receipt(
    *,
    project_root: Path,
    graph: dict[str, Any],
    candidate: dict[str, Any],
    link: dict[str, Any],
) -> dict[str, Any]:
    """Verify a linked receipt and derive capability, verdict and independence."""
    registry = load_verifier_registry(project_root)
    generator_entry = registry.get(candidate.get("generator"))
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{candidate.get('generator')}")
    receipt_ref = link.get("receipt", {})
    receipt_path = _trusted_file(project_root, receipt_ref.get("locator", ""))
    if sha256_file(receipt_path) != receipt_ref.get("sha256"):
        raise EvidenceError("EvidenceLink 回执 SHA-256 与现场文件不匹配")
    receipt = _load_output_json(receipt_path)
    _validate_schema(
        project_root / "research" / "schema" / "evidence-receipt.schema.json",
        receipt,
        "义务证据回执",
    )
    verifier_entry = registry.get(receipt.get("verifier"))
    if verifier_entry is None or verifier_entry.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{receipt.get('verifier')}")
    capability = receipt.get("capability")
    if capability not in verifier_entry.get("capabilities", []):
        raise EvidenceError(f"verifier 未注册 capability={capability}")
    expected_subject = {
        "problem_id": candidate.get("problem_id"),
        "attempt_id": candidate.get("attempt_id"),
        "graph_id": graph.get("graph_id"),
        "obligation_id": candidate.get("obligation_id"),
        "candidate_id": candidate.get("candidate_id"),
    }
    if receipt.get("subject") != expected_subject:
        raise EvidenceError("义务证据回执 subject 与 Candidate 不一致")
    if any(
        link.get(field) != candidate.get(field)
        for field in ("graph_id", "obligation_id", "candidate_id")
    ):
        raise EvidenceError("EvidenceLink 与 Candidate 身份不一致")
    command = receipt.get("command", {})
    if receipt.get("verdict") == "accept" and command.get("exit_code") != 0:
        raise EvidenceError("accept 回执必须绑定成功 verifier 命令")
    output = receipt.get("output", {})
    output_path = _trusted_file(project_root, output.get("locator", ""))
    if sha256_file(output_path) != output.get("sha256"):
        raise EvidenceError("verifier 输出 SHA-256 与现场文件不匹配")
    _validate_output_policy(
        policy=verifier_entry["policy"],
        output_path=output_path,
        verdict=receipt.get("verdict"),
        capability=capability,
        invalidates=[],
    )
    return {
        "capability": capability,
        "verdict": receipt.get("verdict"),
        "verifier": receipt.get("verifier"),
        "independent": verifier_entry["trust_domain"] != generator_entry["trust_domain"],
        "native_status": receipt.get("native_status"),
        "receipt": receipt,
    }


def verify_evidence_receipt(
    *,
    project_root: Path,
    result: dict[str, Any],
    evidence: dict[str, Any],
    generator: str,
) -> str:
    """验证回执、底层输出、签发能力与派生独立性，返回 capability。"""
    registry = load_verifier_registry(project_root)
    generator_entry = registry.get(generator)
    verifier_entry = registry.get(evidence.get("verifier"))
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{generator}")
    if verifier_entry is None or verifier_entry.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{evidence.get('verifier')}")
    capability = evidence.get("capability")
    if capability not in verifier_entry.get("capabilities", []):
        raise EvidenceError(f"verifier 未注册 capability={capability}")
    derived_independent = (
        verifier_entry["trust_domain"] != generator_entry["trust_domain"]
    )
    if evidence.get("independent") is not derived_independent:
        raise EvidenceError("independent 与 registry 派生值不一致")

    receipt_path = _trusted_file(project_root, evidence.get("locator", ""))
    claimed_digest = evidence.get("sha256")
    if not isinstance(claimed_digest, str) or sha256_file(receipt_path) != claimed_digest:
        raise EvidenceError("回执 SHA-256 与现场文件不匹配")
    try:
        if receipt_path.stat().st_size > MAX_VERIFIER_JSON_BYTES:
            raise EvidenceError("证据回执超过 2 MiB 上限")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except EvidenceError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError("证据回执不是有效 JSON") from exc
    _validate_schema(
        project_root / "research" / "schema" / "evidence-receipt.schema.json",
        receipt,
        "证据回执",
    )
    for field in ("evidence_id", "capability", "verdict", "verifier", "checked_at"):
        if receipt.get(field) != evidence.get(field):
            raise EvidenceError(f"回执字段与 Result 不一致：{field}")
    expected_subject = {
        "problem_id": result.get("problem_id"),
        "attempt_id": result.get("attempt_id"),
        "result_id": result.get("result_id"),
    }
    if receipt.get("subject") != expected_subject:
        raise EvidenceError("回执 subject 与 Result 不一致")
    command = receipt.get("command", {})
    if evidence.get("verdict") == "accept" and command.get("exit_code") != 0:
        raise EvidenceError("accept 回执必须绑定成功 verifier 命令")
    output = receipt.get("output", {})
    output_path = _trusted_file(project_root, output.get("locator", ""))
    if sha256_file(output_path) != output.get("sha256"):
        raise EvidenceError("verifier 输出 SHA-256 与现场文件不匹配")
    _validate_output_policy(
        policy=verifier_entry["policy"],
        output_path=output_path,
        verdict=evidence.get("verdict"),
        capability=capability,
        invalidates=evidence.get("invalidates", []),
    )
    return capability
