import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


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
