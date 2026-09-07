#!/usr/bin/env python3
"""Synthetic P0 attacks for Obligation DAG -> Candidate -> EvidenceLink -> closure."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from vibe_mathing.bundle import BundleConflict, derive_research_bundle
from vibe_mathing.evidence import create_obligation_evidence_receipt
from vibe_mathing.lean_obligation import (
    _toolchain_fingerprint,
    verify_lean_obligation,
)
from vibe_mathing.obligations import (
    canonical_json_sha256,
    derive_obligation_closure,
    statement_sha256,
    validate_obligation_records,
)
from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded
from vibe_mathing.semantic_review import create_semantic_review_evidence

from validate_research_spaces import qualifies_as_solution


ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-09-05T00:00:00Z"
SCHEMAS = (
    "attempt.schema.json",
    "candidate-artifact.schema.json",
    "evidence-link.schema.json",
    "evidence-receipt.schema.json",
    "lean-obligation-request.schema.json",
    "obligation-graph.schema.json",
    "research-bundle.schema.json",
    "semantic-review.schema.json",
    "verifier-registry.schema.json",
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values),
        encoding="utf-8",
    )


def base_registry(extra: list[dict] | None = None) -> dict:
    principals = [
        {
            "id": "web-generator",
            "role": "generator",
            "trust_domain": "web-generator",
            "policy": None,
            "capabilities": [],
        },
        {
            "id": "synthetic-kernel",
            "role": "verifier",
            "trust_domain": "synthetic-kernel",
            "policy": "test-fixture-v1",
            "capabilities": ["kernel_check"],
        },
        {
            "id": "synthetic-axiom-auditor",
            "role": "verifier",
            "trust_domain": "synthetic-audit",
            "policy": "test-fixture-v1",
            "capabilities": ["axiom_escape_audit"],
        },
        {
            "id": "semantic-reviewer",
            "role": "verifier",
            "trust_domain": "semantic-review",
            "policy": "structured-semantic-review-v1",
            "capabilities": ["statement_faithfulness"],
        },
    ]
    principals.extend(extra or [])
    return {"schema_version": "1.0.0", "principals": principals}


def problem() -> dict:
    return {
        "schema_version": "1.0.0",
        "problem_id": "problem:synthetic-obligation",
        "title": "Synthetic obligation closure",
        "aliases": [],
        "statement": {"text": "Prove the synthetic root claim.", "language": "en", "version": 1},
        "domain": {"description": "finite synthetic objects", "objects": ["synthetic object"]},
        "quantifiers": [{"kind": "forall", "variables": ["x"], "domain": "synthetic objects"}],
        "definitions": [],
        "assumptions": [],
        "allowed_axioms": [],
        "msc": ["03B30"],
        "sources": [
            {
                "source": "synthetic fixture",
                "source_record_id": None,
                "url": "https://example.invalid/synthetic-obligation",
                "retrieved_at": STAMP,
            }
        ],
        "acceptance": {"policy": "solution-admission-v1"},
        "constraints": {
            "allowed_methods": ["proof", "formalization"],
            "allowed_adapters": [],
            "max_attempts": 10,
            "runtime": {
                "max_transitions": 16,
                "max_retries": 2,
                "timeout_seconds": 30,
                "max_output_bytes": 1048576,
            },
        },
        "lifecycle": "active",
        "created_at": STAMP,
        "updated_at": STAMP,
    }


def prepare_project(root: Path, *, registry: dict | None = None) -> dict:
    for name in SCHEMAS:
        target = root / "research/schema" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "research/schema" / name, target)
    (root / "problem-library/schema").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "problem-library/schema/canonical-problem.schema.json",
        root / "problem-library/schema/canonical-problem.schema.json",
    )
    (root / "result-library/schema").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        ROOT / "result-library/schema/result.schema.json",
        root / "result-library/schema/result.schema.json",
    )
    value = problem()
    contract_digest = canonical_json_sha256(value)
    attempt = {
        "attempt_id": "attempt:synthetic-route",
        "problem_id": value["problem_id"],
        "route_id": "route:synthetic-route",
        "problem_contract_sha256": contract_digest,
        "obligation_graph_id": "graph:synthetic-route-v1",
        "generator": "web-generator",
        "objective": "Close one immutable synthetic obligation DAG.",
        "method": "proof",
        "lifecycle": "running",
        "started_at": STAMP,
        "completed_at": None,
        "inputs": [],
        "claims": [],
        "artifacts": [],
    }
    write_jsonl(root / "problem-library/records/canonical-problems.jsonl", [value])
    write_jsonl(root / "problem-library/records/problems.jsonl", [])
    write_jsonl(root / "research/records/attempts.jsonl", [attempt])
    write_jsonl(root / "research/records/obligation-graphs.jsonl", [])
    write_jsonl(root / "research/records/candidate-artifacts.jsonl", [])
    write_jsonl(root / "research/records/evidence-links.jsonl", [])
    write_jsonl(root / "result-library/records/results.jsonl", [])
    write_json(
        root / "result-library/indexes/solutions.json",
        {"schema_version": "2.0.0", "result_ids": []},
    )
    write_json(root / "research/verifiers.json", registry or base_registry())
    return {"problem": value, "attempt": attempt, "contract_digest": contract_digest}


def make_statement(label: str, *, formal: str | None = None) -> dict:
    return {"text": f"Synthetic claim {label}", "language": "en", "formal_declaration": formal}


def make_graph(context: dict, dependencies: dict[str, list[str]]) -> dict:
    cards = []
    for obligation_id, deps in dependencies.items():
        statement = make_statement(obligation_id)
        cards.append(
            {
                "obligation_id": obligation_id,
                "kind": "root_claim" if obligation_id == "obligation:root" else "lemma",
                "statement": statement,
                "statement_sha256": statement_sha256(statement),
                "dependencies": deps,
                "acceptance": {
                    "required_capabilities": [
                        "kernel_check",
                        "axiom_escape_audit",
                        "statement_faithfulness",
                    ],
                    "allowed_candidate_kinds": ["proof", "counterexample", "formalization"],
                },
                "source_refs": ["problem-library/records/canonical-problems.jsonl"],
            }
        )
    return {
        "schema_version": "1.0.0",
        "graph_id": context["attempt"]["obligation_graph_id"],
        "problem_id": context["problem"]["problem_id"],
        "attempt_id": context["attempt"]["attempt_id"],
        "route_id": context["attempt"]["route_id"],
        "problem_contract_sha256": context["contract_digest"],
        "root_obligation_id": "obligation:root",
        "obligations": cards,
        "created_at": STAMP,
        "supersedes": None,
    }


def standard_dependencies() -> dict[str, list[str]]:
    return {
        "obligation:root": ["obligation:lemma-a", "obligation:lemma-b"],
        "obligation:lemma-a": ["obligation:leaf-a"],
        "obligation:lemma-b": ["obligation:leaf-b"],
        "obligation:leaf-a": [],
        "obligation:leaf-b": [],
    }


def install_graph(root: Path, graph: dict) -> None:
    write_jsonl(root / "research/records/obligation-graphs.jsonl", [graph])


def make_candidate(root: Path, graph: dict, obligation_id: str, kind: str) -> dict:
    suffix = obligation_id.removeprefix("obligation:")
    candidate_id = f"candidate:{suffix}-{kind}"
    locator = f"research/artifacts/candidates/{suffix}-{kind}.txt"
    artifact = root / locator
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(f"{candidate_id}\n", encoding="utf-8")
    obligation = next(item for item in graph["obligations"] if item["obligation_id"] == obligation_id)
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "graph_id": graph["graph_id"],
        "obligation_id": obligation_id,
        "problem_id": graph["problem_id"],
        "attempt_id": graph["attempt_id"],
        "statement_sha256": obligation["statement_sha256"],
        "kind": kind,
        "generator": "web-generator",
        "artifact": {
            "locator": locator,
            "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            "media_type": "text/plain",
        },
        "source_refs": ["problem-library/records/canonical-problems.jsonl"],
        "created_at": STAMP,
    }


def evidence_link(root: Path, graph: dict, candidate: dict, capability: str, verifier: str) -> dict:
    suffix = capability.replace("_", "-")
    output_locator = (
        f"research/artifacts/outputs/synthetic/{candidate['candidate_id'].removeprefix('candidate:')}-{suffix}.json"
    )
    write_json(root / output_locator, {"capability": capability, "verdict": "accept"})
    evidence_id = f"evidence:{candidate['candidate_id'].removeprefix('candidate:')}.{suffix}"
    receipt = create_obligation_evidence_receipt(
        project_root=root,
        graph=graph,
        candidate=candidate,
        evidence_id=evidence_id,
        capability=capability,
        verdict="accept",
        verifier=verifier,
        checked_at=STAMP,
        output_locator=output_locator,
        command=["synthetic-verifier", capability],
        executor="in_process",
        native_status="accepted",
    )
    return {
        "schema_version": "1.0.0",
        "evidence_link_id": f"evidence-link:{candidate['candidate_id'].removeprefix('candidate:')}.{suffix}",
        "graph_id": graph["graph_id"],
        "obligation_id": candidate["obligation_id"],
        "candidate_id": candidate["candidate_id"],
        "receipt": {"locator": receipt["locator"], "sha256": receipt["sha256"]},
        "invalidates": [],
        "linked_at": STAMP,
    }


def semantic_link(root: Path, graph: dict, candidate: dict) -> dict:
    suffix = candidate["candidate_id"].removeprefix("candidate:")
    locator = f"research/artifacts/semantic-reviews/{suffix}.json"
    review = {
        "schema_version": "1.0.0",
        "problem_id": graph["problem_id"],
        "attempt_id": graph["attempt_id"],
        "graph_id": graph["graph_id"],
        "obligation_id": candidate["obligation_id"],
        "candidate_id": candidate["candidate_id"],
        "problem_contract_sha256": graph["problem_contract_sha256"],
        "statement_sha256": candidate["statement_sha256"],
        "reviewer": "semantic-reviewer",
        "reviewed_at": STAMP,
        "checks": {
            "domain": "accept",
            "quantifiers": "accept",
            "definitions": "accept",
            "assumptions": "accept",
            "claim_strength": "accept",
            "source_alignment": "accept",
        },
        "verdict": "accept",
        "issues": [],
        "rationale": "Synthetic independent semantic fixture.",
    }
    write_json(root / locator, review)
    return create_semantic_review_evidence(
        project_root=root,
        review_locator=locator,
        evidence_id=f"evidence:{suffix}.semantic",
    )["evidence_link"]


def close_candidates(root: Path, graph: dict, candidates: list[dict]) -> list[dict]:
    write_jsonl(root / "research/records/candidate-artifacts.jsonl", candidates)
    links: list[dict] = []
    for candidate in candidates:
        links.append(evidence_link(root, graph, candidate, "kernel_check", "synthetic-kernel"))
        links.append(
            evidence_link(
                root,
                graph,
                candidate,
                "axiom_escape_audit",
                "synthetic-axiom-auditor",
            )
        )
        links.append(semantic_link(root, graph, candidate))
    write_jsonl(root / "research/records/evidence-links.jsonl", links)
    return links


class ObligationHarnessTest(unittest.TestCase):
    def test_normal_and_dag_closure_result_and_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            graph = make_graph(context, standard_dependencies())
            install_graph(root, graph)
            candidates = [
                make_candidate(root, graph, identity, "proof")
                for identity in standard_dependencies()
            ]
            links = close_candidates(root, graph, candidates)
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "proof_closed")
            self.assertEqual(len(closure["nodes"]), 5)
            self.assertEqual(closure["open_obligation_ids"], [])
            root_candidate = next(
                item for item in candidates if item["obligation_id"] == graph["root_obligation_id"]
            )
            root_links = [
                item["evidence_link_id"]
                for item in links
                if item["candidate_id"] == root_candidate["candidate_id"]
            ]
            result = {
                "result_id": "result:synthetic-root-proof",
                "problem_id": graph["problem_id"],
                "attempt_id": graph["attempt_id"],
                "obligation_graph_id": graph["graph_id"],
                "root_obligation_id": graph["root_obligation_id"],
                "statement_sha256": next(
                    item["statement_sha256"]
                    for item in graph["obligations"]
                    if item["obligation_id"] == graph["root_obligation_id"]
                ),
                "evidence_link_ids": root_links,
                "kind": "proof",
                "claim": "Synthetic root is true.",
                "scope": "the frozen synthetic ProblemContract",
                "outcome": "established",
                "evidence": [],
                "created_at": STAMP,
            }
            write_jsonl(root / "result-library/records/results.jsonl", [result])
            self.assertTrue(
                qualifies_as_solution(
                    result,
                    {context["attempt"]["attempt_id"]: context["attempt"]},
                    project_root=root,
                )
            )
            bundle = derive_research_bundle(root, graph["problem_id"])
            self.assertEqual(bundle["disposition"], "solved")
            self.assertEqual(bundle["solution_view"], [result["result_id"]])
            self.assertEqual(bundle["obligation_graphs"][0]["closure"]["root_status"], "proof_closed")

    def test_direct_counterexample_closes_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            graph = make_graph(context, {"obligation:root": []})
            install_graph(root, graph)
            candidate = make_candidate(root, graph, "obligation:root", "counterexample")
            close_candidates(root, graph, [candidate])
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "counterexample_closed")
            self.assertEqual(closure["refuted_obligation_ids"], ["obligation:root"])

    def test_child_refutation_only_kills_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            dependencies = {
                "obligation:root": ["obligation:child"],
                "obligation:child": [],
            }
            graph = make_graph(context, dependencies)
            install_graph(root, graph)
            candidates = [
                make_candidate(root, graph, "obligation:root", "proof"),
                make_candidate(root, graph, "obligation:child", "counterexample"),
            ]
            close_candidates(root, graph, candidates)
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "route_refuted")
            self.assertEqual(closure["refuted_obligation_ids"], ["obligation:child"])
            self.assertNotEqual(closure["root_status"], "counterexample_closed")

    def test_unknown_dependency_and_cycle_fail_closed(self) -> None:
        cases = {
            "unknown": {
                "obligation:root": ["obligation:missing"],
            },
            "cycle": {
                "obligation:root": ["obligation:child"],
                "obligation:child": ["obligation:root"],
            },
        }
        for label, dependencies in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                context = prepare_project(root)
                graph = make_graph(context, dependencies)
                install_graph(root, graph)
                errors = validate_obligation_records(root)
                self.assertTrue(errors)
                self.assertIn("未知" if label == "unknown" else "循环", errors[0])

    def test_statement_change_stales_old_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            graph = make_graph(context, standard_dependencies())
            install_graph(root, graph)
            candidates = [
                make_candidate(root, graph, identity, "proof")
                for identity in standard_dependencies()
            ]
            close_candidates(root, graph, candidates)
            self.assertEqual(
                derive_obligation_closure(root, graph["graph_id"])["root_status"],
                "proof_closed",
            )
            changed = copy.deepcopy(graph)
            root_card = next(
                item for item in changed["obligations"] if item["obligation_id"] == "obligation:root"
            )
            root_card["statement"]["text"] = "Mutated root statement"
            root_card["statement_sha256"] = statement_sha256(root_card["statement"])
            install_graph(root, changed)
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "open")
            self.assertIn("candidate:root-proof", closure["stale_candidate_ids"])
            self.assertTrue(closure["stale_evidence_link_ids"])

    def test_proof_counterexample_conflict_blocks_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            graph = make_graph(context, {"obligation:root": []})
            install_graph(root, graph)
            close_candidates(
                root,
                graph,
                [
                    make_candidate(root, graph, "obligation:root", "proof"),
                    make_candidate(root, graph, "obligation:root", "counterexample"),
                ],
            )
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "conflict")
            with self.assertRaises(BundleConflict):
                derive_research_bundle(root, graph["problem_id"])

    def test_timeout_and_memory_bound_do_not_claim_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(RuntimeErrorBase, "超时"):
                execute_bounded(
                    [sys.executable, "-c", "import time; time.sleep(2)"],
                    cwd=root,
                    timeout_seconds=1,
                    max_output_bytes=4096,
                )
            try:
                outcome = execute_bounded(
                    [sys.executable, "-c", "x=bytearray(512*1024*1024); print(len(x))"],
                    cwd=root,
                    timeout_seconds=10,
                    max_output_bytes=65536,
                    max_memory_bytes=64 * 1024 * 1024,
                )
            except RuntimeErrorBase as exc:
                self.assertRegex(str(exc), "信号|内存|resource")
            else:
                self.assertNotEqual(outcome["exit_code"], 0)
                self.assertIn("MemoryError", outcome["stderr"])

    def test_lean_exit_zero_with_sorry_does_not_close(self) -> None:
        if shutil.which("lake") is None or shutil.which("lean") is None:
            self.skipTest("fixed Lean/Lake toolchain is not installed in this portable test job")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = prepare_project(root)
            graph = make_graph(context, {"obligation:root": []})
            root_card = graph["obligations"][0]
            root_card["statement"]["formal_declaration"] = "theorem target : True"
            root_card["statement_sha256"] = statement_sha256(root_card["statement"])
            install_graph(root, graph)
            fixture = root / "research/artifacts/candidates/lean-sorry-fixture"
            fixture.mkdir(parents=True)
            (fixture / "lean-toolchain").write_text(
                (ROOT / "fixtures/lean-proof/lean-toolchain").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (fixture / "lakefile.toml").write_text(
                'name = "ObligationFixture"\nversion = "0.1.0"\ndefaultTargets = ["ObligationFixture"]\n\n[[lean_lib]]\nname = "ObligationFixture"\n',
                encoding="utf-8",
            )
            source = fixture / "ObligationFixture.lean"
            source.write_text(
                "namespace ObligationFixture\n"
                "theorem target : True := by\n"
                "  sorry\n"
                "end ObligationFixture\n",
                encoding="utf-8",
            )
            candidate = {
                "schema_version": "1.0.0",
                "candidate_id": "candidate:lean-sorry-proof",
                "graph_id": graph["graph_id"],
                "obligation_id": "obligation:root",
                "problem_id": graph["problem_id"],
                "attempt_id": graph["attempt_id"],
                "statement_sha256": root_card["statement_sha256"],
                "kind": "formalization",
                "generator": "web-generator",
                "artifact": {
                    "locator": source.relative_to(root).as_posix(),
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "media_type": "text/x-lean",
                },
                "source_refs": ["problem-library/records/canonical-problems.jsonl"],
                "created_at": STAMP,
            }
            write_jsonl(root / "research/records/candidate-artifacts.jsonl", [candidate])
            toolchain, fingerprint = _toolchain_fingerprint(fixture)
            allowlist = [{"id": "lean", "version": toolchain, "fingerprint": fingerprint}]
            generic = [
                {
                    "id": "generic-lean-kernel",
                    "role": "verifier",
                    "trust_domain": "lean-kernel",
                    "policy": "lean-obligation-kernel-v1",
                    "capabilities": ["kernel_check"],
                    "toolchain_allowlist": allowlist,
                },
                {
                    "id": "generic-lean-axiom",
                    "role": "verifier",
                    "trust_domain": "lean-audit",
                    "policy": "lean-obligation-axiom-v1",
                    "capabilities": ["axiom_escape_audit"],
                    "toolchain_allowlist": allowlist,
                },
                {
                    "id": "generic-lean-statement",
                    "role": "verifier",
                    "trust_domain": "lean-statement",
                    "policy": "lean-obligation-statement-v1",
                    "capabilities": ["statement_identity"],
                    "toolchain_allowlist": allowlist,
                },
            ]
            write_json(root / "research/verifiers.json", base_registry(generic))
            request = {
                "schema_version": "1.0.0",
                "graph_id": graph["graph_id"],
                "obligation_id": "obligation:root",
                "candidate_id": candidate["candidate_id"],
                "fixture_root": fixture.relative_to(root).as_posix(),
                "module": "ObligationFixture",
                "source_files": ["ObligationFixture.lean"],
                "declaration": "ObligationFixture.target",
                "expected_declaration": "theorem target : True",
                "allowed_axioms": [],
                "budgets": {
                    "timeout_seconds": 120,
                    "max_output_bytes": 1048576,
                    "max_memory_bytes": 64 * 1024 * 1024 * 1024,
                },
                "verifiers": {
                    "kernel_check": "generic-lean-kernel",
                    "axiom_escape_audit": "generic-lean-axiom",
                    "statement_identity": "generic-lean-statement",
                },
            }
            report = verify_lean_obligation(project_root=root, request=request)
            self.assertTrue(report["decisions"]["kernel_check"], report)
            self.assertFalse(report["decisions"]["axiom_escape_audit"])
            write_jsonl(
                root / "research/records/evidence-links.jsonl",
                report["evidence_links"],
            )
            closure = derive_obligation_closure(root, graph["graph_id"])
            self.assertEqual(closure["root_status"], "open")


if __name__ == "__main__":
    unittest.main()
