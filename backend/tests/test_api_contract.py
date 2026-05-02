from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT / "backend"
APP_FACTORY = ROOT / "backend" / "app" / "__init__.py"
MIDDLEWARE = ROOT / "backend" / "app" / "middleware" / "tenant_middleware.py"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def test_product_blueprints_are_registered_under_api_prefix():
    source = APP_FACTORY.read_text(encoding="utf-8")
    expected_prefixes = [
        "/api/industry",
        "/api/comparator",
        "/api/impact",
        "/api/competitor",
        "/api/export",
        "/api/demo",
        "/api/status",
        "/api/decision",
        "/api/brief",
    ]

    for prefix in expected_prefixes:
        assert f"url_prefix='{prefix}'" in source or f'url_prefix="{prefix}"' in source


def test_demo_and_status_are_public_for_no_key_onboarding():
    source = MIDDLEWARE.read_text(encoding="utf-8")
    assert '"/api/demo"' in source
    assert '"/api/status"' in source
    assert '"/api/decision"' in source
    assert '"/api/brief"' in source
    assert '"/api/competitor"' in source
    assert '"/api/comparator/demo"' in source
    assert '"/api/settings/providers"' in source
    assert '"/api/settings/readiness"' in source
    assert '"/api/impact/scenarios"' in source


def test_critical_frontend_routes_exist_in_backend_url_map(monkeypatch):
    from app import create_app
    from app.config import Config

    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    app = create_app()

    available = {
        (rule.rule, method)
        for rule in app.url_map.iter_rules()
        for method in rule.methods
    }
    expected = [
        ("GET", "/api/demo/campaigns"),
        ("GET", "/api/demo/campaigns/<demo_id>/dashboard"),
        ("POST", "/api/brief/quality"),
        ("POST", "/api/brief/revise"),
        ("POST", "/api/decision/analyze"),
        ("POST", "/api/decision/what-if"),
        ("POST", "/api/decision/budget-scenario"),
        ("POST", "/api/comparator/compare"),
        ("GET", "/api/comparator/metrics"),
        ("GET", "/api/comparator/demo/campaigns"),
        ("POST", "/api/comparator/demo/compare"),
        ("GET", "/api/impact/scenarios/<sentiment_value>"),
        ("GET", "/api/competitor/scenarios"),
        ("POST", "/api/competitor/simulate"),
        ("POST", "/api/export/pptx"),
        ("POST", "/api/export/csv"),
        ("POST", "/api/export/strategy-pack"),
        ("GET", "/api/settings/providers"),
        ("POST", "/api/settings/readiness"),
        ("POST", "/api/report/generate/status"),
        ("POST", "/api/campaign"),
        ("GET", "/api/campaign"),
        ("GET", "/api/campaign/<campaign_id>"),
        ("POST", "/api/campaign/<campaign_id>/pipeline/start"),
        ("GET", "/api/campaign/<campaign_id>/pipeline/status"),
        ("GET", "/api/dashboard/campaign/<campaign_id>/kpi"),
        ("GET", "/api/dashboard/campaign/<campaign_id>/report"),
        ("GET", "/api/dashboard/campaign/<campaign_id>/timeline"),
        ("GET", "/api/dashboard/campaign/<campaign_id>/segments"),
        ("POST", "/api/simulation/create"),
        ("POST", "/api/simulation/prepare"),
        ("POST", "/api/simulation/prepare/status"),
        ("GET", "/api/simulation/<simulation_id>"),
        ("GET", "/api/simulation/list"),
        ("POST", "/api/simulation/start"),
        ("POST", "/api/simulation/stop"),
        ("GET", "/api/simulation/<simulation_id>/run-status"),
        ("GET", "/api/simulation/<simulation_id>/run-status/detail"),
    ]

    for method, route in expected:
        assert (route, method) in available
