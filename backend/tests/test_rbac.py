import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.models.settings import SettingsManager  # noqa: E402
from app.models.user import UserRole  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


@pytest.fixture()
def rbac_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)

    SettingsManager.invalidate()
    from app.api import campaign as campaign_api  # noqa: E402
    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("RBAC Test Org", "rbac-test-org", "admin@example.com")
    other_org = org_service.create_org("Other RBAC Org", "other-rbac-org", "owner@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))

    users = {
        "admin": user_service.create_user(
            org.org_id,
            "admin@example.com",
            "local-test-password",
            name="Admin",
            role=UserRole.ADMIN,
        ),
        "analyst": user_service.create_user(
            org.org_id,
            "analyst@example.com",
            "local-test-password",
            name="Analyst",
            role=UserRole.ANALYST,
        ),
        "viewer": user_service.create_user(
            org.org_id,
            "viewer@example.com",
            "local-test-password",
            name="Viewer",
            role=UserRole.VIEWER,
        ),
    }

    app = create_app()
    app.config.update(TESTING=True)
    auth = AuthService()
    headers = {
        role: {"Authorization": f"Bearer {auth.create_token(user)}"}
        for role, user in users.items()
    }

    yield app.test_client(), headers, org, other_org

    SettingsManager.invalidate()
    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None


def test_auth_me_requires_authentication(rbac_context):
    client, _, _, _ = rbac_context

    response = client.get("/api/auth/me")
    api_key_response = client.post("/api/auth/api-key")
    switch_response = client.post("/api/auth/switch-org", json={"org_id": "org_other"})

    assert response.status_code == 401
    assert api_key_response.status_code == 401
    assert switch_response.status_code == 401
    payload = response.get_json()
    assert "traceback" not in str(payload).lower()


def test_viewer_can_read_campaigns_but_cannot_mutate(rbac_context):
    client, headers, _, _ = rbac_context

    read_response = client.get("/api/campaign", headers=headers["viewer"])
    create_response = client.post("/api/campaign", headers=headers["viewer"], json={"name": "Viewer Attempt"})
    delete_response = client.delete("/api/campaign/cmp_missing", headers=headers["viewer"])

    assert read_response.status_code == 200
    assert create_response.status_code == 403
    assert delete_response.status_code == 403
    assert "traceback" not in str(create_response.get_json()).lower()


def test_analyst_can_create_campaign_but_cannot_manage_settings_or_api_keys(rbac_context):
    client, headers, _, _ = rbac_context

    campaign_response = client.post(
        "/api/campaign",
        headers=headers["analyst"],
        json={
            "name": "Analyst Campaign",
            "description": "Created in an RBAC contract test.",
            "objective": "message_testing",
        },
    )
    settings_response = client.put(
        "/api/settings",
        headers=headers["analyst"],
        json={"language": "en"},
    )
    api_key_response = client.post("/api/auth/api-key", headers=headers["analyst"])
    provider_test_response = client.post(
        "/api/settings/test-llm",
        headers=headers["analyst"],
        json={"provider": "openai", "model": "gpt-4o-mini", "api_key": "not-used"},
    )
    strategy_pack_response = client.post(
        "/api/export/strategy-pack",
        headers=headers["analyst"],
        json={
            "mode": "brand",
            "campaign": {"name": "RBAC Strategy Pack"},
            "source": {"type": "local_estimate"},
        },
    )
    strategy_pack_pptx_response = client.post(
        "/api/export/strategy-pack/pptx",
        headers=headers["analyst"],
        json={
            "mode": "brand",
            "campaign": {"name": "RBAC Strategy Pack"},
            "source": {"type": "local_estimate"},
        },
    )
    switch_response = client.post(
        "/api/auth/switch-org",
        headers=headers["analyst"],
        json={"org_id": "org_other"},
    )

    assert campaign_response.status_code == 201
    assert settings_response.status_code == 403
    assert api_key_response.status_code == 403
    assert provider_test_response.status_code == 403
    assert strategy_pack_response.status_code == 200
    assert strategy_pack_response.get_json()["data"]["source"]["source_mode"] == "local_estimate"
    assert strategy_pack_pptx_response.status_code == 200
    assert (
        strategy_pack_pptx_response.mimetype
        == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    assert switch_response.status_code == 403


def test_admin_can_access_privileged_auth_and_settings_flows(rbac_context):
    client, headers, org, _ = rbac_context

    me_response = client.get("/api/auth/me", headers=headers["admin"])
    api_key_response = client.post("/api/auth/api-key", headers=headers["admin"])
    settings_response = client.put(
        "/api/settings",
        headers=headers["admin"],
        json={
            "language": "en",
            "llm": {
                "provider": "ollama",
                "model": "qwen2.5:7b",
                "api_key": "",
                "base_url": "http://localhost:11434/v1",
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "ollama",
                "model": "nomic-embed-text",
                "api_key": "",
                "base_url": "http://localhost:11434",
            },
            "graph_db": {
                "mode": "local",
                "uri": "bolt://localhost:7687",
                "user": "neo4j",
                "password": "",
                "password_present": True,
            },
            "task_llm": {},
        },
    )
    switch_response = client.post(
        "/api/auth/switch-org",
        headers=headers["admin"],
        json={"org_id": org.org_id},
    )

    assert me_response.status_code == 200
    assert api_key_response.status_code == 200
    api_key_payload = api_key_response.get_json()
    assert api_key_payload["data"]["api_key"].startswith("ms_")
    assert "password_hash" not in str(me_response.get_json())
    assert settings_response.status_code == 200
    assert switch_response.status_code == 501
    assert "disabled" in switch_response.get_json()["error"].lower()
    assert "token" not in str(switch_response.get_json()).lower()


def test_viewer_and_analyst_cannot_run_admin_only_destructive_operations(rbac_context):
    client, headers, _, _ = rbac_context

    viewer_graph_delete = client.delete("/api/graph/delete/graph_missing", headers=headers["viewer"])
    analyst_report_delete = client.delete("/api/report/report_missing", headers=headers["analyst"])

    assert viewer_graph_delete.status_code == 403
    assert analyst_report_delete.status_code == 403


def test_viewer_cannot_run_simulation_report_export_or_persona_mutations(rbac_context):
    client, headers, _, _ = rbac_context

    start_response = client.post(
        "/api/simulation/start",
        headers=headers["viewer"],
        json={},
    )
    stop_response = client.post(
        "/api/simulation/stop",
        headers=headers["viewer"],
        json={},
    )
    close_env_response = client.post(
        "/api/simulation/close-env",
        headers=headers["viewer"],
        json={},
    )
    report_response = client.post(
        "/api/report/generate",
        headers=headers["viewer"],
        json={"simulation_id": "sim_missing"},
    )
    export_response = client.post(
        "/api/export/pptx",
        headers=headers["viewer"],
        json={"title": "Viewer export attempt"},
    )
    strategy_pack_response = client.post(
        "/api/export/strategy-pack",
        headers=headers["viewer"],
        json={"title": "Viewer strategy pack attempt"},
    )
    strategy_pack_pptx_response = client.post(
        "/api/export/strategy-pack/pptx",
        headers=headers["viewer"],
        json={"title": "Viewer strategy pack PPTX attempt"},
    )
    persona_response = client.post(
        "/api/persona/generate",
        headers=headers["viewer"],
        json={"campaign_id": "cmp_missing", "target": {"persona_count": 1}},
    )

    assert start_response.status_code == 403
    assert stop_response.status_code == 403
    assert close_env_response.status_code == 403
    assert report_response.status_code == 403
    assert export_response.status_code == 403
    assert strategy_pack_response.status_code == 403
    assert strategy_pack_pptx_response.status_code == 403
    assert persona_response.status_code == 403


def test_org_switching_does_not_allow_cross_org_or_existence_probing(rbac_context):
    client, headers, _, other_org = rbac_context

    other_org_response = client.post(
        "/api/auth/switch-org",
        headers=headers["admin"],
        json={"org_id": other_org.org_id},
    )
    missing_org_response = client.post(
        "/api/auth/switch-org",
        headers=headers["admin"],
        json={"org_id": "org_missing"},
    )

    assert other_org_response.status_code == 403
    assert missing_org_response.status_code == 403
    assert other_org_response.get_json() == missing_org_response.get_json()
    rendered = str(other_org_response.get_json()) + str(missing_org_response.get_json())
    assert other_org.org_id not in rendered
    assert "org_missing" not in rendered
    assert "token" not in rendered.lower()
