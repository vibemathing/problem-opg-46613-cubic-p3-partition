"""Problem、Attempt、Result 与 Solution View 的单机事务存储。"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator, FormatChecker


COLLECTIONS = {
    "problems": (
        "problem-library/records/canonical-problems.jsonl",
        "problem-library/schema/canonical-problem.schema.json",
        "problem_id",
    ),
    "attempts": (
        "research/records/attempts.jsonl",
        "research/schema/attempt.schema.json",
        "attempt_id",
    ),
    "results": (
        "result-library/records/results.jsonl",
        "result-library/schema/result.schema.json",
        "result_id",
    ),
}


class StoreError(RuntimeError):
    """事务、schema 或幂等契约失败。"""


def _parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise StoreError("时间戳必须是 ISO 8601 字符串")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise StoreError("时间戳必须是有效 ISO 8601 日期时间") from exc
    if parsed.tzinfo is None:
        raise StoreError("时间戳必须包含时区")
    return parsed.astimezone(timezone.utc)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class ResearchStore:
    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()
        self.lock_path = self.root / "research" / ".store.lock"
        self.journal_path = self.root / "research" / ".store-transaction.json"

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            self._recover_locked()
            yield

    def locked(self) -> Iterator[None]:
        """为跨 collection 的外部只读校验提供一致快照锁。"""
        return self._locked()

    def _paths(self, collection: str) -> tuple[Path, Path, str]:
        try:
            record_path, schema_path, id_field = COLLECTIONS[collection]
        except KeyError as exc:
            raise StoreError(f"未知 collection：{collection}") from exc
        return self.root / record_path, self.root / schema_path, id_field

    def read(self, collection: str) -> list[dict[str, Any]]:
        """在恢复任何未完成事务后读取一致快照。"""
        with self._locked():
            return self._read_unlocked(collection)

    def snapshot(self) -> dict[str, list[dict[str, Any]]]:
        """在同一锁内校验并返回三张真相表的一致快照。"""
        with self._locked():
            snapshot = {
                collection: self._read_unlocked(collection)
                for collection in COLLECTIONS
            }
            for collection, records in snapshot.items():
                self._validate(collection, records)
            self._validate_integrity_locked(snapshot)
            return snapshot

    def _read_unlocked(self, collection: str) -> list[dict[str, Any]]:
        path, _, _ = self._paths(collection)
        if not path.is_file():
            return []
        records: list[dict[str, Any]] = []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise StoreError(f"{path}:{number}: JSONL 无效") from exc
            if not isinstance(value, dict):
                raise StoreError(f"{path}:{number}: 记录不是对象")
            records.append(value)
        return records

    def _validate(self, collection: str, records: list[dict[str, Any]]) -> None:
        _, schema_path, id_field = self._paths(collection)
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise StoreError(f"无法读取 schema：{schema_path}") from exc
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        seen: set[str] = set()
        for index, record in enumerate(records, 1):
            errors = sorted(validator.iter_errors(record), key=lambda item: list(item.path))
            if errors:
                raise StoreError(f"{collection}:{index}: {errors[0].message}")
            record_id = record[id_field]
            if record_id in seen:
                raise StoreError(f"{collection}: 重复 ID：{record_id}")
            seen.add(record_id)

    def upsert(
        self,
        collection: str,
        record: dict[str, Any],
        *,
        fail_after_replace: int | None = None,
    ) -> bool:
        """按稳定 ID 幂等写入；相同 ID 不同内容拒绝覆盖。"""
        with self._locked():
            records = self._read_unlocked(collection)
            _, _, id_field = self._paths(collection)
            record_id = record.get(id_field)
            for current in records:
                if current.get(id_field) == record_id:
                    if current == record:
                        return False
                    raise StoreError(f"{collection}: ID 已存在且内容不同：{record_id}")
            records.append(record)
            self.commit({collection: records}, fail_after_replace=fail_after_replace, locked=True)
            return True

    def replace_problem(self, record: dict[str, Any]) -> None:
        """只允许 ProblemContract lifecycle 单向转换，其他契约字段保持冻结。"""
        transitions = {
            "draft": {"active", "withdrawn"},
            "active": {"withdrawn"},
            "withdrawn": set(),
        }
        with self._locked():
            records = self._read_unlocked("problems")
            for index, current in enumerate(records):
                if current.get("problem_id") != record.get("problem_id"):
                    continue
                old = current.get("lifecycle")
                new = record.get("lifecycle")
                frozen = {
                    key: value
                    for key, value in current.items()
                    if key not in {"lifecycle", "updated_at"}
                }
                proposed = {
                    key: value
                    for key, value in record.items()
                    if key not in {"lifecycle", "updated_at"}
                }
                if frozen != proposed or new not in transitions.get(old, set()):
                    raise StoreError(
                        f"ProblemContract 只允许 lifecycle 单向转换：{old} -> {new}"
                    )
                if _parse_timestamp(record.get("updated_at")) <= _parse_timestamp(
                    current.get("updated_at")
                ):
                    raise StoreError("ProblemContract lifecycle 转换必须推进 updated_at")
                records[index] = record
                break
            else:
                raise StoreError(f"Problem 不存在：{record.get('problem_id')}")
            self.commit({"problems": records}, locked=True)

    def replace_result(
        self, record: dict[str, Any], *, fail_after_replace: int | None = None
    ) -> None:
        """只允许 Result 追加 evidence 的版本化替换，不允许改写既有字段。"""
        with self._locked():
            records = self._read_unlocked("results")
            for index, current in enumerate(records):
                if current.get("result_id") != record.get("result_id"):
                    continue
                frozen = {
                    key: value
                    for key, value in current.items()
                    if key not in {"evidence", "outcome"}
                }
                proposed = {
                    key: value
                    for key, value in record.items()
                    if key not in {"evidence", "outcome"}
                }
                outcome_change = (current.get("outcome"), record.get("outcome"))
                allowed_outcome_change = outcome_change[0] == outcome_change[1] or (
                    outcome_change[0] in {"established", "refuted", "supported"}
                    and outcome_change[1] == "withdrawn"
                )
                if (
                    frozen != proposed
                    or not allowed_outcome_change
                    or record.get("evidence", [])[: len(current.get("evidence", []))]
                    != current.get("evidence", [])
                ):
                    raise StoreError("Result 只能在 evidence 账本尾部追加记录")
                records[index] = record
                break
            else:
                raise StoreError(f"Result 不存在：{record.get('result_id')}")
            self.commit({"results": records}, fail_after_replace=fail_after_replace, locked=True)

    def replace_attempt(self, record: dict[str, Any]) -> None:
        """按允许的 lifecycle 单调转换更新 Attempt。"""
        transitions = {
            "planned": {"running", "blocked", "failed"},
            "running": {"completed", "blocked", "failed"},
            "blocked": {"running", "failed"},
            "completed": set(),
            "failed": set(),
        }
        with self._locked():
            records = self._read_unlocked("attempts")
            for index, current in enumerate(records):
                if current.get("attempt_id") != record.get("attempt_id"):
                    continue
                old = current.get("lifecycle")
                new = record.get("lifecycle")
                if new != old and new not in transitions.get(old, set()):
                    raise StoreError(f"Attempt 非法状态转换：{old} -> {new}")
                records[index] = record
                break
            else:
                raise StoreError(f"Attempt 不存在：{record.get('attempt_id')}")
            self.commit({"attempts": records}, locked=True)

    def commit(
        self,
        changes: dict[str, list[dict[str, Any]]],
        *,
        fail_after_replace: int | None = None,
        locked: bool = False,
    ) -> None:
        if not locked:
            with self._locked():
                return self.commit(changes, fail_after_replace=fail_after_replace, locked=True)
        if "attempts" in changes:
            current_attempt_ids = {
                item["attempt_id"] for item in self._read_unlocked("attempts")
            }
            final_problems = changes.get("problems", self._read_unlocked("problems"))
            problems_by_id = {item["problem_id"]: item for item in final_problems}
            final_attempts = changes["attempts"]
            for attempt in final_attempts:
                if attempt.get("attempt_id") in current_attempt_ids:
                    continue
                problem = problems_by_id.get(attempt.get("problem_id"))
                if problem is None:
                    continue
                if problem.get("lifecycle") != "active":
                    raise StoreError("只有 active ProblemContract 允许创建新 Attempt")
                constraints = problem.get("constraints", {})
                if attempt.get("method") not in constraints.get("allowed_methods", []):
                    raise StoreError(
                        f"Attempt method={attempt.get('method')} 未被 ProblemContract 允许"
                    )
                problem_attempts = [
                    item
                    for item in final_attempts
                    if item.get("problem_id") == problem["problem_id"]
                ]
                if len(problem_attempts) > constraints.get("max_attempts", 0):
                    raise StoreError("ProblemContract 的 max_attempts 预算耗尽")
        for collection, records in changes.items():
            self._validate(collection, records)
        self._validate_integrity_locked(changes)
        prepared: list[dict[str, str]] = []
        transaction_id = hashlib.sha256(
            json.dumps(changes, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()[:16]
        for collection, records in changes.items():
            target, _, id_field = self._paths(collection)
            target.parent.mkdir(parents=True, exist_ok=True)
            ordered = sorted(records, key=lambda item: item[id_field])
            data = b"".join(
                (json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n").encode()
                for item in ordered
            )
            temporary = target.with_name(f".{target.name}.{transaction_id}.tmp")
            with temporary.open("wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            prepared.append(
                {
                    "target": str(target.relative_to(self.root)),
                    "temporary": str(temporary.relative_to(self.root)),
                    "sha256": _digest(data),
                }
            )
        journal = {
            "schema_version": "1.0.0",
            "transaction_id": transaction_id,
            "prepared": prepared,
        }
        journal_data = (json.dumps(journal, sort_keys=True, indent=2) + "\n").encode()
        journal_temporary = self.journal_path.with_suffix(".json.tmp")
        try:
            with journal_temporary.open("wb") as handle:
                handle.write(journal_data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(journal_temporary, self.journal_path)
        finally:
            journal_temporary.unlink(missing_ok=True)
        _fsync_directory(self.journal_path.parent)
        for count, item in enumerate(prepared, 1):
            os.replace(self.root / item["temporary"], self.root / item["target"])
            _fsync_directory((self.root / item["target"]).parent)
            if fail_after_replace == count:
                raise StoreError("故障注入：事务提交中断")
        self.journal_path.unlink()
        _fsync_directory(self.journal_path.parent)

    def recover(self) -> None:
        with self._locked():
            return

    def _recover_locked(self) -> None:
        if not self.journal_path.is_file():
            self.journal_path.with_suffix(".json.tmp").unlink(missing_ok=True)
            for record_path, _, _ in COLLECTIONS.values():
                target = self.root / record_path
                for orphan in target.parent.glob(f".{target.name}.*.tmp"):
                    orphan.unlink(missing_ok=True)
            return
        try:
            journal = json.loads(self.journal_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise StoreError("事务日志损坏，拒绝继续写入") from exc
        allowed_targets = {
            path for path, _, _ in COLLECTIONS.values()
        }
        prepared = journal.get("prepared")
        if journal.get("schema_version") != "1.0.0" or not isinstance(prepared, list):
            raise StoreError("事务日志契约无效，拒绝继续写入")
        for item in prepared:
            if not isinstance(item, dict) or item.get("target") not in allowed_targets:
                raise StoreError("事务日志包含未授权 target")
            target = self.root / item["target"]
            temporary = self.root / item["temporary"]
            if temporary.parent != target.parent or not temporary.name.startswith(
                f".{target.name}."
            ):
                raise StoreError("事务日志包含未授权暂存文件位置")
            if temporary.is_file():
                os.replace(temporary, target)
                _fsync_directory(target.parent)
            if not target.is_file() or _digest(target.read_bytes()) != item.get("sha256"):
                raise StoreError(f"事务恢复无法证明目标完整：{target}")
        self.journal_path.unlink()
        _fsync_directory(self.journal_path.parent)

    def _validate_integrity_locked(
        self, changes: dict[str, list[dict[str, Any]]]
    ) -> None:
        from validate_research_spaces import validate_cross_references

        final = {
            collection: changes.get(collection, self._read_unlocked(collection))
            for collection in COLLECTIONS
        }
        problem_ids = {item["problem_id"] for item in final["problems"]}
        attempt_ids = {item["attempt_id"] for item in final["attempts"]}
        errors: list[str] = []
        validate_cross_references(
            final["problems"],
            problem_ids,
            final["attempts"],
            attempt_ids,
            final["results"],
            errors,
            project_root=self.root,
        )
        if errors:
            raise StoreError(f"跨记录完整性失败：{errors[0]}")

    def rebuild_solution_view(self) -> list[str]:
        from validate_research_spaces import derive_solution_ids

        with self._locked():
            snapshot = {
                collection: self._read_unlocked(collection)
                for collection in COLLECTIONS
            }
            for collection, records in snapshot.items():
                self._validate(collection, records)
            self._validate_integrity_locked(snapshot)
            attempts = {item["attempt_id"]: item for item in snapshot["attempts"]}
            solution_ids = derive_solution_ids(
                snapshot["results"], attempts, project_root=self.root
            )
            payload = {
                "schema_version": "2.0.0",
                "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "result_ids": solution_ids,
            }
            path = self.root / "result-library" / "indexes" / "solutions.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()
            temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
            try:
                with temporary.open("wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, path)
                _fsync_directory(path.parent)
            finally:
                temporary.unlink(missing_ok=True)
        return solution_ids
