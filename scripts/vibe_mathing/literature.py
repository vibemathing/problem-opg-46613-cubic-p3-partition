"""文献 provider registry、脱敏请求构造和显式 live 健康检查。"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


USER_AGENT = "vibe-mathing-cn/0.2 literature-provider-health"


class LiteratureProviderError(RuntimeError):
    """Provider registry、凭据或 live 请求不满足契约。"""


def load_provider_registry(project_root: Path) -> dict[str, dict[str, Any]]:
    """读取并验证 provider registry，返回按 ID 索引的只读配置。"""
    registry_path = project_root / "literature/providers.json"
    schema_path = project_root / "literature/schema/literature-providers.schema.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LiteratureProviderError("无法读取文献 provider registry 或 schema") from exc
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(registry),
        key=lambda item: list(item.path),
    )
    if errors:
        raise LiteratureProviderError(
            f"文献 provider registry schema 无效：{errors[0].message}"
        )
    providers: dict[str, dict[str, Any]] = {}
    for provider in registry["providers"]:
        provider_id = provider["id"]
        if provider_id in providers:
            raise LiteratureProviderError(f"重复 provider ID：{provider_id}")
        auth = provider["auth"]
        if auth["mode"] == "none" and any(
            auth[field] is not None for field in ("name", "env")
        ):
            raise LiteratureProviderError(f"{provider_id}: auth=none 不得声明凭据")
        if auth["mode"] == "none" and auth["required_for_live"]:
            raise LiteratureProviderError(
                f"{provider_id}: auth=none 不得要求 live 凭据"
            )
        if auth["mode"] != "none" and not auth["name"]:
            raise LiteratureProviderError(f"{provider_id}: auth 缺少 name")
        if auth["mode"] != "none" and not auth["env"]:
            raise LiteratureProviderError(f"{provider_id}: auth 缺少 env")
        contact = provider["contact"]
        if bool(contact["env"]) != bool(contact["query_parameter"]):
            raise LiteratureProviderError(
                f"{provider_id}: contact env 与 query_parameter 必须同时配置"
            )
        providers[provider_id] = provider
    return providers


def build_provider_request(
    provider: Mapping[str, Any],
    query: str,
    *,
    environ: Mapping[str, str],
    require_credentials: bool,
) -> tuple[urllib.request.Request, dict[str, Any]]:
    """构造真实请求和不含凭据值的审计摘要。"""
    if not query.strip():
        raise LiteratureProviderError("检索 query 不能为空")
    provider_id = str(provider["id"])
    parameters = dict(provider["extra_query"])
    parameters[str(provider["query_parameter"])] = query.strip()
    redacted_parameters = dict(parameters)
    headers = {"Accept": "application/json, application/atom+xml", "User-Agent": USER_AGENT}
    safe_headers = dict(headers)

    contact = provider["contact"]
    if contact["env"]:
        contact_value = environ.get(str(contact["env"]), "").strip()
        if contact_value:
            parameters[str(contact["query_parameter"])] = contact_value
            redacted_parameters[str(contact["query_parameter"])] = "<configured>"

    auth = provider["auth"]
    secret = ""
    if auth["env"]:
        secret = environ.get(str(auth["env"]), "").strip()
    if require_credentials and auth["required_for_live"] and not secret:
        raise LiteratureProviderError(
            f"{provider_id}: 缺少受信凭据条目 {auth['env']}"
        )
    if secret and auth["mode"] == "query":
        parameters[str(auth["name"])] = secret
        redacted_parameters[str(auth["name"])] = "<redacted>"
    elif secret and auth["mode"] == "header":
        headers[str(auth["name"])] = secret
        safe_headers[str(auth["name"])] = "<redacted>"

    url = f"{provider['base_url']}?{urllib.parse.urlencode(parameters)}"
    safe_url = f"{provider['base_url']}?{urllib.parse.urlencode(redacted_parameters)}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    summary = {
        "provider": provider_id,
        "url": safe_url,
        "headers": safe_headers,
        "timeout_seconds": provider["timeout_seconds"],
        "max_retries": provider["max_retries"],
        "response_format": provider["response_format"],
        "credential_env": auth["env"],
        "credential_configured": bool(secret),
    }
    return request, summary


def check_provider_live(
    provider: Mapping[str, Any],
    query: str,
    *,
    environ: Mapping[str, str],
) -> dict[str, Any]:
    """执行一次有界 live 请求；只读取前 1 KiB，不保存响应正文。"""
    request, summary = build_provider_request(
        provider, query, environ=environ, require_credentials=True
    )
    retries = int(provider["max_retries"])
    last_error = ""
    started = time.monotonic()
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(
                request, timeout=int(provider["timeout_seconds"])
            ) as response:
                status = getattr(response, "status", 200)
                response.read(1024)
            if not 200 <= status < 300:
                raise LiteratureProviderError(
                    f"{provider['id']}: HTTP status={status}"
                )
            return {
                **summary,
                "status": "PASS",
                "http_status": status,
                "attempts": attempt + 1,
                "duration_seconds": round(time.monotonic() - started, 3),
            }
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt == retries:
                break
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = type(exc).__name__
            if attempt == retries:
                break
        if attempt < retries:
            time.sleep(min(2**attempt, 2))
    raise LiteratureProviderError(
        f"{provider['id']}: live health 失败（{last_error or 'unknown'}）"
    )
