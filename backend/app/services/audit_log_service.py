"""Org-scoped JSONL audit logging for private pilot operations."""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from flask import g, has_request_context, request

from ..config import Config
from ..utils.audit_redaction import redact_audit_metadata
from ..utils.logger import get_logger


logger = get_logger("mirofish.audit")


AUDIT_EVENT_TYPES = {
    "login",
    "campaign_created",
    "campaign_updated",
    "campaign_deleted",
    "simulation_started",
    "simulation_stopped",
    "report_generation_started",
    "report_downloaded",
    "export_generated",
    "calibration_imported",
    "settings_updated",
}

_ORG_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def _safe_org_id(org_id: str) -> str:
    """Validate org IDs before using them in audit filesystem paths."""
    value = str(org_id or "").strip()
    if not value or ".." in value or os.sep in value or (os.altsep and os.altsep in value):
        raise ValueError("Invalid org_id for audit path")
    if not _ORG_ID_PATTERN.fullmatch(value):
        raise ValueError("Invalid org_id for audit path")
    return value


class AuditLogService:
    """Append-only audit event writer using per-organization JSONL files."""

    def __init__(self, upload_folder: str | None = None):
        self.base_dir = upload_folder or Config.UPLOAD_FOLDER

    def _audit_dir(self, org_id: str) -> str:
        safe_org_id = _safe_org_id(org_id)
        path = os.path.join(self.base_dir, "organizations", safe_org_id, "audit")
        os.makedirs(path, exist_ok=True)
        return path

    def audit_log_path(self, org_id: str) -> str:
        return os.path.join(self._audit_dir(org_id), "audit_events.jsonl")

    def record_event(
        self,
        *,
        org_id: str,
        event_type: str,
        actor_user_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if event_type not in AUDIT_EVENT_TYPES:
            raise ValueError(f"Unsupported audit event type: {event_type}")
        safe_org_id = _safe_org_id(org_id)

        event = {
            "event_id": f"audit_{uuid.uuid4().hex[:12]}",
            "event_type": event_type,
            "org_id": safe_org_id,
            "actor_user_id": str(actor_user_id or "") or None,
            "resource_type": resource_type,
            "resource_id": str(resource_id or "") or None,
            "metadata": redact_audit_metadata(metadata or {}),
            "request": self._request_context(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        path = self.audit_log_path(safe_org_id)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def list_events(self, org_id: str) -> list[dict[str, Any]]:
        path = self.audit_log_path(org_id)
        if not os.path.exists(path):
            return []
        events = []
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events

    def delete_org_events(self, org_id: str) -> bool:
        path = self.audit_log_path(org_id)
        if not os.path.exists(path):
            return False
        os.remove(path)
        return True

    def _request_context(self) -> dict[str, Any]:
        if not has_request_context():
            return {}
        return {
            "method": request.method,
            "path": request.path,
        }


def current_actor_user_id() -> str | None:
    if not has_request_context():
        return None
    if g.get("current_user_id"):
        return str(g.current_user_id)
    if g.get("current_user"):
        return str(g.current_user.get("user_id") or "") or None
    return None


def record_audit_event(
    *,
    org_id: str,
    event_type: str,
    actor_user_id: str | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Best-effort audit write that never exposes raw exception details to clients."""
    try:
        return AuditLogService().record_event(
            org_id=org_id,
            event_type=event_type,
            actor_user_id=actor_user_id or current_actor_user_id(),
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata,
        )
    except Exception as exc:
        logger.warning("Audit event write failed: %s", exc.__class__.__name__)
        return None
