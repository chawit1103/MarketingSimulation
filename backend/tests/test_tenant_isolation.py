import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.models.project import ProjectManager  # noqa: E402
from app.models.settings import SettingsManager  # noqa: E402
from app.models.task import TaskManager  # noqa: E402
from app.models.user import UserRole  # noqa: E402
from app.services.auth_service import AuthService  # noqa: E402
from app.services.campaign_service import CampaignService  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.report_agent import Report, ReportManager, ReportStatus  # noqa: E402
from app.services.simulation_manager import SimulationManager  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


@pytest.fixture()
def tenant_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    monkeypatch.setattr(SimulationManager, "SIMULATION_DATA_DIR", str(tmp_path / "simulations"))
    monkeypatch.setattr(ReportManager, "REPORTS_DIR", str(tmp_path / "reports"))
    monkeypatch.setattr(ProjectManager, "PROJECTS_DIR", str(tmp_path / "projects"))

    SettingsManager.invalidate()
    TaskManager._instance = None

    from app.api import campaign as campaign_api  # noqa: E402

    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org_a = org_service.create_org("Tenant A", "tenant-a", "a@example.com")
    org_b = org_service.create_org("Tenant B", "tenant-b", "b@example.com")

    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    user_a = user_service.create_user(
        org_a.org_id,
        "admin-a@example.com",
        "local-test-password",
        name="Admin A",
        role=UserRole.ADMIN,
    )
    user_b = user_service.create_user(
        org_b.org_id,
        "admin-b@example.com",
        "local-test-password",
        name="Admin B",
        role=UserRole.ADMIN,
    )

    campaign_service = CampaignService(upload_folder=str(tmp_path))
    campaign_b = campaign_service.create_campaign(
        org_b.org_id,
        "Tenant B Campaign",
        description="Private campaign for tenant isolation checks.",
        created_by=user_b.user_id,
    )

    project_b = ProjectManager.create_project("Tenant B Project", org_id=org_b.org_id)
    project_b.graph_id = "graph_tenant_b"
    ProjectManager.save_project(project_b)

    simulation_b = SimulationManager().create_simulation(
        project_id=project_b.project_id,
        graph_id=project_b.graph_id,
        org_id=org_b.org_id,
        campaign_id=campaign_b.campaign_id,
    )

    report_b = Report(
        report_id="report_tenant_b",
        simulation_id=simulation_b.simulation_id,
        graph_id=simulation_b.graph_id,
        simulation_requirement="Private tenant B report",
        status=ReportStatus.COMPLETED,
        org_id=org_b.org_id,
        campaign_id=campaign_b.campaign_id,
        markdown_content="# Private report\n\nTenant B only.",
    )
    ReportManager.save_report(report_b)

    app = create_app()
    app.config.update(TESTING=True)
    auth = AuthService()
    headers = {
        "org_a": {"Authorization": f"Bearer {auth.create_token(user_a)}"},
        "org_b": {"Authorization": f"Bearer {auth.create_token(user_b)}"},
    }

    yield {
        "client": app.test_client(),
        "headers": headers,
        "campaign_b": campaign_b,
        "simulation_b": simulation_b,
        "report_b": report_b,
    }

    SettingsManager.invalidate()
    TaskManager._instance = None
    campaign_api._campaign_service = None
    campaign_api._pipeline_orchestrator = None


def _assert_safe_not_found(response, forbidden_id: str):
    assert response.status_code == 404
    payload = response.get_json()
    assert payload["error"] == "Resource not found"
    assert forbidden_id not in str(payload)
    assert "traceback" not in str(payload).lower()


def test_org_a_cannot_read_org_b_campaign_pipeline_status(tenant_context):
    client = tenant_context["client"]
    headers = tenant_context["headers"]
    campaign = tenant_context["campaign_b"]

    response = client.get(
        f"/api/campaign/{campaign.campaign_id}/pipeline/status",
        headers=headers["org_a"],
    )

    _assert_safe_not_found(response, campaign.campaign_id)


def test_org_a_cannot_read_org_b_simulation_or_dashboard(tenant_context):
    client = tenant_context["client"]
    headers = tenant_context["headers"]
    campaign = tenant_context["campaign_b"]
    simulation = tenant_context["simulation_b"]

    sim_response = client.get(f"/api/simulation/{simulation.simulation_id}", headers=headers["org_a"])
    dashboard_response = client.get(
        f"/api/dashboard/campaign/{campaign.campaign_id}/kpi",
        headers=headers["org_a"],
    )

    _assert_safe_not_found(sim_response, simulation.simulation_id)
    _assert_safe_not_found(dashboard_response, campaign.campaign_id)


def test_org_a_cannot_download_or_delete_org_b_report(tenant_context):
    client = tenant_context["client"]
    headers = tenant_context["headers"]
    report = tenant_context["report_b"]

    download_response = client.get(f"/api/report/{report.report_id}/download", headers=headers["org_a"])
    delete_response = client.delete(f"/api/report/{report.report_id}", headers=headers["org_a"])
    owner_response = client.get(f"/api/report/{report.report_id}", headers=headers["org_b"])

    _assert_safe_not_found(download_response, report.report_id)
    _assert_safe_not_found(delete_response, report.report_id)
    assert owner_response.status_code == 200
    assert owner_response.get_json()["data"]["report_id"] == report.report_id


def test_org_b_can_read_its_own_simulation_and_report(tenant_context):
    client = tenant_context["client"]
    headers = tenant_context["headers"]
    simulation = tenant_context["simulation_b"]
    report = tenant_context["report_b"]

    sim_response = client.get(f"/api/simulation/{simulation.simulation_id}", headers=headers["org_b"])
    report_response = client.get(f"/api/report/{report.report_id}", headers=headers["org_b"])

    assert sim_response.status_code == 200
    assert sim_response.get_json()["data"]["simulation_id"] == simulation.simulation_id
    assert report_response.status_code == 200
    assert report_response.get_json()["data"]["report_id"] == report.report_id


def test_unknown_ids_return_safe_not_found_without_leaking_lookup_details(tenant_context):
    client = tenant_context["client"]
    headers = tenant_context["headers"]
    unknown_simulation = "sim_unknown_private"

    response = client.get(f"/api/simulation/{unknown_simulation}", headers=headers["org_a"])

    _assert_safe_not_found(response, unknown_simulation)
