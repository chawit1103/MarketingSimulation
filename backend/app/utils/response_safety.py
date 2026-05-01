"""Helpers for keeping client-facing API responses production-safe."""

from __future__ import annotations

from typing import Any, List, Tuple


SENSITIVE_ERROR_KEYS = {"traceback", "stacktrace", "stack"}
TRACEBACK_MARKER = "Traceback (most recent call last)"


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
        if isinstance(value, str) and TRACEBACK_MARKER in value:
            removed.append(value)
            return "Internal server error"
        return value

    return _sanitize(payload), removed
