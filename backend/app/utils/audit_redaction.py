"""Helpers for keeping audit metadata free of raw sensitive content."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


REDACTED = "[REDACTED]"

SENSITIVE_KEYWORDS = {
    "api_key",
    "apikey",
    "authorization",
    "auth_header",
    "bearer",
    "credential",
    "credentials",
    "password",
    "provider_secret",
    "refresh_token",
    "secret",
    "token",
}

CONTENT_KEYWORDS = {
    "brief",
    "campaign_brief",
    "content",
    "crm",
    "customer",
    "customer_record",
    "customer_records",
    "description",
    "document",
    "email",
    "file",
    "file_content",
    "graph_credentials",
    "name",
    "notes",
    "phone",
    "pii",
    "prompt",
    "raw",
    "raw_crm",
    "raw_record",
    "raw_records",
    "social_post",
    "text",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"ms_[A-Za-z0-9_\-]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]+", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9_\-]{32,}"),
]
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d[\s().-]?){8,}\d")


def _normalized_key(key: Any) -> str:
    return str(key).replace("-", "_").lower()


def is_sensitive_audit_key(key: Any) -> bool:
    normalized = _normalized_key(key)
    return normalized in SENSITIVE_KEYWORDS or any(part in normalized for part in SENSITIVE_KEYWORDS)


def is_content_audit_key(key: Any) -> bool:
    normalized = _normalized_key(key)
    return normalized in CONTENT_KEYWORDS or any(part in normalized for part in CONTENT_KEYWORDS)


def is_sensitive_audit_value(value: str) -> bool:
    if EMAIL_PATTERN.search(value) or PHONE_PATTERN.search(value):
        return True
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def redact_audit_metadata(value: Any) -> Any:
    """Return a JSON-safe copy with secrets, PII, and raw content redacted."""
    if isinstance(value, Mapping):
        clean: dict[str, Any] = {}
        for key, item in value.items():
            if is_sensitive_audit_key(key) or is_content_audit_key(key):
                clean[str(key)] = REDACTED
                continue
            clean[str(key)] = redact_audit_metadata(item)
        return clean

    if isinstance(value, list):
        return [redact_audit_metadata(item) for item in value[:50]]

    if isinstance(value, tuple):
        return [redact_audit_metadata(item) for item in value[:50]]

    if isinstance(value, str):
        if is_sensitive_audit_value(value) or len(value) > 180:
            return REDACTED
        return value

    if value is None or isinstance(value, (bool, int, float)):
        return value

    return str(value)


def audit_changed_fields(payload: Mapping[str, Any], allowed_fields: set[str] | None = None) -> list[str]:
    """Return changed field names only, excluding secret-like keys."""
    fields = []
    for key in payload.keys():
        field = str(key)
        if allowed_fields is not None and field not in allowed_fields:
            continue
        if is_sensitive_audit_key(field):
            continue
        fields.append(field)
    return sorted(fields)
