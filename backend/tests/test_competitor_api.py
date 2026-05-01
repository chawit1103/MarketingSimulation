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


def test_competitor_scenarios_include_crisis_templates(client):
    response = client.get("/api/competitor/scenarios")

    assert response.status_code == 200
    payload = response.get_json()
    scenario_ids = {item["id"] for item in payload["scenarios"]}

    assert payload["success"] is True
    assert "price_war" in scenario_ids
    assert "influencer_backlash" in scenario_ids
    assert "product_recall" in scenario_ids
    assert "regulatory_issue" in scenario_ids
    assert "esg_controversy" in scenario_ids
    assert "fake_news" in scenario_ids
    assert "competitor_launch" in scenario_ids
    assert "traceback" not in payload


def test_competitor_simulation_returns_backend_labeled_war_room_fields(client):
    response = client.post(
        "/api/competitor/simulate",
        json={
            "scenario": "product_recall",
            "rounds": 8,
            "campaign_name": "Premium Water Launch",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    data = payload["data"]

    assert payload["success"] is True
    assert data["source"]["type"] == "live_backend"
    assert "Premium Water Launch" in data["brands"]
    assert data["expected_sentiment_movement"]
    assert data["affected_segments"]
    assert data["amplification_channels"]
    assert data["key_drivers"]
    assert data["recommended_response"]
    assert {item["stage"] for item in data["response_playbook"]} == {
        "first_2_hours",
        "first_24_hours",
        "first_72_hours",
    }
    assert "traceback" not in payload


def test_competitor_simulation_rejects_invalid_custom_brand_count(client):
    response = client.post(
        "/api/competitor/simulate",
        json={
            "scenario_name": "Invalid Custom Scenario",
            "brands": [{"name": "Only Brand", "market_share": 100}],
        },
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["error"] == "Need at least 2 brands"
    assert "traceback" not in payload
