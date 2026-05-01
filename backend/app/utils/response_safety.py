"""Helpers for keeping client-facing API responses production-safe."""

from __future__ import annotations

import re
from typing import Any, List, Tuple


SENSITIVE_ERROR_KEYS = {"traceback", "stacktrace", "stack"}
TRACEBACK_MARKER = "Traceback (most recent call last)"
SECRET_PATTERNS = (
    (re.compile(r"sk-[A-Za-z0-9_\-]{8,}"), "sk-***"),
    (re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(password\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(token\s*[:=]\s*)([^\s,;]+)"), r"\1***"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)([^\s,;]+)"), r"\1***"),
)


def sanitize_api_payload(payload: Any) -> Tuple[Any, List[str]]:
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

    return _sanitize(payload), removed
