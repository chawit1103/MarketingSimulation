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
from app.services.calibration_service import CalibrationService, CalibrationValidationError  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


def test_calibration_compares_actuals_against_estimates(tmp_path):
    service = CalibrationService(storage_dir=str(tmp_path))

    result = service.import_actual_results(
        org_id="org_a",
        payload={
            "campaign_id": "cmp_1",
            "impressions": 120000,
            "clicks": 3600,
            "ctr": 3.0,
            "conversion_rate": 1.4,
            "sentiment_score": 62,
            "crisis_incident_flag": False,
            "estimate": {
                "impressions": 100000,
                "clicks": 3000,
                "ctr": 2.5,
                "conversion_rate": 1.2,
                "sentiment_score": 58,
                "crisis_risk": 25,
            },
            "qualitative_notes": "Aggregate sales team feedback was positive after launch.",
        },
    )

    assert result["campaign_id"] == "cmp_1"
    assert result["calibration_status"] == "partially_calibrated"
    assert result["risk_classification"] == "matched_no_crisis"
    assert result["source"]["data_basis"] == "manual_actual_import"
    assert "org_id" not in result
    ctr = next(row for row in result["comparison"] if row["metric"] == "ctr")
    assert ctr["estimate"] == 2.5
    assert ctr["actual"] == 3.0
    assert ctr["delta"] == 0.5


def test_calibration_status_reaches_calibrated_with_campaign_count(tmp_path):
    service = CalibrationService(storage_dir=str(tmp_path))
    for idx in range(3):
        result = service.import_actual_results(
            org_id="org_a",
            payload={
                "campaign_id": f"cmp_{idx}",
                "impressions": 1000 + idx,
                "estimated_impressions": 900 + idx,
            },
        )

    assert result["calibration_status"] == "calibrated_with_3_campaigns"
    status = service.get_status("org_a", "cmp_2")
    assert status["calibration_status"] == "calibrated_with_3_campaigns"


def test_calibration_rejects_pii_and_raw_data_fields(tmp_path):
    service = CalibrationService(storage_dir=str(tmp_path))

    with pytest.raises(CalibrationValidationError):
        service.import_actual_results(
            org_id="org_a",
            payload={
                "campaign_id": "cmp_1",
                "impressions": 1000,
                "customer_list": [{"email": "person@example.com"}],
            },
        )

    with pytest.raises(CalibrationValidationError):
        service.import_actual_results(
            org_id="org_a",
            payload={
                "campaign_id": "cmp_1",
                "impressions": 1000,
                "qualitative_notes": "Please call 081-234-5678 for the raw lead sample.",
            },
        )


def test_calibration_parses_single_row_csv(tmp_path):
    service = CalibrationService(storage_dir=str(tmp_path))

    payload = service.parse_csv_text(
        "campaign_id,impressions,estimated_impressions,crisis_incident_flag\n"
        "cmp_csv,25000,20000,false\n"
    )
    result = service.import_actual_results(org_id="org_a", payload=payload)

    assert result["campaign_id"] == "cmp_csv"
    assert result["comparison"][0]["metric"] == "impressions"
    assert result["risk_classification"] == "not_available"


@pytest.fixture()
def calibration_api_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    SettingsManager.invalidate()

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("Calibration Org", "calibration-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    analyst = user_service.create_user(
        org.org_id,
        "analyst@example.com",
        "local-test-password",
        name="Analyst",
        role=UserRole.ANALYST,
    )
    viewer = user_service.create_user(
        org.org_id,
        "viewer@example.com",
        "local-test-password",
        name="Viewer",
        role=UserRole.VIEWER,
    )

    app = create_app()
    app.config.update(TESTING=True)

    from app.api import calibration as calibration_api  # noqa: E402

    calibration_api.calibration_service = CalibrationService(storage_dir=str(tmp_path / "calibration"))
    auth = AuthService()
    headers = {
        "analyst": {"Authorization": f"Bearer {auth.create_token(analyst)}"},
        "viewer": {"Authorization": f"Bearer {auth.create_token(viewer)}"},
    }

    yield app.test_client(), headers
    SettingsManager.invalidate()


def test_calibration_api_requires_analyst_for_import(calibration_api_context):
    client, headers = calibration_api_context

    viewer_response = client.post(
        "/api/calibration/actual-results",
        headers=headers["viewer"],
        json={"campaign_id": "cmp_1", "impressions": 1000},
    )
    analyst_response = client.post(
        "/api/calibration/actual-results",
        headers=headers["analyst"],
        json={
            "campaign_id": "cmp_1",
            "impressions": 1200,
            "estimated_impressions": 1000,
        },
    )

    assert viewer_response.status_code == 403
    assert analyst_response.status_code == 201
    assert analyst_response.get_json()["data"]["calibration_status"] == "partially_calibrated"
    assert "traceback" not in str(analyst_response.get_json()).lower()


def test_calibration_api_rejects_raw_customer_data(calibration_api_context):
    client, headers = calibration_api_context

    response = client.post(
        "/api/calibration/actual-results",
        headers=headers["analyst"],
        json={
            "campaign_id": "cmp_1",
            "impressions": 1000,
            "raw_posts": ["this should not be ingested"],
        },
    )

    assert response.status_code == 422
    payload = response.get_json()
    assert payload["code"] == "calibration_validation_failed"
    assert "traceback" not in str(payload).lower()
