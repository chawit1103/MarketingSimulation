import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.services.action_plan import ActionPlanService  # noqa: E402


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def sample_inputs():
    return {
        "campaign": {
            "name": "Premium Water Launch",
            "objective": "product_launch",
            "target": {"channels": ["tiktok", "instagram", "line"]},
        },
        "kpis": {
            "overall_sentiment": 41,
            "conversion_probability": 68,
            "social_influence": 76,
            "message_resonance": 73,
            "crisis_risk": "medium",
            "confidence_score": 82,
        },
        "segments": [
            {"name": "Urban Health Buyers", "sentiment": 63},
            {"name": "Price-Sensitive Mass", "sentiment": -12},
        ],
        "evidence": {
            "confidence_score": 82,
            "risk_drivers": ["Price premium needs stronger proof."],
        },
        "source": {"type": "demo_mode", "warning": "Demo only."},
    }


def test_action_plan_has_required_sections_and_item_shape():
    payload = sample_inputs()
    plan = ActionPlanService().generate(**payload)

    assert plan["version"] == "structured_action_plan_v1"
    assert plan["source"]["type"] == "demo_mode"
    assert "guaranteed" in plan["disclaimer"]
    assert set(plan["sections"]) == {
        "creative_adjustment",
        "channel_allocation",
        "crisis_prevention",
        "validation_plan",
    }

    for section in plan["sections"].values():
        assert section["items"]
        for item in section["items"]:
            assert item["recommendation"]
            assert item["reason"]
            assert item["expected_impact"]
            assert item["risk"]


def test_action_plan_inherits_unknown_source_safely():
    payload = sample_inputs()
    payload["source"] = {"type": "untrusted_custom_source"}
    plan = ActionPlanService().generate(**payload)

    assert plan["source"]["type"] == "unknown"
    assert plan["sections"]["validation_plan"]["items"][0]["priority"] == "high"


def test_demo_dashboard_includes_structured_action_plan(client):
    response = client.get("/api/demo/campaigns/demo-premium-water/dashboard")

    assert response.status_code == 200
    payload = response.get_json()
    plan = payload["data"]["action_plan"]

    assert plan["source"]["type"] == "demo_mode"
    assert "creative_adjustment" in plan["sections"]
    assert "channel_allocation" in plan["sections"]
    assert "traceback" not in payload
