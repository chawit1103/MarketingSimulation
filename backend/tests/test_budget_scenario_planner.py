import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.services.budget_scenario_planner import BudgetScenarioPlanner  # noqa: E402


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_budget_scenario_planner_returns_directional_allocation_with_source():
    result = BudgetScenarioPlanner().plan({
        "total_budget": 3000000,
        "duration_weeks": 8,
        "objective": "conversion",
        "risk_tolerance": "medium",
        "target_segments": ["Urban families", "Price-sensitive shoppers"],
        "channel_mix": {
            "facebook": 35,
            "tiktok": 25,
            "instagram": 20,
            "line": 20,
        },
    })

    assert result["version"] == "budget_scenario_planner_v1"
    assert result["source"]["type"] == "live_backend"
    assert result["source"]["data_basis"] == "deterministic_scenario_estimate"
    assert result["confidence_level"].endswith("directional")
    assert result["allocation_ranges"]
    assert result["segment_allocation_ranges"]
    assert result["assumptions"]
    assert result["limitations"]
    assert result["recommended_validation_step"]
    assert "backend_verified" not in str(result)
    rendered = str(result).lower()
    assert "guaranteed" not in rendered
    assert "optimization certainty" not in rendered


def test_budget_scenario_planner_demo_mode_is_labeled_demo_fixture():
    result = BudgetScenarioPlanner().plan({
        "demo": True,
        "total_budget": 1200000,
        "duration_weeks": 6,
        "objective": "awareness",
        "risk_tolerance": "low",
        "target_segments": ["Creator-led discovery", "Family shoppers"],
        "channel_mix": ["tiktok", "instagram", "facebook", "line"],
    })

    assert result["source"]["type"] == "demo_mode"
    assert result["source"]["data_basis"] == "demo_fixture"
    assert "not live campaign evidence" in result["source"]["warning"]


def test_budget_scenario_endpoint_is_public_and_safe(client):
    response = client.post("/api/decision/budget-scenario", json={
        "inputs": {
            "total_budget": 2500000,
            "duration_weeks": 6,
            "objective": "crisis_recovery",
            "risk_tolerance": "high",
            "target_segments": ["Concerned parents", "Creator audiences"],
            "channel_mix": {"facebook": 40, "line": 25, "youtube": 20, "twitter_x": 15},
        }
    })

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["source"]["type"] == "live_backend"
    assert data["objective"] == "crisis_recovery"
    assert data["risk_tolerance"] == "high"
    assert data["allocation_ranges"][0]["budget_range"]["midpoint"] > 0
    rendered = str(payload)
    assert "traceback" not in rendered.lower()
    assert "guaranteed" not in rendered.lower()
    assert "backend_verified" not in rendered
