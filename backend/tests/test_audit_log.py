import json
import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.api.calibration import _safe_calibration_campaign_id  # noqa: E402
from app.api.export import _safe_export_type, _safe_source_metadata  # noqa: E402
from app.api.report import _report_audit_metadata, _safe_report_campaign_id  # noqa: E402
from app.config import Config  # noqa: E402
from app.models.settings import SettingsManager  # noqa: E402
from app.models.user import UserRole  # noqa: E402
from app.services.audit_log_service import AuditLogService  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402
from app.utils.audit_redaction import REDACTED, redact_audit_metadata  # noqa: E402


def test_audit_redaction_removes_secrets_pii_and_raw_content():
    metadata = {
        "campaign_id": "cmp_safe",
        "campaign_brief": "Launch the confidential customer retention offer.",
        "api_key": "placeholder-key-for-redaction-test",
        "nested": {
            "email": "person@example.com",
            "raw_crm_records": [{"phone": "+1 555 111 2222"}],
            "safe_flag": True,
        },
    }

    redacted = redact_audit_metadata(metadata)
    rendered = json.dumps(redacted)

    assert redacted["campaign_id"] == "cmp_safe"
    assert redacted["campaign_brief"] == REDACTED
    assert redacted["api_key"] == REDACTED
    assert redacted["nested"]["email"] == REDACTED
    assert redacted["nested"]["raw_crm_records"] == REDACTED
    assert redacted["nested"]["safe_flag"] is True
    assert "confidential customer retention" not in rendered
    assert "placeholder-key-for-redaction-test" not in rendered
    assert "person@example.com" not in rendered
    assert "+1 555 111 2222" not in rendered


def test_export_audit_type_normalization_rejects_arbitrary_request_text():
    assert _safe_export_type("dashboard") == "dashboard"
    assert _safe_export_type("strategy-pack") == "strategy_pack"
    assert _safe_export_type("Campaign Name With Sensitive Brief") == "unknown"
    assert _safe_export_type("person@example.com") == "unknown"
    assert _safe_export_type("confidential-campaign-token-text") == "unknown"
    assert _safe_export_type(None) == "generic"


def test_strategy_pack_source_audit_metadata_is_categorical_only():
    assert _safe_source_metadata({
        "source_mode": "demo-mode",
        "data_basis": "demo-fixture",
    }) == {"source_mode": "demo_mode", "data_basis": "demo_fixture"}
    assert _safe_source_metadata({
        "source_mode": "Confidential Campaign Name",
        "data_basis": "person@example.com",
    }) == {"source_mode": "unknown", "data_basis": "unknown"}
    assert _safe_source_metadata({
        "source_mode": "backend_verified",
        "data_basis": "real_simulation",
    }) == {"source_mode": "backend_verified", "data_basis": "real_simulation"}
    assert _safe_source_metadata({
        "source_mode": "live_backend",
        "data_basis": "backend_generated",
    }) == {"source_mode": "live_backend", "data_basis": "backend_generated"}


@pytest.mark.parametrize(
    ("campaign_id", "expected"),
    [
        ("cmp_a1b2c3d4e5f6", "cmp_a1b2c3d4e5f6"),
        ("Customer Alpha Launch", "unknown"),
        ("client-campaign@example.com", "unknown"),
        ("Brief for a confidential customer launch " * 8, "unknown"),
        ("cmp_a1b2c3/4e5f6", "unknown"),
        ("cmp_a1b2c3 4e5f6", "unknown"),
    ],
)
def test_safe_calibration_campaign_id_allows_only_generated_ids(campaign_id, expected):
    assert _safe_calibration_campaign_id(campaign_id) == expected


@pytest.mark.parametrize(
    ("campaign_id", "expected"),
    [
        ("cmp_a1b2c3d4e5f6", "cmp_a1b2c3d4e5f6"),
        ("Customer Alpha Launch", "unknown"),
        ("client-campaign@example.com", "unknown"),
        ("organizations/acme/audit", "unknown"),
        ("Brief for a confidential customer launch " * 8, "unknown"),
        ("cmp_a1b2c3/4e5f6", "unknown"),
        ("cmp_a1b2c3 4e5f6", "unknown"),
    ],
)
def test_safe_report_campaign_id_reuses_generated_id_rules(campaign_id, expected):
    assert _safe_report_campaign_id(campaign_id) == expected


@pytest.mark.parametrize(
    "unsafe_campaign_id",
    [
        "Customer Alpha Launch",
        "client-campaign@example.com",
        "organizations/acme/audit",
        "../customer-alpha/report",
        "Brief for a confidential customer launch " * 8,
    ],
)
def test_report_audit_events_replace_unsafe_campaign_ids(tmp_path, unsafe_campaign_id):
    service = AuditLogService(upload_folder=str(tmp_path))

    for event_type in ("report_generation_started", "report_downloaded"):
        service.record_event(
            org_id="org_a",
            event_type=event_type,
            resource_type="report",
            resource_id=f"report_{event_type}",
            metadata=_report_audit_metadata(
                "sim_safe",
                unsafe_campaign_id,
                format="markdown" if event_type == "report_downloaded" else None,
            ),
        )

    events = service.list_events("org_a")
    report_events = [event for event in events if event["event_type"].startswith("report_")]
    audit_jsonl = Path(service.audit_log_path("org_a")).read_text(encoding="utf-8")

    assert len(report_events) == 2
    assert {event["metadata"]["campaign_id"] for event in report_events} == {"unknown"}
    assert unsafe_campaign_id not in audit_jsonl


def test_report_audit_events_preserve_safe_generated_campaign_ids(tmp_path):
    service = AuditLogService(upload_folder=str(tmp_path))
    safe_campaign_id = "cmp_a1b2c3d4e5f6"

    for event_type in ("report_generation_started", "report_downloaded"):
        service.record_event(
            org_id="org_a",
            event_type=event_type,
            resource_type="report",
            resource_id=f"report_{event_type}",
            metadata=_report_audit_metadata("sim_safe", safe_campaign_id),
        )

    events = service.list_events("org_a")
    report_events = [event for event in events if event["event_type"].startswith("report_")]

    assert len(report_events) == 2
    assert {event["metadata"]["campaign_id"] for event in report_events} == {safe_campaign_id}


def test_audit_log_service_writes_org_scoped_jsonl_without_raw_content(tmp_path):
    service = AuditLogService(upload_folder=str(tmp_path))

    event = service.record_event(
        org_id="org_a",
        event_type="campaign_updated",
        actor_user_id="user_1",
        resource_type="campaign",
        resource_id="cmp_1",
        metadata={
            "changed_fields": ["description", "status"],
            "brief_text": "Raw customer brief text should not be persisted.",
            "provider_token": "placeholder-provider-token-for-test",
        },
    )

    events = service.list_events("org_a")
    rendered = json.dumps(events)

    assert event["event_type"] == "campaign_updated"
    assert len(events) == 1
    assert events[0]["org_id"] == "org_a"
    assert events[0]["metadata"]["brief_text"] == REDACTED
    assert events[0]["metadata"]["provider_token"] == REDACTED
    assert "Raw customer brief" not in rendered
    assert "placeholder-provider-token-for-test" not in rendered
    assert service.audit_log_path("org_a").endswith("organizations/org_a/audit/audit_events.jsonl")


@pytest.mark.parametrize(
    "org_id",
    [
        "",
        "   ",
        "../outside",
        "org/child",
        "org\\child",
        "org..child",
        "org child",
        "org.child",
    ],
)
def test_audit_log_service_rejects_invalid_org_path_segments(tmp_path, org_id):
    service = AuditLogService(upload_folder=str(tmp_path))

    with pytest.raises(ValueError):
        service.record_event(
            org_id=org_id,
            event_type="campaign_updated",
            metadata={"changed_fields": ["status"]},
        )

    assert not (tmp_path / "outside").exists()
    assert not (tmp_path.parent / "outside").exists()


@pytest.fixture()
def audit_api_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    SettingsManager.invalidate()

    from app.api import campaign as campaign_api  # noqa: E402

    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("Audit Org", "audit-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    admin = user_service.create_user(
        org.org_id,
        "admin@example.com",
        "local-test-password",
        name="Admin",
        role=UserRole.ADMIN,
    )
    analyst = user_service.create_user(
        org.org_id,
        "analyst@example.com",
        "local-test-password",
        name="Analyst",
        role=UserRole.ANALYST,
    )

    app = create_app()
    app.config.update(TESTING=True)
    auth = AuthService()
    headers = {
        "admin": {"Authorization": f"Bearer {auth.create_token(admin)}"},
        "analyst": {"Authorization": f"Bearer {auth.create_token(analyst)}"},
    }

    yield app.test_client(), headers, org, str(tmp_path)

    SettingsManager.invalidate()
    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None


def test_login_campaign_and_settings_routes_create_safe_audit_events(audit_api_context):
    client, headers, org, upload_folder = audit_api_context

    login_response = client.post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "local-test-password"},
    )
    campaign_response = client.post(
        "/api/campaign",
        headers=headers["analyst"],
        json={
            "name": "Confidential Launch Name",
            "description": "Raw campaign brief with a customer segment.",
            "objective": "message_testing",
            "target": {"segment_name": "Do not log this segment"},
        },
    )
    campaign_id = campaign_response.get_json()["data"]["campaign_id"]
    get_campaign_response = client.get(f"/api/campaign/{campaign_id}", headers=headers["analyst"])
    update_campaign_response = client.put(
        f"/api/campaign/{campaign_id}",
        headers=headers["analyst"],
        json={
            "description": "Updated raw customer brief should also stay out.",
            "status": "draft",
        },
    )
    settings_response = client.put(
        "/api/settings",
        headers=headers["admin"],
        json={
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": "unit-api-key-should-not-be-logged",
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "graph-password-should-not-be-logged",
            },
        },
    )

    assert login_response.status_code == 200
    assert campaign_response.status_code == 201
    assert get_campaign_response.status_code == 200
    assert update_campaign_response.status_code == 200
    assert settings_response.status_code == 200

    events = AuditLogService(upload_folder=upload_folder).list_events(org.org_id)
    event_types = [event["event_type"] for event in events]
    rendered = json.dumps(events)

    assert "login" in event_types
    assert "campaign_created" in event_types
    assert "campaign_updated" in event_types
    assert "settings_updated" in event_types
    assert "admin@example.com" not in rendered
    assert "local-test-password" not in rendered
    assert "Confidential Launch Name" not in rendered
    assert "Raw campaign brief" not in rendered
    assert "Updated raw customer brief" not in rendered
    assert "Do not log this segment" not in rendered
    assert "unit-api-key-should-not-be-logged" not in rendered
    assert "graph-password-should-not-be-logged" not in rendered


def test_calibration_import_creates_audit_event_without_raw_actuals(audit_api_context):
    client, headers, org, upload_folder = audit_api_context

    response = client.post(
        "/api/calibration/actual-results",
        headers=headers["analyst"],
        json={
            "campaign_id": "cmp_a1b2c3d4e5f6",
            "impressions": 1200,
            "estimated_impressions": 1000,
            "qualitative_notes": "Aggregate only; no raw customer records.",
        },
    )

    assert response.status_code == 201

    events = AuditLogService(upload_folder=upload_folder).list_events(org.org_id)
    calibration_events = [event for event in events if event["event_type"] == "calibration_imported"]
    rendered = json.dumps(events)

    assert len(calibration_events) == 1
    assert calibration_events[0]["resource_id"].startswith("cal_")
    assert calibration_events[0]["metadata"]["campaign_id"] == "cmp_a1b2c3d4e5f6"
    assert "Aggregate only" not in rendered
    assert "impressions" not in rendered


@pytest.mark.parametrize(
    "unsafe_campaign_id",
    [
        "Customer Alpha Launch",
        "client-campaign@example.com",
        "Brief for a confidential customer launch " * 8,
    ],
)
def test_calibration_import_audit_event_replaces_unsafe_campaign_id(audit_api_context, unsafe_campaign_id):
    client, headers, org, upload_folder = audit_api_context

    response = client.post(
        "/api/calibration/actual-results",
        headers=headers["analyst"],
        json={
            "campaign_id": unsafe_campaign_id,
            "impressions": 1200,
            "estimated_impressions": 1000,
        },
    )

    assert response.status_code == 201

    audit_service = AuditLogService(upload_folder=upload_folder)
    events = audit_service.list_events(org.org_id)
    calibration_events = [event for event in events if event["event_type"] == "calibration_imported"]
    audit_jsonl = Path(audit_service.audit_log_path(org.org_id)).read_text(encoding="utf-8")

    assert len(calibration_events) == 1
    assert calibration_events[0]["metadata"]["campaign_id"] == "unknown"
    assert unsafe_campaign_id not in audit_jsonl
