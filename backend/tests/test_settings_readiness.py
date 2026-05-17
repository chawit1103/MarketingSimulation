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
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


@pytest.fixture()
def authenticated_settings_client(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    SettingsManager.invalidate()

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("Settings Security Org", "settings-security-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    user = user_service.create_user(
        org.org_id,
        "admin@example.com",
        "local-test-password",
        name="Admin",
        role=UserRole.ADMIN,
    )

    app = create_app()
    app.config.update(TESTING=True)
    token = AuthService().create_token(user)

    yield app.test_client(), {"Authorization": f"Bearer {token}"}

    SettingsManager.invalidate()


def test_settings_readiness_demo_mode_requires_no_secrets(client):
    response = client.post("/api/settings/readiness", json={"mode": "demo"})

    assert response.status_code == 200
    payload = response.get_json()
    data = payload["data"]

    assert payload["success"] is True
    assert data["ready"] is True
    assert data["checks"]["llm"]["status"] == "skipped"
    assert data["cost_estimate"]["per_100_personas"] == 0
    assert "traceback" not in str(payload).lower()


def test_settings_readiness_cloud_mode_reports_missing_keys_without_echoing_secrets(client):
    response = client.post(
        "/api/settings/readiness",
        json={
            "mode": "cloud",
            "llm": {"provider": "openai", "model": "gpt-4o-mini", "api_key": ""},
            "embedding": {"provider": "openai", "model": "text-embedding-3-small", "api_key": ""},
            "graph_db": {"mode": "cloud", "uri": "neo4j+s://example.databases.neo4j.io", "user": "neo4j"},
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    data = payload["data"]

    assert data["ready"] is False
    assert data["checks"]["llm"]["status"] == "needs_attention"
    assert "Cloud provider requires an API key." in data["checks"]["llm"]["issues"]
    assert "api_key" not in str(payload)
    assert "traceback" not in str(payload).lower()


def test_settings_readiness_accepts_secret_presence_flags_without_secret_values(client):
    response = client.post(
        "/api/settings/readiness",
        json={
            "mode": "cloud",
            "llm": {"provider": "openai", "model": "gpt-4o-mini", "api_key_present": True},
            "embedding": {"provider": "openai", "model": "text-embedding-3-small", "api_key_present": True},
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password_present": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    data = payload["data"]

    assert data["ready"] is True
    assert data["checks"]["llm"]["status"] == "ready"
    assert data["checks"]["embedding"]["status"] == "ready"
    assert data["checks"]["neo4j"]["status"] == "ready"
    assert "api_key" not in str(payload)
    assert "password" not in str(payload)


def test_settings_providers_catalog_is_public_and_safe(client):
    response = client.get("/api/settings/providers")

    assert response.status_code == 200
    payload = response.get_json()

    assert payload["success"] is True
    assert payload["llm_providers"]
    assert payload["embedding_providers"]
    assert "api_key" not in str(payload).lower()


def test_settings_read_response_uses_presence_flags_without_raw_secrets(authenticated_settings_client):
    client, headers = authenticated_settings_client
    SettingsManager().update(
        {
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": "unit-llm-secret-value",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-small",
                "api_key": "unit-embedding-secret-value",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "unit-graph-secret-value",
            },
            "task_llm": {},
        }
    )

    response = client.get("/api/settings", headers=headers)

    assert response.status_code == 200
    payload = response.get_json()
    rendered = str(payload)
    settings = payload["settings"]

    assert settings["llm"]["api_key_present"] is True
    assert settings["embedding"]["api_key_present"] is True
    assert settings["graph_db"]["password_present"] is True
    assert "api_key" not in settings["llm"]
    assert "api_key" not in settings["embedding"]
    assert "password" not in settings["graph_db"]
    assert "unit-llm-secret-value" not in rendered
    assert "unit-embedding-secret-value" not in rendered
    assert "unit-graph-secret-value" not in rendered
    assert "traceback" not in rendered.lower()


def test_settings_update_preserves_existing_secrets_for_blank_and_masked_values(authenticated_settings_client):
    client, headers = authenticated_settings_client
    SettingsManager().update(
        {
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "old-model",
                "api_key": "existing-llm-secret",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "old-embedding",
                "api_key": "existing-embedding-secret",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://old.example",
                "user": "neo4j",
                "password": "existing-graph-secret",
            },
            "task_llm": {},
        }
    )

    response = client.put(
        "/api/settings",
        headers=headers,
        json={
            "language": "th",
            "llm": {
                "provider": "openai",
                "model": "new-model",
                "api_key": "",
                "api_key_present": True,
                "base_url": None,
                "temperature": 0.4,
                "max_tokens": 2048,
                "timeout": 90,
            },
            "embedding": {
                "provider": "openai",
                "model": "new-embedding",
                "api_key": "••••cret",
                "api_key_present": True,
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://new.example",
                "user": "neo4j",
                "password": "",
                "password_present": True,
            },
            "task_llm": {},
        },
    )

    assert response.status_code == 200
    stored = SettingsManager().get()
    assert stored.llm.model == "new-model"
    assert stored.llm.api_key == "existing-llm-secret"
    assert stored.embedding.model == "new-embedding"
    assert stored.embedding.api_key == "existing-embedding-secret"
    assert stored.graph_db.uri == "neo4j+s://new.example"
    assert stored.graph_db.password == "existing-graph-secret"
    assert "existing-graph-secret" not in str(response.get_json())


def test_settings_update_accepts_new_secret_but_never_echoes_it(authenticated_settings_client):
    client, headers = authenticated_settings_client

    response = client.put(
        "/api/settings",
        headers=headers,
        json={
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": "replacement-llm-secret",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-small",
                "api_key": "replacement-embedding-secret",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "replacement-graph-secret",
            },
            "task_llm": {},
        },
    )

    assert response.status_code == 200
    assert "replacement-llm-secret" not in str(response.get_json())
    assert "replacement-embedding-secret" not in str(response.get_json())
    assert "replacement-graph-secret" not in str(response.get_json())

    read_response = client.get("/api/settings", headers=headers)
    payload = read_response.get_json()
    rendered = str(payload)

    assert payload["settings"]["llm"]["api_key_present"] is True
    assert payload["settings"]["embedding"]["api_key_present"] is True
    assert payload["settings"]["graph_db"]["password_present"] is True
    assert "replacement-llm-secret" not in rendered
    assert "replacement-embedding-secret" not in rendered
    assert "replacement-graph-secret" not in rendered
