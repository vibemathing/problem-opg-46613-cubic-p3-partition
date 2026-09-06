"""Immutable obligation DAGs, candidate artifacts, EvidenceLinks and closure gates."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

from .evidence import (
    EvidenceError,
    load_verifier_registry,
    sha256_file,
    verify_obligation_evidence_receipt,
)


GRAPH_RECORDS = Path("research/records/obligation-graphs.jsonl")
CANDIDATE_RECORDS = Path("research/records/candidate-artifacts.jsonl")
EVIDENCE_LINK_RECORDS = Path("research/records/evidence-links.jsonl")
MAX_RECORD_BYTES = 2 * 1024 * 1024


class ObligationError(RuntimeError):
    """An obligation truth object or derived closure is invalid."""


class ObligationConflict(ObligationError):
    """A proof and a counterexample both satisfy the same obligation."""


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def statement_sha256(statement: dict[str, Any]) -> str:
    """Digest the exact structured statement, not a rendered or normalized paraphrase."""
    return canonical_json_sha256(statement)


def _load_schema(project_root: Path, name: str) -> dict[str, Any]:
    path = project_root / "research" / "schema" / name
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ObligationError(f"无法读取 schema：{path}") from exc
    if not isinstance(value, dict):
        raise ObligationError(f"schema 不是 JSON object：{path}")
    return value


def _validate_schema(project_root: Path, name: str, value: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(
            _load_schema(project_root, name),
            format_checker=FormatChecker(),
        ).iter_errors(value),
        key=lambda item: list(item.path),
    )
    if errors:
        path = "/".join(str(part) for part in errors[0].path) or "<root>"
        raise ObligationError(f"{label} schema 无效 ({path})：{errors[0].message}")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    if path.is_symlink() or not path.is_file():
        raise ObligationError(f"记录路径必须是 regular file：{path}")
    values: list[dict[str, Any]] = []
    with path.open("rb") as handle:
        for line_number, raw in enumerate(handle, 1):
            if len(raw) > MAX_RECORD_BYTES:
                raise ObligationError(f"{path}:{line_number} 超过 2 MiB")
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ObligationError(f"{path}:{line_number} 不是有效 JSON") from exc
            if not isinstance(value, dict):
                raise ObligationError(f"{path}:{line_number} 必须是 JSON object")
            values.append(value)
    return values


def _index_unique(records: Iterable[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        identity = record.get(key)
        if not isinstance(identity, str):
            raise ObligationError(f"{label} 缺少 {key}")
        if identity in index:
            raise ObligationError(f"{label} {key} 重复：{identity}")
        index[identity] = record
    return index


def _trusted_artifact(project_root: Path, locator: str) -> Path:
    if not isinstance(locator, str) or not locator:
        raise ObligationError("artifact locator 为空")
    pure = PurePosixPath(locator)
    if pure.is_absolute() or ".." in pure.parts or "\\" in locator:
        raise ObligationError(f"artifact locator 非法：{locator}")
    if pure.parts[:2] != ("research", "artifacts"):
        raise ObligationError(f"artifact 必须位于 research/artifacts：{locator}")
    path = project_root.joinpath(*pure.parts)
    root = project_root.resolve()
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ObligationError(f"artifact 不存在：{locator}") from exc
    if path.is_symlink() or not path.is_file():
        raise ObligationError(f"artifact 必须是 regular file：{locator}")
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ObligationError(f"artifact 逃逸 project root：{locator}") from exc
    return path


def _problem_contracts(project_root: Path) -> dict[str, dict[str, Any]]:
    return _index_unique(
        _read_jsonl(project_root / "problem-library/records/canonical-problems.jsonl"),
        "problem_id",
        "ProblemContract",
    )


def _attempts(project_root: Path) -> dict[str, dict[str, Any]]:
    return _index_unique(
        _read_jsonl(project_root / "research/records/attempts.jsonl"),
        "attempt_id",
        "Attempt",
    )


def _validate_graph_structure(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    obligations = _index_unique(graph["obligations"], "obligation_id", "Obligation")
    root_id = graph["root_obligation_id"]
    if root_id not in obligations:
        raise ObligationError(f"root obligation 不存在：{root_id}")
    for obligation in obligations.values():
        actual_digest = statement_sha256(obligation["statement"])
        if actual_digest != obligation["statement_sha256"]:
            raise ObligationError(
                f"statement_sha256 不匹配：{obligation['obligation_id']}"
            )
        unknown = sorted(set(obligation["dependencies"]) - obligations.keys())
        if unknown:
            raise ObligationError(
                f"未知 obligation dependency：{obligation['obligation_id']} -> {unknown[0]}"
            )

    color: dict[str, int] = {}

    def visit(identity: str) -> None:
        state = color.get(identity, 0)
        if state == 1:
            raise ObligationError(f"ObligationGraph 含循环：{identity}")
        if state == 2:
            return
        color[identity] = 1
        for dependency in obligations[identity]["dependencies"]:
            visit(dependency)
        color[identity] = 2

    visit(root_id)
    unreachable = sorted(set(obligations) - color.keys())
    if unreachable:
        raise ObligationError(f"ObligationGraph 含 root 不可达节点：{unreachable[0]}")
    return obligations


def load_obligation_state(project_root: Path) -> dict[str, Any]:
    """Load and validate all append-only obligation truth objects."""
    project_root = project_root.resolve()
    graphs = _read_jsonl(project_root / GRAPH_RECORDS)
    candidates = _read_jsonl(project_root / CANDIDATE_RECORDS)
    links = _read_jsonl(project_root / EVIDENCE_LINK_RECORDS)
    if not graphs and not candidates and not links:
        return {
            "graphs": {},
            "current_graph_by_attempt": {},
            "obligations_by_graph": {},
            "candidates": {},
            "links": [],
            "link_receipts": {},
        }
    problems = _problem_contracts(project_root)
    attempts = _attempts(project_root)
    graph_index: dict[str, dict[str, Any]] = {}
    obligations_by_graph: dict[str, dict[str, dict[str, Any]]] = {}
    superseded: set[str] = set()
    child_by_predecessor: dict[str, str] = {}
    for graph in graphs:
        _validate_schema(project_root, "obligation-graph.schema.json", graph, "ObligationGraph")
        graph_id = graph["graph_id"]
        if graph_id in graph_index:
            raise ObligationError(f"graph_id 重复：{graph_id}")
        predecessor = graph["supersedes"]
        if predecessor is not None:
            old = graph_index.get(predecessor)
            if old is None:
                raise ObligationError(f"supersedes 必须引用更早 graph：{predecessor}")
            if predecessor in child_by_predecessor:
                raise ObligationError(f"ObligationGraph revision 分叉：{predecessor}")
            if (old["problem_id"], old["attempt_id"]) != (
                graph["problem_id"],
                graph["attempt_id"],
            ):
                raise ObligationError("ObligationGraph revision 跨 Problem/Attempt")
            child_by_predecessor[predecessor] = graph_id
            superseded.add(predecessor)
        problem = problems.get(graph["problem_id"])
        if problem is None:
            raise ObligationError(f"ObligationGraph 引用未知 Problem：{graph['problem_id']}")
        if canonical_json_sha256(problem) != graph["problem_contract_sha256"]:
            raise ObligationError(f"ProblemContract digest 漂移：{graph_id}")
        attempt = attempts.get(graph["attempt_id"])
        if attempt is None or attempt.get("problem_id") != graph["problem_id"]:
            raise ObligationError(f"ObligationGraph 引用未知或跨题 Attempt：{graph['attempt_id']}")
        if attempt.get("route_id") != graph["route_id"]:
            raise ObligationError(f"ObligationGraph route 与 Attempt 不一致：{graph_id}")
        if attempt.get("problem_contract_sha256") != graph["problem_contract_sha256"]:
            raise ObligationError(f"Attempt 的 ProblemContract digest 不一致：{graph_id}")
        graph_index[graph_id] = graph
        obligations_by_graph[graph_id] = _validate_graph_structure(graph)

    current_graph_by_attempt: dict[str, str] = {}
    for graph_id, graph in graph_index.items():
        if graph_id in superseded:
            continue
        attempt_id = graph["attempt_id"]
        if attempt_id in current_graph_by_attempt:
            raise ObligationError(f"一个 Attempt 存在多个 current ObligationGraph：{attempt_id}")
        current_graph_by_attempt[attempt_id] = graph_id
        if attempts[attempt_id].get("obligation_graph_id") != graph_id:
            raise ObligationError(f"Attempt 未绑定 current ObligationGraph：{attempt_id}")

    candidate_index: dict[str, dict[str, Any]] = {}
    registry = load_verifier_registry(project_root)
    for candidate in candidates:
        _validate_schema(project_root, "candidate-artifact.schema.json", candidate, "Candidate")
        candidate_id = candidate["candidate_id"]
        if candidate_id in candidate_index:
            raise ObligationError(f"candidate_id 重复：{candidate_id}")
        graph = graph_index.get(candidate["graph_id"])
        if graph is None:
            raise ObligationError(f"Candidate 引用未知 graph：{candidate_id}")
        if any(
            candidate[field] != graph[field]
            for field in ("problem_id", "attempt_id", "graph_id")
        ):
            raise ObligationError(f"Candidate 与 graph 身份不一致：{candidate_id}")
        obligation = obligations_by_graph[graph["graph_id"]].get(candidate["obligation_id"])
        if obligation is None:
            raise ObligationError(f"Candidate 引用未知 obligation：{candidate_id}")
        if candidate["kind"] not in obligation["acceptance"]["allowed_candidate_kinds"]:
            raise ObligationError(f"Candidate kind 未被 obligation 允许：{candidate_id}")
        generator = registry.get(candidate["generator"])
        if generator is None or generator.get("role") != "generator":
            raise ObligationError(f"Candidate generator 未注册：{candidate['generator']}")
        artifact = _trusted_artifact(project_root, candidate["artifact"]["locator"])
        if sha256_file(artifact) != candidate["artifact"]["sha256"]:
            raise ObligationError(f"Candidate artifact digest 不匹配：{candidate_id}")
        candidate_index[candidate_id] = candidate

    link_index: dict[str, dict[str, Any]] = {}
    link_receipts: dict[str, dict[str, Any]] = {}
    for link in links:
        _validate_schema(project_root, "evidence-link.schema.json", link, "EvidenceLink")
        link_id = link["evidence_link_id"]
        if link_id in link_index:
            raise ObligationError(f"evidence_link_id 重复：{link_id}")
        candidate = candidate_index.get(link["candidate_id"])
        if candidate is None:
            raise ObligationError(f"EvidenceLink 引用未知 Candidate：{link_id}")
        unknown_invalidations = [value for value in link["invalidates"] if value not in link_index]
        if unknown_invalidations:
            raise ObligationError(
                f"EvidenceLink invalidates 必须引用更早 link：{unknown_invalidations[0]}"
            )
        try:
            info = verify_obligation_evidence_receipt(
                project_root=project_root,
                graph=graph_index[candidate["graph_id"]],
                candidate=candidate,
                link=link,
            )
        except EvidenceError as exc:
            raise ObligationError(f"EvidenceLink 回执无效 {link_id}：{exc}") from exc
        if link["invalidates"]:
            if info["verdict"] != "reject" or not info["independent"]:
                raise ObligationError("只有独立 reject 回执可以 invalidates EvidenceLink")
            for old_id in link["invalidates"]:
                old_link = link_index[old_id]
                old_info = link_receipts[old_id]
                if old_link["candidate_id"] != link["candidate_id"]:
                    raise ObligationError("EvidenceLink 不得跨 Candidate invalidates")
                if old_info["capability"] != info["capability"]:
                    raise ObligationError("EvidenceLink 不得跨 capability invalidates")
        link_index[link_id] = link
        link_receipts[link_id] = info

    return {
        "graphs": graph_index,
        "current_graph_by_attempt": current_graph_by_attempt,
        "obligations_by_graph": obligations_by_graph,
        "candidates": candidate_index,
        "links": links,
        "link_receipts": link_receipts,
    }


def derive_obligation_closure(
    project_root: Path,
    graph_id: str,
    *,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Derive AND-DAG closure only from current immutable objects and valid receipts."""
    state = state or load_obligation_state(project_root)
    graph = state["graphs"].get(graph_id)
    if graph is None:
        raise ObligationError(f"未知 ObligationGraph：{graph_id}")
    if state["current_graph_by_attempt"].get(graph["attempt_id"]) != graph_id:
        raise ObligationError(f"ObligationGraph 已被 supersede：{graph_id}")
    obligations = state["obligations_by_graph"][graph_id]
    candidates = {
        key: value
        for key, value in state["candidates"].items()
        if value["graph_id"] == graph_id
    }
    invalidated: set[str] = set()
    for link in state["links"]:
        if link["graph_id"] != graph_id:
            continue
        info = state["link_receipts"][link["evidence_link_id"]]
        if info["verdict"] == "reject" and info["independent"]:
            invalidated.update(link["invalidates"])

    accepted_by_candidate: dict[str, dict[str, list[str]]] = {}
    stale_candidates: set[str] = set()
    stale_links: set[str] = set()
    for candidate_id, candidate in candidates.items():
        obligation = obligations[candidate["obligation_id"]]
        if candidate["statement_sha256"] != obligation["statement_sha256"]:
            stale_candidates.add(candidate_id)
    for link in state["links"]:
        link_id = link["evidence_link_id"]
        if link["graph_id"] != graph_id:
            continue
        candidate_id = link["candidate_id"]
        info = state["link_receipts"][link_id]
        if candidate_id in stale_candidates or link_id in invalidated:
            stale_links.add(link_id)
            continue
        if info["verdict"] != "accept" or not info["independent"]:
            continue
        accepted_by_candidate.setdefault(candidate_id, {}).setdefault(
            info["capability"], []
        ).append(link_id)

    node_states: dict[str, dict[str, Any]] = {}

    def evaluate(obligation_id: str) -> dict[str, Any]:
        if obligation_id in node_states:
            return node_states[obligation_id]
        obligation = obligations[obligation_id]
        dependencies = [evaluate(value) for value in obligation["dependencies"]]
        required = set(obligation["acceptance"]["required_capabilities"])
        verified_proofs: list[str] = []
        verified_counterexamples: list[str] = []
        accepted_links: dict[str, list[str]] = {}
        candidate_capabilities: dict[str, list[str]] = {}
        for candidate_id, candidate in candidates.items():
            if candidate["obligation_id"] != obligation_id or candidate_id in stale_candidates:
                continue
            by_capability = accepted_by_candidate.get(candidate_id, {})
            capabilities = set(by_capability)
            candidate_capabilities[candidate_id] = sorted(capabilities)
            accepted_links[candidate_id] = sorted(
                link_id for values in by_capability.values() for link_id in values
            )
            if not required.issubset(capabilities):
                continue
            if candidate["kind"] == "counterexample":
                verified_counterexamples.append(candidate_id)
            else:
                verified_proofs.append(candidate_id)
        dependencies_closed = all(item["status"] == "closed" for item in dependencies)
        proof_closed = bool(verified_proofs) and dependencies_closed
        counterexample_closed = bool(verified_counterexamples)
        if proof_closed and counterexample_closed:
            status = "conflict"
        elif counterexample_closed:
            status = "refuted"
        elif proof_closed:
            status = "closed"
        elif any(item["status"] in {"refuted", "blocked_by_dependency", "conflict"} for item in dependencies):
            status = "blocked_by_dependency"
        else:
            status = "open"
        value = {
            "obligation_id": obligation_id,
            "statement_sha256": obligation["statement_sha256"],
            "status": status,
            "dependencies": list(obligation["dependencies"]),
            "required_capabilities": sorted(required),
            "verified_proof_candidates": sorted(verified_proofs),
            "verified_counterexample_candidates": sorted(verified_counterexamples),
            "candidate_capabilities": dict(sorted(candidate_capabilities.items())),
            "accepted_evidence_links": dict(sorted(accepted_links.items())),
        }
        node_states[obligation_id] = value
        return value

    root = evaluate(graph["root_obligation_id"])
    for obligation_id in sorted(obligations):
        evaluate(obligation_id)
    root_status = {
        "closed": "proof_closed",
        "refuted": "counterexample_closed",
        "blocked_by_dependency": "route_refuted",
        "conflict": "conflict",
        "open": "open",
    }[root["status"]]
    return {
        "schema_version": "1.0.0",
        "graph_id": graph_id,
        "problem_id": graph["problem_id"],
        "attempt_id": graph["attempt_id"],
        "route_id": graph["route_id"],
        "problem_contract_sha256": graph["problem_contract_sha256"],
        "root_obligation_id": graph["root_obligation_id"],
        "root_status": root_status,
        "nodes": [node_states[key] for key in sorted(node_states)],
        "open_obligation_ids": sorted(
            key for key, value in node_states.items() if value["status"] == "open"
        ),
        "blocked_obligation_ids": sorted(
            key
            for key, value in node_states.items()
            if value["status"] == "blocked_by_dependency"
        ),
        "refuted_obligation_ids": sorted(
            key for key, value in node_states.items() if value["status"] == "refuted"
        ),
        "conflicting_obligation_ids": sorted(
            key for key, value in node_states.items() if value["status"] == "conflict"
        ),
        "stale_candidate_ids": sorted(stale_candidates),
        "stale_evidence_link_ids": sorted(stale_links),
        "invalidated_evidence_link_ids": sorted(invalidated),
    }


def derive_all_obligation_closures(project_root: Path) -> list[dict[str, Any]]:
    state = load_obligation_state(project_root)
    return [
        derive_obligation_closure(project_root, graph_id, state=state)
        for graph_id in sorted(set(state["current_graph_by_attempt"].values()))
    ]


def obligation_result_gate(
    project_root: Path,
    result: dict[str, Any],
    attempt: dict[str, Any],
) -> dict[str, Any]:
    """Fail closed for graph-bound Results and return root EvidenceLink capabilities."""
    graph_id = attempt.get("obligation_graph_id")
    if graph_id is None:
        if any(
            field in result
            for field in (
                "obligation_graph_id",
                "root_obligation_id",
                "statement_sha256",
                "evidence_link_ids",
            )
        ):
            raise ObligationError("legacy Attempt 不得引用 ObligationGraph Result 字段")
        return {"required": False, "capabilities": set(), "closure": None}
    state = load_obligation_state(project_root)
    graph = state["graphs"].get(graph_id)
    if graph is None:
        raise ObligationError(f"Result 所需 ObligationGraph 不存在：{graph_id}")
    closure = derive_obligation_closure(project_root, graph_id, state=state)
    if closure["root_status"] == "conflict":
        raise ObligationConflict("root proof 与 counterexample 同时闭合")
    if result.get("obligation_graph_id") != graph_id:
        raise ObligationError("Result obligation_graph_id 与 Attempt 不一致")
    root_id = graph["root_obligation_id"]
    root_obligation = state["obligations_by_graph"][graph_id][root_id]
    if result.get("root_obligation_id") != root_id:
        raise ObligationError("Result root_obligation_id 不一致")
    if result.get("statement_sha256") != root_obligation["statement_sha256"]:
        raise ObligationError("Result statement_sha256 已失效")
    expected_root_status = {
        "proof": "proof_closed",
        "counterexample": "counterexample_closed",
    }.get(result.get("kind"))
    if expected_root_status is None or closure["root_status"] != expected_root_status:
        raise ObligationError(
            f"Result kind={result.get('kind')} 与 root closure={closure['root_status']} 不一致"
        )
    root_node = next(
        item for item in closure["nodes"] if item["obligation_id"] == root_id
    )
    winning_candidates = (
        root_node["verified_proof_candidates"]
        if result["kind"] == "proof"
        else root_node["verified_counterexample_candidates"]
    )
    selected_ids = result.get("evidence_link_ids", [])
    if not selected_ids:
        raise ObligationError("graph-bound Result 必须引用 root EvidenceLink")
    allowed_links: set[str] = set()
    for candidate_id in winning_candidates:
        allowed_links.update(root_node["accepted_evidence_links"].get(candidate_id, []))
    if not set(selected_ids).issubset(allowed_links):
        raise ObligationError("Result 引用了 stale、invalidated、非独立或非 root EvidenceLink")
    capabilities = {
        state["link_receipts"][link_id]["capability"] for link_id in selected_ids
    }
    return {"required": True, "capabilities": capabilities, "closure": closure}


def write_closure_snapshot(project_root: Path, graph_id: str) -> dict[str, str]:
    """Write a content-addressed derived closure view; truth remains in JSONL ledgers."""
    closure = derive_obligation_closure(project_root, graph_id)
    encoded = (json.dumps(closure, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    digest = hashlib.sha256(encoded).hexdigest()
    locator = (
        "research/artifacts/derived/obligation-closures/"
        f"{graph_id.removeprefix('graph:')}/{digest}.json"
    )
    path = project_root / locator
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file():
        if path.read_bytes() != encoded:
            raise ObligationError(f"closure snapshot 已存在且内容不同：{locator}")
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
    return {"locator": locator, "sha256": digest}


def validate_obligation_records(project_root: Path) -> list[str]:
    try:
        state = load_obligation_state(project_root)
        for graph_id in sorted(set(state["current_graph_by_attempt"].values())):
            derive_obligation_closure(project_root, graph_id, state=state)
    except ObligationError as exc:
        return [str(exc)]
    return []
