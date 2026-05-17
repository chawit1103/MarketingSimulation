import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.services.brief_quality import BriefQualityService  # noqa: E402


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def complete_brief():
    return {
        "name": "Premium Water Launch",
        "description": "Launch in Bangkok for 8 weeks with awareness and conversion KPIs.",
        "objective": "product_launch",
        "target": {
            "segment_name": "Urban health buyers and family decision makers",
            "regions": ["Bangkok", "Central Thailand"],
            "channels": ["facebook", "instagram", "tiktok", "line"],
            "persona_count": 500,
        },
        "campaign_duration": "8 weeks",
        "budget_range": "฿2M-3M media spend",
        "primary_kpi": "conversion probability and brand lift",
        "competitor_context": "Competitor A is discounting bottled water and creator bundles.",
        "brand_constraints": "Must avoid medical claims; tone should be premium but practical.",
        "risk_legal_notes": "Legal review needed for mineral benefit claims and eco packaging.",
    }


def test_brief_quality_scores_complete_brief_high():
    result = BriefQualityService().score(complete_brief())

    assert result["score"] == 100
    assert result["level"] == "strong"
    assert result["missing_fields"] == []
    assert result["confidence_impact"] == "low_negative_impact"


def test_brief_quality_identifies_missing_fields():
    result = BriefQualityService().score({
        "name": "Thin campaign",
        "description": "We want to launch something soon.",
        "objective": "product_launch",
    })

    missing_keys = {item["key"] for item in result["missing_fields"]}
    assert result["score"] < 50
    assert "budget_range" in missing_keys
    assert "primary_kpi" in missing_keys
    assert "risk_legal_notes" in missing_keys


def test_brief_quality_endpoint_is_public_and_deterministic(client):
    response = client.post("/api/brief/quality", json={"brief": complete_brief()})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["data"]["score"] == 100
    assert payload["data"]["method"] == "deterministic_brief_quality_v1"
    assert "traceback" not in payload


def test_brief_quality_endpoint_handles_plain_text(client):
    response = client.post("/api/brief/quality", json={"brief": "Launch in Bangkok on TikTok for 4 weeks."})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert isinstance(payload["data"]["missing_fields"], list)
    assert "traceback" not in payload
