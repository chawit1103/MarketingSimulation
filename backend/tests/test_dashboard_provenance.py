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
from app.services.campaign_service import CampaignService  # noqa: E402
from app.services.kpi_calculator import KPICalculator  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


@pytest.fixture()
def dashboard_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    SettingsManager.invalidate()

    from app.api import campaign as campaign_api  # noqa: E402

    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("Dashboard Trust Org", "dashboard-trust-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    user = user_service.create_user(
        org.org_id,
        "admin@example.com",
        "local-test-password",
        name="Admin",
        role=UserRole.ADMIN,
    )
    campaign = CampaignService(upload_folder=str(tmp_path)).create_campaign(
        org.org_id,
        "Trust Campaign",
        description="Campaign used for dashboard provenance tests.",
        created_by=user.user_id,
    )

    app = create_app()
    app.config.update(TESTING=True)
    headers = {"Authorization": f"Bearer {AuthService().create_token(user)}"}

    yield app.test_client(), headers, campaign

    SettingsManager.invalidate()
    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None


def test_unknown_campaign_does_not_return_plausible_backend_verified_kpis(dashboard_context):
    client, headers, _ = dashboard_context

    response = client.get("/api/dashboard/campaign/cmp_unknown/kpi", headers=headers)
    payload = response.get_json()

    assert response.status_code == 404
    assert payload["error"] == "Resource not found"
    assert "backend_verified" not in str(payload)
    assert "overall_sentiment" not in str(payload)


def test_dashboard_mock_fallback_is_labeled_local_estimate(dashboard_context):
    client, headers, campaign = dashboard_context

    response = client.get(f"/api/dashboard/campaign/{campaign.campaign_id}/kpi", headers=headers)
    payload = response.get_json()

    assert response.status_code == 200
    data = payload["data"]
    assert data["source"]["type"] == "local_estimate"
    assert data["source"]["source_mode"] == "local_estimate"
    assert data["source"]["data_basis"] == "local_estimate"
    assert data["action_plan"]["source"]["type"] == "local_estimate"
    assert data["source"]["campaign_id"] == campaign.campaign_id
    assert "backend_verified" not in str(data["source"])


def test_real_simulation_kpi_input_is_labeled_backend_verified():
    report = KPICalculator().calculate(
        campaign_id="cmp_real",
        org_id="org_real",
        simulation_id="sim_real",
        simulation_data={
            "simulation_id": "sim_real",
            "run_id": "run_real",
            "confidence_score": 81,
            "kpis": {
                "overall_sentiment": 22.5,
                "conversion_probability": 64.0,
                "crisis_risk": 18.0,
                "social_influence_index": 71.0,
                "message_resonance": 69.0,
                "brand_perception_shift": 8.0,
                "opinion_polarization": 27.0,
            },
            "segments": [
                {"segment_name": "All personas", "persona_count": 100, "avg_sentiment": 22.5},
            ],
            "timeline": [
                {"round_num": 1, "simulated_hour": 1, "avg_sentiment": 22.5, "action_count": 12},
            ],
        },
    )

    assert report.source_mode == "backend_verified"
    assert report.data_basis == "real_simulation"
    assert report.simulation_id == "sim_real"
    assert report.run_id == "run_real"
    assert report.confidence == 81
    assert report.overall_sentiment == 22.5
