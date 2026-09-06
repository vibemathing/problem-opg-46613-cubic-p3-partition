"""Structured semantic-review receipts for obligation candidates."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .evidence import EvidenceError, create_obligation_evidence_receipt, sha256_file
from .obligations import ObligationError, load_obligation_state


class SemanticReviewError(RuntimeError):
    """A semantic review is malformed or targets a different statement."""


def _review_path(project_root: Path, locator: str) -> Path:
    pure = PurePosixPath(locator)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or "\\" in locator
        or pure.parts[:2] != ("research", "artifacts")
    ):
        raise SemanticReviewError("semantic review 必须位于 research/artifacts")
    path = project_root.joinpath(*pure.parts)
    try:
        path.resolve(strict=True).relative_to(project_root.resolve())
    except (OSError, ValueError) as exc:
        raise SemanticReviewError("semantic review 不存在或逃逸 project root") from exc
    if path.is_symlink() or not path.is_file():
        raise SemanticReviewError("semantic review 必须是 regular file")
    return path


def create_semantic_review_evidence(
    *,
    project_root: Path,
    review_locator: str,
    evidence_id: str,
) -> dict[str, Any]:
    """Validate one review artifact and return a receipt plus uncommitted EvidenceLink."""
    project_root = project_root.resolve()
    path = _review_path(project_root, review_locator)
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(
            (project_root / "research/schema/semantic-review.schema.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise SemanticReviewError("无法读取 semantic review 或 schema") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(review),
        key=lambda item: list(item.path),
    )
    if errors:
        raise SemanticReviewError(f"semantic review schema 无效：{errors[0].message}")
    try:
        state = load_obligation_state(project_root)
    except ObligationError as exc:
        raise SemanticReviewError(str(exc)) from exc
    graph = state["graphs"].get(review["graph_id"])
    candidate = state["candidates"].get(review["candidate_id"])
    if graph is None or candidate is None:
        raise SemanticReviewError("semantic review 引用未知 graph/candidate")
    obligation = state["obligations_by_graph"][graph["graph_id"]].get(
        review["obligation_id"]
    )
    if obligation is None:
        raise SemanticReviewError("semantic review 引用未知 obligation")
    expected = {
        "problem_id": candidate["problem_id"],
        "attempt_id": candidate["attempt_id"],
        "graph_id": candidate["graph_id"],
        "obligation_id": candidate["obligation_id"],
        "candidate_id": candidate["candidate_id"],
        "problem_contract_sha256": graph["problem_contract_sha256"],
        "statement_sha256": obligation["statement_sha256"],
    }
    if any(review.get(key) != value for key, value in expected.items()):
        raise SemanticReviewError("semantic review subject 或 statement digest 已失效")
    try:
        receipt = create_obligation_evidence_receipt(
            project_root=project_root,
            graph=graph,
            candidate=candidate,
            evidence_id=evidence_id,
            capability="statement_faithfulness",
            verdict=review["verdict"],
            verifier=review["reviewer"],
            checked_at=review["reviewed_at"],
            output_locator=review_locator,
            command=["vibe-mathing", "structured-semantic-review"],
            executor="in_process",
            native_status="accepted" if review["verdict"] != "undetermined" else "incomplete",
            inputs=[{"locator": review_locator, "sha256": sha256_file(path)}],
        )
    except EvidenceError as exc:
        raise SemanticReviewError(str(exc)) from exc
    link_id = f"evidence-link:{evidence_id.removeprefix('evidence:')}"
    return {
        "receipt": receipt,
        "evidence_link": {
            "schema_version": "1.0.0",
            "evidence_link_id": link_id,
            "graph_id": graph["graph_id"],
            "obligation_id": obligation["obligation_id"],
            "candidate_id": candidate["candidate_id"],
            "receipt": {"locator": receipt["locator"], "sha256": receipt["sha256"]},
            "invalidates": [],
            "linked_at": review["reviewed_at"],
        },
    }
