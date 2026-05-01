from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_FACTORY = ROOT / "backend" / "app" / "__init__.py"
MIDDLEWARE = ROOT / "backend" / "app" / "middleware" / "tenant_middleware.py"


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
    assert '"/api/settings/providers"' in source
    assert '"/api/settings/readiness"' in source
    assert '"/api/impact/scenarios"' in source
