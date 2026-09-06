"""可恢复运行状态机、预算、超时与有界子进程执行。"""

from __future__ import annotations

import hashlib
import json
import os
import selectors
import signal
import subprocess
import time
import fcntl
import resource
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


TERMINAL_STATES = {"accepted", "rejected", "blocked", "failed", "cancelled"}
TRANSITIONS = {
    "planned": {"routed", "cancelled"},
    "routed": {"running", "cancelled"},
    "running": {"candidate_ready", "blocked", "failed", "cancelled"},
    "candidate_ready": {"verifying", "blocked", "failed", "cancelled"},
    "verifying": {"accepted", "rejected", "blocked", "failed", "cancelled"},
}
DEFAULT_BUDGETS = {
    "max_transitions": 16,
    "max_retries": 2,
    "timeout_seconds": 30,
    "max_output_bytes": 1_048_576,
}


class RuntimeErrorBase(RuntimeError):
    """运行状态或预算契约失败。"""


class InjectedInterruption(RuntimeErrorBase):
    """测试用可恢复中断，不改变真实业务逻辑。"""


class ArtifactHighWatermark(RuntimeErrorBase):
    """当前 producer 已到滚动水位；只应暂停该 producer。"""


class ArtifactBudgetExceeded(RuntimeErrorBase):
    """当前 producer 超出 artifact 配额；不得继续写入。"""


def artifact_usage(root: Path) -> dict[str, Any]:
    """统计一个 producer 的文件树，不跟随软链接，也不删除任何内容。"""
    total = 0
    files = 0
    errors: list[str] = []
    if root.is_symlink():
        return {"path": str(root), "bytes": 0, "files": 0, "errors": ["root path is a symlink"]}
    if not root.exists():
        return {"path": str(root), "bytes": 0, "files": 0, "errors": ["path does not exist"]}
    def on_walk_error(error: OSError) -> None:
        errors.append(str(error))

    for base, directories, names in os.walk(root, followlinks=False, onerror=on_walk_error):
        directories[:] = [name for name in directories if not Path(base, name).is_symlink()]
        for name in names:
            path = Path(base, name)
            try:
                if path.is_symlink() or not path.is_file():
                    continue
                total += path.stat().st_size
                files += 1
            except OSError as exc:
                errors.append(f"{path}: {exc}")
    return {"path": str(root), "bytes": total, "files": files, "errors": errors}


def check_artifact_budget(
    root: Path,
    budget: dict[str, int],
    *,
    additional_bytes: int = 0,
    additional_files: int = 0,
) -> dict[str, Any]:
    """Return a bounded quota decision before a producer emits more output."""
    required = ("max_bytes", "max_files")
    if any(not isinstance(budget.get(key), int) or budget[key] <= 0 for key in required):
        raise RuntimeErrorBase("artifact max_bytes/max_files must be positive integers")
    high_bytes = budget.get("high_watermark_bytes", budget.get("warn_bytes"))
    high_files = budget.get("high_watermark_files", budget.get("max_files"))
    if not isinstance(high_bytes, int) or high_bytes <= 0 or not isinstance(high_files, int) or high_files <= 0:
        raise RuntimeErrorBase("artifact high-watermark budgets must be positive integers")
    if high_bytes > budget["max_bytes"] or high_files > budget["max_files"]:
        raise RuntimeErrorBase("artifact high-watermark cannot exceed max budget")
    if additional_bytes < 0 or additional_files < 0:
        raise RuntimeErrorBase("artifact anticipated usage cannot be negative")
    usage = artifact_usage(root)
    if usage["errors"]:
        raise RuntimeErrorBase(f"artifact 目录不可安全计量：{usage['errors'][0]}")
    projected_bytes = usage["bytes"] + additional_bytes
    projected_files = usage["files"] + additional_files
    if projected_bytes > budget["max_bytes"] or projected_files > budget["max_files"]:
        state = "over_budget"
        action = "stop_current_producer"
    elif projected_bytes >= high_bytes or projected_files >= high_files:
        state = "high_watermark"
        action = "pause_current_producer"
    else:
        state = "normal"
        action = "continue"
    return {
        **usage,
        "state": state,
        "recommended_action": action,
        "projected_bytes": projected_bytes,
        "projected_files": projected_files,
        "max_bytes": budget["max_bytes"],
        "max_files": budget["max_files"],
        "high_watermark_bytes": high_bytes,
        "high_watermark_files": high_files,
    }


def _validate_state(project_root: Path, state: dict[str, Any]) -> None:
    schema_path = project_root / "research" / "schema" / "run-state.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeErrorBase(f"无法读取运行状态 schema：{schema_path}") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(state),
        key=lambda item: list(item.path),
    )
    if errors:
        raise RuntimeErrorBase(f"运行状态 schema 无效：{errors[0].message}")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_run_id(problem_id: str, adapter: str) -> str:
    value = hashlib.sha256(f"{problem_id}\0{adapter}\0v1".encode()).hexdigest()[:20]
    return f"run:{value}"


def run_path(project_root: Path, run_id: str) -> Path:
    safe_id = run_id.removeprefix("run:")
    if not safe_id or not all(character in "0123456789abcdef" for character in safe_id):
        raise RuntimeErrorBase("run_id 格式无效")
    return project_root / "research" / "runs" / safe_id / "run.json"


@contextmanager
def locked_run(project_root: Path, run_id: str) -> Any:
    """序列化同一 run 的所有副作用，避免并发状态与 artifact 竞争。"""
    path = run_path(project_root, run_id).with_name("run.lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    project_root = path.parents[3]
    _validate_state(project_root, payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    data = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    try:
        with temporary.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def create_run(
    project_root: Path,
    problem_id: str,
    adapter: str,
    budgets: dict[str, int] | None = None,
) -> dict[str, Any]:
    run_id = stable_run_id(problem_id, adapter)
    path = run_path(project_root, run_id)
    if path.is_file():
        return load_run(project_root, run_id)
    effective = {**DEFAULT_BUDGETS, **(budgets or {})}
    if any(not isinstance(value, int) or value <= 0 for value in effective.values()):
        raise RuntimeErrorBase("所有运行预算必须是正整数")
    created = now()
    state = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "problem_id": problem_id,
        "adapter": adapter,
        "status": "planned",
        "transition_count": 0,
        "retry_count": 0,
        "budgets": effective,
        "checkpoints": [{"status": "planned", "at": created}],
        "last_error": None,
        "created_at": created,
        "updated_at": created,
    }
    _write_atomic(path, state)
    return state


def load_run(project_root: Path, run_id: str) -> dict[str, Any]:
    path = run_path(project_root, run_id)
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeErrorBase(f"无法读取运行状态：{run_id}") from exc
    _validate_state(project_root, state)
    if state.get("run_id") != run_id:
        raise RuntimeErrorBase("运行状态身份或 schema_version 漂移")
    return state


def transition(project_root: Path, state: dict[str, Any], target: str) -> dict[str, Any]:
    current = state.get("status")
    if current in TERMINAL_STATES or target not in TRANSITIONS.get(current, set()):
        raise RuntimeErrorBase(f"非法运行状态转换：{current} -> {target}")
    count = state["transition_count"] + 1
    if count > state["budgets"]["max_transitions"]:
        raise RuntimeErrorBase("运行转换预算耗尽")
    changed = {**state, "status": target, "transition_count": count, "updated_at": now()}
    changed["checkpoints"] = [*state["checkpoints"], {"status": target, "at": changed["updated_at"]}]
    _write_atomic(run_path(project_root, state["run_id"]), changed)
    return changed


def execute_bounded(
    argv: list[str],
    *,
    cwd: Path,
    timeout_seconds: int,
    max_output_bytes: int,
    max_memory_bytes: int | None = None,
    max_cpu_seconds: int | None = None,
    artifact_root: Path | None = None,
    artifact_budget: dict[str, int] | None = None,
    artifact_check_interval_seconds: float = 1.0,
) -> dict[str, Any]:
    if not argv or any(not isinstance(item, str) or not item for item in argv):
        raise RuntimeErrorBase("子进程 argv 无效")
    if timeout_seconds <= 0 or max_output_bytes <= 0:
        raise RuntimeErrorBase("子进程 timeout 与输出预算必须为正数")
    for value, label in (
        (max_memory_bytes, "内存"),
        (max_cpu_seconds, "CPU 时间"),
    ):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise RuntimeErrorBase(f"子进程 {label}预算必须为正整数")
    if artifact_root is not None:
        if artifact_budget is None:
            raise RuntimeErrorBase("提供 artifact_root 时必须同时提供 artifact_budget")
        if artifact_check_interval_seconds <= 0:
            raise RuntimeErrorBase("artifact 检查间隔必须为正数")
        initial = check_artifact_budget(artifact_root, artifact_budget)
        if initial["state"] == "over_budget":
            raise ArtifactBudgetExceeded("producer 启动前已超过 artifact 配额")
        if initial["state"] == "high_watermark":
            raise ArtifactHighWatermark("producer 启动前已达到 artifact high-watermark")

    def apply_limits() -> None:
        if max_memory_bytes is not None:
            resource.setrlimit(resource.RLIMIT_AS, (max_memory_bytes, max_memory_bytes))
        if max_cpu_seconds is not None:
            resource.setrlimit(resource.RLIMIT_CPU, (max_cpu_seconds, max_cpu_seconds))

    process = subprocess.Popen(
        argv,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        preexec_fn=apply_limits if (max_memory_bytes is not None or max_cpu_seconds is not None) else None,
    )
    if process.stdout is None or process.stderr is None:
        raise RuntimeErrorBase("无法建立子进程输出通道")

    def terminate_group() -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()

    streams = {
        process.stdout: bytearray(),
        process.stderr: bytearray(),
    }
    selector = selectors.DefaultSelector()
    for stream in streams:
        selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout_seconds
    next_artifact_check = time.monotonic()
    try:
        while selector.get_map():
            if artifact_root is not None and time.monotonic() >= next_artifact_check:
                decision = check_artifact_budget(artifact_root, artifact_budget or {})
                next_artifact_check = time.monotonic() + artifact_check_interval_seconds
                if decision["state"] == "over_budget":
                    terminate_group()
                    raise ArtifactBudgetExceeded(
                        f"producer 超出 artifact 配额：{decision['bytes']} bytes/{decision['files']} files"
                    )
                if decision["state"] == "high_watermark":
                    terminate_group()
                    raise ArtifactHighWatermark(
                        f"producer 达到 artifact high-watermark：{decision['bytes']} bytes/{decision['files']} files"
                    )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                terminate_group()
                raise RuntimeErrorBase(f"子进程超时：{timeout_seconds}s")
            for key, _ in selector.select(timeout=min(remaining, 0.1)):
                stream = key.fileobj
                chunk = os.read(stream.fileno(), 65_536)
                if not chunk:
                    selector.unregister(stream)
                    continue
                buffer = streams[stream]
                buffer.extend(chunk)
                if sum(len(value) for value in streams.values()) > max_output_bytes:
                    terminate_group()
                    raise RuntimeErrorBase("子进程 stdout+stderr 超过总输出预算")
        return_code = process.wait()
        if artifact_root is not None:
            final_decision = check_artifact_budget(artifact_root, artifact_budget or {})
            if final_decision["state"] == "over_budget":
                raise ArtifactBudgetExceeded(
                    f"producer 完成时超出 artifact 配额：{final_decision['bytes']} bytes/{final_decision['files']} files"
                )
            if final_decision["state"] == "high_watermark":
                raise ArtifactHighWatermark(
                    f"producer 完成时达到 artifact high-watermark：{final_decision['bytes']} bytes/{final_decision['files']} files"
                )
    finally:
        selector.close()
        process.stdout.close()
        process.stderr.close()

    if return_code < 0:
        raise RuntimeErrorBase(f"子进程被信号终止：{-return_code}")
    stdout = bytes(streams[process.stdout])
    stderr = bytes(streams[process.stderr])
    return {
        "argv": argv,
        "exit_code": return_code,
        "stdout": stdout.decode(errors="replace"),
        "stderr": stderr.decode(errors="replace"),
    }


def record_retry(project_root: Path, state: dict[str, Any], error: str) -> dict[str, Any]:
    retries = state["retry_count"] + 1
    if retries > state["budgets"]["max_retries"]:
        raise RuntimeErrorBase("运行重试预算耗尽")
    changed = {**state, "retry_count": retries, "last_error": error, "updated_at": now()}
    _write_atomic(run_path(project_root, state["run_id"]), changed)
    return changed


def cancel_run(project_root: Path, run_id: str) -> dict[str, Any]:
    """在 run 互斥锁内执行显式取消；终态取消保持幂等。"""
    with locked_run(project_root, run_id):
        state = load_run(project_root, run_id)
        if state["status"] == "cancelled":
            return state
        current = state["status"]
        if current in TERMINAL_STATES or "cancelled" not in TRANSITIONS.get(current, set()):
            raise RuntimeErrorBase(f"非法运行状态转换：{current} -> cancelled")
        cancelled_at = now()
        changed = {
            **state,
            "status": "cancelled",
            "updated_at": cancelled_at,
            "last_error": "用户或监管器显式取消",
            "checkpoints": [
                *state["checkpoints"],
                {"status": "cancelled", "at": cancelled_at},
            ],
        }
        _write_atomic(run_path(project_root, run_id), changed)
        return changed
