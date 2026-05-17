import sys
from pathlib import Path

import pytest
from flask import jsonify


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_demo_dashboard_route_is_public_and_labeled(client):
    response = client.get("/api/demo/campaigns/demo-premium-water/dashboard")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["campaign"]["id"] == "demo-premium-water"
    assert payload["data"]["source"]["type"] == "demo_mode"
    assert "traceback" not in payload


def test_every_visible_demo_campaign_has_matching_dashboard_fixture(client):
    list_response = client.get("/api/demo/campaigns")
    assert list_response.status_code == 200
    campaigns = list_response.get_json()["data"]
    assert campaigns

    for campaign in campaigns:
        response = client.get(f"/api/demo/campaigns/{campaign['id']}/dashboard")
        assert response.status_code == 200
        payload = response.get_json()
        data = payload["data"]

        assert data["campaign"]["id"] == campaign["id"]
        assert data["source"]["type"] == "demo_mode"
        assert data["source"]["source_mode"] == "demo_mode"
        assert data["source"]["data_basis"] == "demo_fixture"
        assert data["source"]["type"] != "backend_verified"
        assert data["source"]["source_mode"] != "backend_verified"
        assert "backend_verified" not in str(data).lower()
        assert data["kpis"]
        assert data["segments"]
        assert data["action_plan"]
        assert data["evidence"]["assumptions"]
        assert data["evidence"]["limitations"]
        assert data["evidence"]["risk_drivers"]
        assert data["evidence"]["quotes"]
        assert data["evidence"]["recommended_actions"]
        assert data["evidence"]["recommended_validation_step"]


def test_demo_dashboard_unknown_id_returns_safe_404(client):
    response = client.get("/api/demo/campaigns/demo-missing/dashboard")
    payload = response.get_json()

    assert response.status_code == 404
    assert payload == {
        "success": False,
        "error": "Demo dashboard not found",
        "code": "demo_dashboard_not_found",
    }
    assert "premium-water" not in str(payload)
    assert "traceback" not in str(payload).lower()


def test_impact_quick_scenario_route_is_public_and_labeled(client):
    response = client.get(
        "/api/impact/scenarios/42?price=120&market=100000&share=10&conversion=5&cost=500000&months=6"
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["campaign_id"] == "quick"
    assert payload["data"]["source"]["type"] == "local_estimate"
    assert "traceback" not in payload


def test_api_response_sanitizer_strips_traceback_from_client_payload(app):
    @app.get("/api/demo/test-traceback-sanitizer")
    def _traceback_test():
        return jsonify(
            {
                "success": False,
                "error": "boom",
                "traceback": "Traceback (most recent call last):\nsecret stack",
            }
        ), 500

    response = app.test_client().get("/api/demo/test-traceback-sanitizer")
    payload = response.get_json()

    assert response.status_code == 500
    assert payload == {"success": False, "error": "Internal server error", "code": "internal_error"}


def test_production_rejects_known_fallback_secret():
    class ProductionConfig(Config):
        ENVIRONMENT = "production"
        SECRET_KEY = "3c-simulator-secret-key"

    with pytest.raises(RuntimeError, match="Production requires SECRET_KEY"):
        create_app(ProductionConfig)
