import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.models.report import ExecutiveReport  # noqa: E402
from app.models.organization import SubscriptionTier  # noqa: E402
from app.models.user import UserRole  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.campaign_service import CampaignService  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


@pytest.fixture()
def comparator_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org(
        "Comparator Test Org",
        "comparator-test-org",
        "admin@example.com",
        tier=SubscriptionTier.ENTERPRISE,
    )
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    admin = user_service.create_user(
        org.org_id,
        "admin@example.com",
        "local-test-password",
        name="Admin",
        role=UserRole.ADMIN,
    )

    app = create_app()
    app.config.update(TESTING=True)
    headers = {"Authorization": f"Bearer {AuthService().create_token(admin)}"}
    campaign_service = CampaignService(upload_folder=str(tmp_path))

    yield app.test_client(), headers, org, campaign_service


def _campaign_with_report(campaign_service, org_id, name, sentiment, conversion, crisis):
    campaign = campaign_service.create_campaign(org_id, name, objective="message_testing")
    report = ExecutiveReport.empty(campaign.campaign_id, org_id)
    report.overall_sentiment = sentiment
    report.conversion_probability = conversion
    report.social_influence_index = 62
    report.message_resonance = 70
    report.crisis_risk = crisis
    report.brand_perception_shift = 14
    report.opinion_polarization = 30
    report.source_mode = "backend_verified"
    report.data_basis = "real_simulation"
    report.confidence = 0.82
    campaign_service.update_campaign(
        campaign.campaign_id,
        org_id,
        {"results_summary": report.model_dump()},
    )
    return campaign


def test_demo_comparator_returns_three_labeled_campaign_fixtures(comparator_context):
    client, _, _, _ = comparator_context

    response = client.get("/api/comparator/demo/campaigns")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert len(payload["data"]) == 3
    assert {item["direction"] for item in payload["data"]} == {
        "emotional_storytelling",
        "proof_led_trust",
        "price_promotion",
    }
    assert payload["source"]["source_mode"] == "demo_mode"
    assert "backend_verified" not in str(payload)


def test_demo_comparator_compare_returns_ranked_provenance_shape(comparator_context):
    client, _, _, _ = comparator_context

    response = client.post(
        "/api/comparator/demo/compare",
        json={
            "campaign_ids": [
                "cmp_demo_emotional_story",
                "cmp_demo_proof_trust",
                "cmp_demo_price_promo",
            ],
        },
    )
    payload = response.get_json()
    data = payload["data"]

    assert response.status_code == 200
    assert payload["success"] is True
    assert data["source"]["source_mode"] == "demo_mode"
    assert data["source"]["data_basis"] == "demo_fixture"
    assert data["ranked_recommendation"]
    assert data["risk_comparison"]
    assert data["trade_offs"]
    for summary in data["campaign_summaries"]:
        assert summary["source"]["source_mode"] == "demo_mode"
        assert summary["segment_strengths"]
        assert summary["segment_weaknesses"]
        assert summary["recommended_use_case"]
    assert "backend_verified" not in str(data)


def test_authenticated_comparator_preserves_backend_verified_only_for_real_records(comparator_context):
    client, headers, org, campaign_service = comparator_context
    campaign_a = _campaign_with_report(campaign_service, org.org_id, "Proof Route", 35, 68, 18)
    campaign_b = _campaign_with_report(campaign_service, org.org_id, "Promo Route", 22, 75, 46)

    response = client.post(
        "/api/comparator/compare",
        headers=headers,
        json={"campaign_ids": [campaign_a.campaign_id, campaign_b.campaign_id]},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["source"]["source_mode"] == "backend_verified"
    assert data["source"]["data_basis"] == "real_simulation"
    assert data["overall_winner"]["source"]["source_mode"] == "backend_verified"


def test_authenticated_comparator_local_estimate_is_not_backend_verified(comparator_context):
    client, headers, org, campaign_service = comparator_context
    campaign_a = campaign_service.create_campaign(org.org_id, "Draft Emotional", objective="message_testing")
    campaign_b = campaign_service.create_campaign(org.org_id, "Draft Promo", objective="message_testing")

    response = client.post(
        "/api/comparator/compare",
        headers=headers,
        json={"campaign_ids": [campaign_a.campaign_id, campaign_b.campaign_id]},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["source"]["source_mode"] == "local_estimate"
    assert data["source"]["data_basis"] == "local_estimate"
    assert "backend_verified" not in str(data["source"])
    for summary in data["campaign_summaries"]:
        assert summary["source"]["source_mode"] == "local_estimate"
