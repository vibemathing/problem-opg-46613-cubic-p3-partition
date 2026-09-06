"""Fail-closed helpers for the candidate-only Web GPT GitHub channel."""
from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

HEX64 = re.compile(r"^[0-9a-f]{64}$")
SAFE_RELATIVE = re.compile(r"^[A-Za-z0-9._/-]+$")
PRIVATE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-token", re.compile(r"\b(?:github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]{20,})\b")),
    ("authorization-header", re.compile(r"(?im)^\s*authorization\s*:\s*\S+")),
    ("cookie-header", re.compile(r"(?im)^\s*cookie\s*:\s*\S+")),
    ("private-posix-path", re.compile(r"(?:^|[\s'\"`])/(?:home|root|srv|tmp)/[^\s'\"`]+")),
    ("private-windows-path", re.compile(r"(?i)\b[A-Z]:\\Users\\[^\s'\"`]+")),
    ("session-id", re.compile(r"(?i)\b(?:session[_ -]?id|codex resume)\b")),
)
PROHIBITED_PACKET_KEYS = {
    "outcome",
    "result_id",
    "solution_id",
    "evidence_link_id",
    "kernel_checked",
    "independent",
    "result_admission",
}


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"expected JSON object at {path}:{number}")
        records.append(value)
    return records


def validate_schema(instance: Any, schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def normalize_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or "\\" in value
        or not SAFE_RELATIVE.fullmatch(value)
    ):
        raise ValueError(f"unsafe repository-relative path: {value!r}")
    normalized = path.as_posix()
    if normalized.startswith("/") or normalized != value:
        raise ValueError(f"non-canonical repository-relative path: {value!r}")
    return normalized


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def scan_private_text(text: str) -> list[str]:
    return [label for label, pattern in PRIVATE_PATTERNS if pattern.search(text)]


def scan_prohibited_keys(value: Any, prefix: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in PROHIBITED_PACKET_KEYS:
                errors.append(f"prohibited packet key {prefix}.{key}")
            errors.extend(scan_prohibited_keys(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(scan_prohibited_keys(child, f"{prefix}[{index}]"))
    return errors


def load_problem(root: Path) -> dict[str, Any]:
    records = load_jsonl(root / "problem-library/records/canonical-problems.jsonl")
    if len(records) != 1:
        raise ValueError(f"expected exactly one canonical Problem, found {len(records)}")
    return records[0]


def snapshot_file_sha256(root: Path) -> str:
    path = root / "HARNESS_SNAPSHOT.json"
    if not path.is_file() or path.is_symlink():
        raise ValueError("HARNESS_SNAPSHOT.json is missing or unsafe")
    return sha256_file(path)


def find_graph(root: Path, graph_id: str) -> dict[str, Any] | None:
    for record in load_jsonl(root / "research/records/obligation-graphs.jsonl"):
        if record.get("graph_id") == graph_id:
            return record
    return None


def find_obligation(graph: dict[str, Any], obligation_id: str) -> dict[str, Any] | None:
    for obligation in graph.get("obligations", []):
        if isinstance(obligation, dict) and obligation.get("obligation_id") == obligation_id:
            return obligation
    return None


def candidate_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".json": "application/json",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".lean": "text/x-lean",
        ".py": "text/x-python",
        ".csv": "text/csv",
    }.get(suffix, "application/octet-stream")


def _validate_regular_file(root: Path, relative: str, max_bytes: int) -> tuple[Path | None, list[str]]:
    errors: list[str] = []
    try:
        normalized = normalize_relative_path(relative)
    except ValueError as exc:
        return None, [str(exc)]
    path = root / normalized
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None, [f"candidate path missing or escapes root: {relative}"]
    if path.is_symlink() or not path.is_file():
        errors.append(f"candidate path is not a regular file: {relative}")
    elif path.stat().st_size > max_bytes:
        errors.append(f"candidate file exceeds {max_bytes} bytes: {relative}")
    elif path.stat().st_mode & 0o111:
        errors.append(f"candidate file must not be executable: {relative}")
    return path, errors


def validate_packet(root: Path, packet_path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    root = root.resolve()
    errors: list[str] = []
    try:
        packet = load_json(packet_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, [f"cannot load packet {packet_path}: {exc}"]

    schema_path = root / "research/schema/web-attempt-packet.schema.json"
    if not schema_path.is_file():
        return packet, ["missing web-attempt-packet schema"]
    errors.extend(f"schema: {message}" for message in validate_schema(packet, schema_path))
    errors.extend(scan_prohibited_keys(packet))
    errors.extend(f"privacy: {label}" for label in scan_private_text(json.dumps(packet, ensure_ascii=False)))

    try:
        profile = load_json(root / "WEB_CHANNEL_PROFILE.json")
        snapshot = load_json(root / "HARNESS_SNAPSHOT.json")
        problem = load_problem(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return packet, errors + [str(exc)]

    if packet.get("channel") != profile.get("channel_id"):
        errors.append("packet channel does not match WEB_CHANNEL_PROFILE")
    if packet.get("repository") != snapshot.get("repository"):
        errors.append("packet repository does not match Harness snapshot")
    snapshot_identity = snapshot.get("repository_identity", {})
    expected_packet_identity = {
        key: snapshot_identity.get(key)
        for key in ("binding_state", "database_id", "node_id", "default_branch")
    }
    if packet.get("repository_identity") != expected_packet_identity:
        errors.append("packet repository identity does not match Harness snapshot")
    if packet.get("problem_id") != problem.get("problem_id"):
        errors.append("packet problem_id does not match canonical Problem")
    contract_digest = canonical_json_sha256(problem)
    if packet.get("problem_contract_sha256") != contract_digest:
        errors.append("packet ProblemContract digest mismatch")
    try:
        snapshot_digest = snapshot_file_sha256(root)
    except ValueError as exc:
        errors.append(str(exc))
        snapshot_digest = None
    if snapshot_digest and packet.get("harness_snapshot_sha256") != snapshot_digest:
        errors.append("packet Harness snapshot digest mismatch")
    importer_path = root / "scripts/import_web_attempt.py"
    if not importer_path.is_file() or importer_path.is_symlink():
        errors.append("trusted importer policy is missing or unsafe")
    elif packet.get("importer_policy_sha256") != sha256_file(importer_path):
        errors.append("packet trusted importer policy digest mismatch")

    attempts = {record.get("attempt_id"): record for record in load_jsonl(root / "research/records/attempts.jsonl")}
    attempt = attempts.get(packet.get("attempt_id"))
    if attempt is None:
        errors.append("packet attempt_id is not pre-admitted")
    else:
        for field in ("problem_id", "route_id", "obligation_graph_id"):
            expected_key = {"obligation_graph_id": "graph_id"}.get(field, field)
            if field in attempt and attempt.get(field) != packet.get(expected_key):
                errors.append(f"packet {expected_key} does not match Attempt {field}")

    graph = find_graph(root, str(packet.get("graph_id", "")))
    obligation: dict[str, Any] | None = None
    if graph is None:
        errors.append("packet graph_id does not exist")
    else:
        for key in ("problem_id", "attempt_id", "route_id"):
            if graph.get(key) != packet.get(key):
                errors.append(f"packet {key} does not match ObligationGraph")
        if graph.get("problem_contract_sha256") != contract_digest:
            errors.append("ObligationGraph ProblemContract digest mismatch")
        obligation = find_obligation(graph, str(packet.get("obligation_id", "")))
        if obligation is None:
            errors.append("packet obligation_id does not exist in graph")

    failed_routes = {record.get("route_id") for record in load_jsonl(root / "research/records/failed-routes.jsonl")}
    if packet.get("route_id") in failed_routes:
        errors.append("packet repeats a registered failed route")

    transport = packet.get("transport", {})
    if isinstance(transport, dict):
        pr_number = transport.get("pull_request_number")
        pr_url = transport.get("pull_request_url")
        if (pr_number is None) != (pr_url is None):
            errors.append("pull_request_number and pull_request_url must both be null or non-null")
        repository = packet.get("repository")
        issue_number = transport.get("issue_number")
        if repository and issue_number and transport.get("issue_url") != f"https://github.com/{repository}/issues/{issue_number}":
            errors.append("issue_url does not match repository and issue_number")
        if repository and pr_number and pr_url != f"https://github.com/{repository}/pull/{pr_number}":
            errors.append("pull_request_url does not match repository and pull_request_number")
        branch = str(transport.get("branch", ""))
        prefix = str(profile.get("branch_policy", {}).get("prefix", "web/attempt-"))
        if not branch.startswith(prefix):
            errors.append("packet transport branch violates candidate branch policy")

    max_file_bytes = 1_048_576
    candidate_ids: set[str] = set()
    for candidate in packet.get("candidate_artifacts", []):
        if not isinstance(candidate, dict):
            continue
        candidate_id = str(candidate.get("candidate_id", ""))
        if candidate_id in candidate_ids:
            errors.append(f"duplicate candidate_id in packet: {candidate_id}")
        candidate_ids.add(candidate_id)
        if obligation is not None and candidate.get("kind") not in obligation.get("acceptance", {}).get("allowed_candidate_kinds", []):
            errors.append(f"candidate kind is not allowed by obligation: {candidate.get('kind')}")
        locator = str(candidate.get("locator", ""))
        if not matches_any(locator, profile.get("allowed_repository_write_paths", [])):
            errors.append(f"candidate locator is outside allowed write paths: {locator}")
        if matches_any(locator, profile.get("prohibited_repository_write_paths", [])):
            errors.append(f"candidate locator is prohibited: {locator}")
        candidate_path, path_errors = _validate_regular_file(root, locator, max_file_bytes)
        errors.extend(path_errors)
        if candidate_path and candidate_path.is_file():
            if sha256_file(candidate_path) != candidate.get("sha256"):
                errors.append(f"candidate digest mismatch: {locator}")
            try:
                text = candidate_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"binary candidate artifact is forbidden: {locator}")
            else:
                errors.extend(f"privacy in {locator}: {label}" for label in scan_private_text(text))

    repository = packet.get("repository")
    for ref in packet.get("source_refs", []):
        if not isinstance(ref, dict) or ref.get("repository") != repository:
            continue
        relative = str(ref.get("path", ""))
        try:
            normalized = normalize_relative_path(relative)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        path = root / normalized
        if not path.exists() or path.is_symlink():
            errors.append(f"local source ref does not exist or is unsafe: {relative}")

    if obligation is not None:
        statement_digest = obligation.get("statement_sha256")
        if not HEX64.fullmatch(str(statement_digest or "")):
            errors.append("active obligation has invalid statement digest")
        allowed_capabilities = set(obligation.get("acceptance", {}).get("required_capabilities", []))
        requested_capabilities = set(packet.get("requested_verification", []))
        if not requested_capabilities.issubset(allowed_capabilities):
            errors.append("packet requests capabilities outside obligation acceptance")

    return packet, errors


def packet_files(root: Path) -> list[Path]:
    inbox = root / "research/artifacts/web-inbox"
    if not inbox.exists():
        return []
    return sorted(path for path in inbox.rglob("*.json") if path.is_file() and not path.is_symlink())
