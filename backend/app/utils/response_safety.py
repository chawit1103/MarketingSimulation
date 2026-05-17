"""Helpers for keeping client-facing API responses production-safe."""

from __future__ import annotations

import re
from typing import Any, List, Tuple


SENSITIVE_ERROR_KEYS = {"traceback", "stacktrace", "stack"}
SENSITIVE_VALUE_KEYS = {
    "api_key",
    "apikey",
    "api-key",
    "password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "credential",
    "credentials",
    "authorization",
}
SENSITIVE_CONTENT_KEYS = {
    "brief",
    "campaignbrief",
    "campaign_brief",
    "brieftext",
    "brief_text",
    "simulationrequirement",
    "simulation_requirement",
    "documenttext",
    "document_text",
    "additionalcontext",
    "additional_context",
}
TRACEBACK_MARKER = "Traceback (most recent call last)"
SECRET_PATTERNS = (
    (re.compile(r"sk-[A-Za-z0-9_\-]{8,}"), "sk-***"),
    (re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(password\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(token\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)([^\s,;]+)"), r"\1***"),
)


def sanitize_api_payload(payload: Any, status_code: int | None = None) -> Tuple[Any, List[str]]:
    """Remove raw traceback/stack details from JSON payloads.

    Returns the sanitized payload and a list of removed values so callers can
    keep details in server logs without exposing them to clients.
    """
    removed: List[str] = []

    def _sanitize(value: Any) -> Any:
        if isinstance(value, dict):
            clean = {}
            for key, item in value.items():
                if str(key).lower() in SENSITIVE_ERROR_KEYS:
                    removed.append(str(item))
                    continue
                clean[key] = _sanitize(item)
            return clean
        if isinstance(value, list):
            return [_sanitize(item) for item in value]
        if isinstance(value, str):
            if TRACEBACK_MARKER in value:
                removed.append(value)
                return "Internal server error"
            redacted = value
            for pattern, replacement in SECRET_PATTERNS:
                redacted = pattern.sub(replacement, redacted)
            if redacted != value:
                removed.append("Redacted secret-like value from client response")
            return redacted
        return value

    sanitized = _sanitize(payload)
    if (
        status_code is not None
        and status_code >= 500
        and status_code != 501
        and isinstance(sanitized, dict)
        and isinstance(sanitized.get("error"), str)
    ):
        removed.append(f"Replaced 5xx client error string: {sanitized.get('error')}")
        sanitized["error"] = "Internal server error"
        sanitized.setdefault("code", "internal_error")

    return sanitized, removed


def redact_sensitive_payload(payload: Any) -> Any:
    """Redact credential-like fields before writing request data to logs."""
    def _redact(value: Any) -> Any:
        if isinstance(value, dict):
            clean = {}
            for key, item in value.items():
                normalized = str(key).replace("_", "").replace("-", "").lower()
                if normalized in {k.replace("_", "").replace("-", "") for k in SENSITIVE_VALUE_KEYS}:
                    clean[key] = "***" if item not in (None, "") else item
                elif normalized in {k.replace("_", "").replace("-", "") for k in SENSITIVE_CONTENT_KEYS}:
                    clean[key] = "***" if item not in (None, "") else item
                else:
                    clean[key] = _redact(item)
            return clean
        if isinstance(value, list):
            return [_redact(item) for item in value]
        if isinstance(value, str):
            redacted = value
            for pattern, replacement in SECRET_PATTERNS:
                redacted = pattern.sub(replacement, redacted)
            return redacted
        return value

    return _redact(payload)
