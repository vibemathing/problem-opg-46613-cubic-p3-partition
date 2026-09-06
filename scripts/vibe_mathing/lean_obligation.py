"""Bounded, candidate-scoped Lean verifier for obligation EvidenceLinks."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .evidence import (
    EvidenceError,
    create_obligation_evidence_receipt,
    load_verifier_registry,
    sha256_file,
)
from .obligations import ObligationError, load_obligation_state
from .runtime import RuntimeErrorBase, execute_bounded, now


ESCAPE_PATTERN = re.compile(
    r"\b(?:sorry|admit|unsafe|axiom|partial|extern|native_decide|implemented_by)\b|#eval"
)
AXIOM_LIST_PATTERN = re.compile(r"depends on axioms:\s*\[([^\]]*)\]", re.DOTALL)


class LeanObligationError(RuntimeError):
    """The trusted Lean verifier request or execution is invalid."""


def _resolve_tool(name: str) -> str:
    resolved = shutil.which(name)
    if resolved:
        return resolved
    elan_tool = Path.home() / ".elan" / "bin" / name
    if elan_tool.is_file() and os.access(elan_tool, os.X_OK):
        return str(elan_tool)
    raise LeanObligationError(f"找不到 {name}")


def _validate_request(project_root: Path, request: dict[str, Any]) -> None:
    schema_path = project_root / "research/schema/lean-obligation-request.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LeanObligationError(f"无法读取 Lean request schema：{schema_path}") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(request),
        key=lambda item: list(item.path),
    )
    if errors:
        raise LeanObligationError(f"Lean obligation request 无效：{errors[0].message}")


def _safe_directory(project_root: Path, locator: str) -> Path:
    pure = PurePosixPath(locator)
    if pure.is_absolute() or ".." in pure.parts or "\\" in locator:
        raise LeanObligationError(f"fixture_root 非法：{locator}")
    path = project_root.joinpath(*pure.parts)
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(project_root.resolve())
    except (OSError, ValueError) as exc:
        raise LeanObligationError(f"fixture_root 不存在或逃逸：{locator}") from exc
    if path.is_symlink() or not path.is_dir():
        raise LeanObligationError("fixture_root 必须是 project 内 regular directory")
    return path


def _safe_source(fixture_root: Path, locator: str) -> Path:
    pure = PurePosixPath(locator)
    if pure.is_absolute() or ".." in pure.parts or "\\" in locator:
        raise LeanObligationError(f"Lean source path 非法：{locator}")
    path = fixture_root.joinpath(*pure.parts)
    try:
        path.resolve(strict=True).relative_to(fixture_root.resolve())
    except (OSError, ValueError) as exc:
        raise LeanObligationError(f"Lean source 不存在或逃逸：{locator}") from exc
    if path.is_symlink() or not path.is_file():
        raise LeanObligationError(f"Lean source 必须是 regular file：{locator}")
    return path


def _strip_lean_comments_and_strings(text: str) -> str:
    """Conservative lexer used only for escape/header scanning, never for parsing Lean."""
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    while index < len(text):
        pair = text[index : index + 2]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if text[index] == "\n" else " ")
                index += 1
            continue
        if in_string:
            if text[index] == "\\" and index + 1 < len(text):
                output.extend("  ")
                index += 2
            elif text[index] == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if text[index] == "\n" else " ")
                index += 1
            continue
        if pair == "--":
            end = text.find("\n", index)
            if end == -1:
                output.extend(" " * (len(text) - index))
                break
            output.extend(" " * (end - index))
            index = end
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif text[index] == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(text[index])
            index += 1
    return "".join(output)


def _normalize_declaration(value: str) -> str:
    return " ".join(value.split())


def _toolchain_fingerprint(fixture_root: Path) -> tuple[str, str]:
    toolchain_path = fixture_root / "lean-toolchain"
    lakefile_path = fixture_root / "lakefile.toml"
    if not toolchain_path.is_file() or not lakefile_path.is_file():
        raise LeanObligationError("Lean fixture 缺少 lean-toolchain 或 lakefile.toml")
    toolchain = toolchain_path.read_text(encoding="utf-8").strip()
    digest = hashlib.sha256()
    for name in ("lean-toolchain", "lakefile.toml", "lake-manifest.json"):
        path = fixture_root / name
        if not path.is_file():
            continue
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return toolchain, digest.hexdigest()


def _toolchain_admitted(
    registry: dict[str, dict[str, Any]],
    verifier_ids: list[str],
    *,
    toolchain: str,
    fingerprint: str,
) -> bool:
    wanted = {"id": "lean", "version": toolchain, "fingerprint": fingerprint}
    for verifier_id in verifier_ids:
        entry = registry.get(verifier_id)
        if entry is None or entry.get("role") != "verifier":
            return False
        if wanted not in entry.get("toolchain_allowlist", []):
            return False
    return True


def _sanitize_process_result(
    result: dict[str, Any],
    *,
    project_root: Path,
    fixture_root: Path,
) -> dict[str, Any]:
    def clean(value: str) -> str:
        return (
            value.replace(str(fixture_root), "<fixture_root>")
            .replace(str(project_root), "<project_root>")[-8000:]
        )

    return {
        "argv": [Path(result["argv"][0]).name, *result["argv"][1:]],
        "exit_code": result["exit_code"],
        "stdout": clean(result["stdout"]),
        "stderr": clean(result["stderr"]),
        "stdout_sha256": hashlib.sha256(result["stdout"].encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(result["stderr"].encode()).hexdigest(),
    }


def _classify_runtime_failure(exc: RuntimeErrorBase) -> str:
    message = str(exc)
    if "超时" in message:
        return "timeout"
    if any(fragment in message for fragment in ("信号", "内存", "MemoryError", "resource")):
        return "resource_error"
    return "checker_error"


def _parse_axioms(text: str) -> tuple[str, list[str]]:
    if "does not depend on any axioms" in text:
        return "parsed", []
    match = AXIOM_LIST_PATTERN.search(text)
    if not match:
        return "unparsed", []
    names = [item.strip() for item in match.group(1).split(",") if item.strip()]
    return "parsed", sorted(set(names))


def _write_content_addressed_output(
    project_root: Path,
    candidate_id: str,
    capability: str,
    payload: dict[str, Any],
) -> tuple[str, str]:
    encoded = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    digest = hashlib.sha256(encoded).hexdigest()
    locator = (
        "research/artifacts/outputs/obligations/"
        f"{candidate_id.removeprefix('candidate:')}/"
        f"{capability.replace('_', '-')}-{digest}.json"
    )
    path = project_root / locator
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != encoded:
            raise LeanObligationError(f"content-addressed output 冲突：{locator}")
    else:
        temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        try:
            with temporary.open("wb") as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    return locator, digest


def verify_lean_obligation(
    *,
    project_root: Path,
    request: dict[str, Any],
) -> dict[str, Any]:
    """Run fixed Lean commands and return receipts plus uncommitted EvidenceLinks."""
    project_root = project_root.resolve()
    _validate_request(project_root, request)
    try:
        state = load_obligation_state(project_root)
    except ObligationError as exc:
        raise LeanObligationError(str(exc)) from exc
    graph = state["graphs"].get(request["graph_id"])
    candidate = state["candidates"].get(request["candidate_id"])
    if graph is None or candidate is None:
        raise LeanObligationError("Lean request 引用未知 graph/candidate")
    if (
        candidate["graph_id"] != request["graph_id"]
        or candidate["obligation_id"] != request["obligation_id"]
        or candidate["kind"] not in {"proof", "formalization"}
    ):
        raise LeanObligationError("Lean request 与 Candidate 身份或 kind 不一致")
    obligation = state["obligations_by_graph"][graph["graph_id"]][request["obligation_id"]]
    fixture_root = _safe_directory(project_root, request["fixture_root"])
    source_paths = [_safe_source(fixture_root, value) for value in request["source_files"]]
    candidate_path = project_root / candidate["artifact"]["locator"]
    if candidate_path.resolve() not in {path.resolve() for path in source_paths}:
        raise LeanObligationError("Candidate artifact 必须列入 Lean source_files")
    toolchain, toolchain_fingerprint = _toolchain_fingerprint(fixture_root)
    registry = load_verifier_registry(project_root)
    verifier_ids = [request["verifiers"][key] for key in sorted(request["verifiers"])]
    admitted = _toolchain_admitted(
        registry,
        verifier_ids,
        toolchain=toolchain,
        fingerprint=toolchain_fingerprint,
    )
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    stripped_source = _strip_lean_comments_and_strings(source_text)
    escapes = sorted(set(ESCAPE_PATTERN.findall(stripped_source)))
    declaration_identity = (
        _normalize_declaration(request["expected_declaration"])
        in _normalize_declaration(stripped_source)
        and request["declaration"].split(".")[-1]
        in request["expected_declaration"]
    )
    statement_digest_match = candidate["statement_sha256"] == obligation["statement_sha256"]
    budgets = request["budgets"]
    runtime_kwargs = {
        "timeout_seconds": budgets["timeout_seconds"],
        "max_output_bytes": budgets["max_output_bytes"],
        "max_memory_bytes": budgets["max_memory_bytes"],
    }
    lake = _resolve_tool("lake")
    version: dict[str, Any] = {"argv": ["lake", "env", "lean", "--version"], "exit_code": 1, "stdout": "", "stderr": "not run"}
    build: dict[str, Any] = {"argv": ["lake", "--quiet", "build"], "exit_code": 1, "stdout": "", "stderr": "not run"}
    axiom: dict[str, Any] = {"argv": ["lake", "env", "lean", "<axiom-audit>"], "exit_code": 1, "stdout": "", "stderr": "not run"}
    native_status = "accepted"
    runtime_error: str | None = None
    audit_path: Path | None = None
    try:
        version_raw = execute_bounded(
            [lake, "env", "lean", "--version"],
            cwd=fixture_root,
            **runtime_kwargs,
        )
        version = _sanitize_process_result(
            version_raw,
            project_root=project_root,
            fixture_root=fixture_root,
        )
        build_raw = execute_bounded(
            [lake, "--quiet", "build"],
            cwd=fixture_root,
            **runtime_kwargs,
        )
        build = _sanitize_process_result(
            build_raw,
            project_root=project_root,
            fixture_root=fixture_root,
        )
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".lean",
            prefix=".vibe-obligation-audit-",
            dir=fixture_root,
            delete=False,
        ) as handle:
            handle.write(f"import {request['module']}\n#print axioms {request['declaration']}\n")
            audit_path = Path(handle.name)
        axiom_raw = execute_bounded(
            [lake, "env", "lean", audit_path.name],
            cwd=fixture_root,
            **runtime_kwargs,
        )
        axiom = _sanitize_process_result(
            axiom_raw,
            project_root=project_root,
            fixture_root=fixture_root,
        )
        if any(item["exit_code"] != 0 for item in (version, build, axiom)):
            native_status = "rejected"
    except RuntimeErrorBase as exc:
        native_status = _classify_runtime_failure(exc)
        runtime_error = str(exc).replace(str(project_root), "<project_root>").replace(
            str(fixture_root), "<fixture_root>"
        )
    finally:
        if audit_path is not None:
            audit_path.unlink(missing_ok=True)

    axiom_text = axiom.get("stdout", "") + axiom.get("stderr", "")
    parse_status, actual_axioms = _parse_axioms(axiom_text)
    unauthorized_axioms = sorted(set(actual_axioms) - set(request["allowed_axioms"]))
    if not admitted and native_status == "accepted":
        native_status = "unsupported"
    kernel_accept = native_status == "accepted" and build["exit_code"] == 0 and axiom["exit_code"] == 0
    axiom_accept = (
        kernel_accept
        and not escapes
        and parse_status == "parsed"
        and not unauthorized_axioms
    )
    statement_accept = kernel_accept and declaration_identity and statement_digest_match
    decisions = {
        "kernel_check": kernel_accept,
        "axiom_escape_audit": axiom_accept,
        "statement_identity": statement_accept,
    }
    common = {
        "schema_version": "1.0.0",
        "graph_id": graph["graph_id"],
        "obligation_id": obligation["obligation_id"],
        "candidate_id": candidate["candidate_id"],
        "native_status": native_status,
        "toolchain": toolchain,
        "toolchain_fingerprint": toolchain_fingerprint,
        "toolchain_admission_status": "admitted" if admitted else "unadmitted",
        "version": version,
        "build": build,
        "axiom_command": axiom,
        "runtime_error": runtime_error,
    }
    payloads = {
        "kernel_check": {
            **common,
            "capability": "kernel_check",
            "verdict": "accept" if kernel_accept else "undetermined" if native_status in {"timeout", "resource_error", "checker_error", "unsupported"} else "reject",
        },
        "axiom_escape_audit": {
            **common,
            "capability": "axiom_escape_audit",
            "verdict": "accept" if axiom_accept else "undetermined" if native_status in {"timeout", "resource_error", "checker_error", "unsupported"} else "reject",
            "escapes": escapes,
            "allowed_axioms": sorted(request["allowed_axioms"]),
            "actual_axioms": actual_axioms,
            "unauthorized_axioms": unauthorized_axioms,
            "axiom_parse_status": parse_status,
        },
        "statement_identity": {
            **common,
            "capability": "statement_identity",
            "verdict": "accept" if statement_accept else "undetermined" if native_status in {"timeout", "resource_error", "checker_error", "unsupported"} else "reject",
            "expected_declaration": request["expected_declaration"],
            "declaration_identity": declaration_identity,
            "statement_sha256_match": statement_digest_match,
        },
    }
    checked_at = now()
    nonce = hashlib.sha256(
        f"{checked_at}\0{os.getpid()}\0{time.time_ns()}".encode()
    ).hexdigest()[:12]
    inputs = [
        {
            "locator": path.relative_to(project_root).as_posix(),
            "sha256": sha256_file(path),
        }
        for path in source_paths
    ]
    toolchain_record = {
        "id": "lean",
        "version": toolchain,
        "fingerprint": toolchain_fingerprint,
    }
    links: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    for capability in ("kernel_check", "axiom_escape_audit", "statement_identity"):
        payload = payloads[capability]
        locator, output_digest = _write_content_addressed_output(
            project_root,
            candidate["candidate_id"],
            capability,
            payload,
        )
        suffix = capability.replace("_", "-")
        evidence_id = (
            f"evidence:{candidate['candidate_id'].removeprefix('candidate:')}."
            f"{suffix}.{nonce}"
        )
        try:
            receipt = create_obligation_evidence_receipt(
                project_root=project_root,
                graph=graph,
                candidate=candidate,
                evidence_id=evidence_id,
                capability=capability,
                verdict=payload["verdict"],
                verifier=request["verifiers"][capability],
                checked_at=checked_at,
                output_locator=locator,
                command=payload["build"]["argv"] if capability == "kernel_check" else payload["axiom_command"]["argv"],
                command_exit_code=payload["build"]["exit_code"] if capability == "kernel_check" else payload["axiom_command"]["exit_code"],
                native_status=native_status,
                inputs=inputs,
                toolchain=toolchain_record,
            )
        except EvidenceError as exc:
            raise LeanObligationError(str(exc)) from exc
        link_id = (
            f"evidence-link:{candidate['candidate_id'].removeprefix('candidate:')}."
            f"{suffix}.{nonce}"
        )
        links.append(
            {
                "schema_version": "1.0.0",
                "evidence_link_id": link_id,
                "graph_id": graph["graph_id"],
                "obligation_id": obligation["obligation_id"],
                "candidate_id": candidate["candidate_id"],
                "receipt": {
                    "locator": receipt["locator"],
                    "sha256": receipt["sha256"],
                },
                "invalidates": [],
                "linked_at": checked_at,
            }
        )
        receipts.append({**receipt, "output_sha256": output_digest})
    return {
        "native_status": native_status,
        "toolchain_admission_status": "admitted" if admitted else "unadmitted",
        "decisions": decisions,
        "reports": payloads,
        "receipts": receipts,
        "evidence_links": links,
    }
