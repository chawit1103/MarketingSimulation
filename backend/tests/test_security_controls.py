import hashlib
import sys
from pathlib import Path

import pytest


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402


def _legacy_hash(password: str) -> str:
    salt = "0" * 32
    return f"{salt}:{hashlib.sha256((salt + password).encode()).hexdigest()}"


def test_new_password_hashes_use_werkzeug_not_legacy_sha256():
    password_hash = User.hash_password("correct horse battery staple")

    assert not User.is_legacy_password_hash(password_hash)
    assert User.verify_password("correct horse battery staple", password_hash)
    assert not User.verify_password("wrong password", password_hash)


def test_legacy_sha256_password_verifies_and_rehashes_on_login(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("Security Test Org", "security-test-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    user = User(
        org_id=org.org_id,
        email="admin@example.com",
        name="Admin",
        role="admin",
        password_hash=_legacy_hash("legacy-secret"),
    )
    user_service._write_user(user)

    app = create_app()
    response = app.test_client().post(
        "/api/auth/login",
        json={"email": "admin@example.com", "password": "legacy-secret"},
    )

    assert response.status_code == 200
    stored = user_service.get_user(user.user_id, org_id=org.org_id)
    assert stored is not None
    assert not User.is_legacy_password_hash(stored.password_hash)
    assert User.verify_password("legacy-secret", stored.password_hash)


def test_rate_limit_blocks_public_demo_after_configured_threshold():
    class RateLimitTestConfig(Config):
        RATE_LIMIT_ENABLED = True
        RATE_LIMIT_WINDOW_SECONDS = 60
        RATE_LIMIT_DEMO_PER_WINDOW = 2

    app = create_app(RateLimitTestConfig)
    client = app.test_client()
    headers = {"X-Forwarded-For": "203.0.113.24"}

    assert client.get("/api/demo/campaigns", headers=headers).status_code == 200
    assert client.get("/api/demo/campaigns", headers=headers).status_code == 200
    limited = client.get("/api/demo/campaigns", headers=headers)

    assert limited.status_code == 429
    assert limited.get_json()["error"] == "Rate limit exceeded"
    assert limited.headers["Retry-After"]


def test_rate_limit_ignores_forwarded_for_from_untrusted_proxy():
    class RateLimitTestConfig(Config):
        RATE_LIMIT_ENABLED = True
        RATE_LIMIT_WINDOW_SECONDS = 60
        RATE_LIMIT_DEMO_PER_WINDOW = 1
        RATE_LIMIT_TRUSTED_PROXIES = "10.0.0.0/8"

    app = create_app(RateLimitTestConfig)
    client = app.test_client()

    first = client.get(
        "/api/demo/campaigns",
        headers={"X-Forwarded-For": "203.0.113.24"},
        environ_overrides={"REMOTE_ADDR": "127.0.0.1"},
    )
    second = client.get(
        "/api/demo/campaigns",
        headers={"X-Forwarded-For": "198.51.100.7"},
        environ_overrides={"REMOTE_ADDR": "127.0.0.1"},
    )

    assert first.status_code == 200
    assert second.status_code == 429


def test_rate_limit_trusts_forwarded_for_from_configured_proxy_only():
    class RateLimitTestConfig(Config):
        RATE_LIMIT_ENABLED = True
        RATE_LIMIT_WINDOW_SECONDS = 60
        RATE_LIMIT_DEMO_PER_WINDOW = 1
        RATE_LIMIT_TRUSTED_PROXIES = "127.0.0.1"

    app = create_app(RateLimitTestConfig)
    client = app.test_client()
    environ = {"REMOTE_ADDR": "127.0.0.1"}

    first = client.get(
        "/api/demo/campaigns",
        headers={"X-Forwarded-For": "203.0.113.24"},
        environ_overrides=environ,
    )
    second = client.get(
        "/api/demo/campaigns",
        headers={"X-Forwarded-For": "198.51.100.7"},
        environ_overrides=environ,
    )
    repeat_first = client.get(
        "/api/demo/campaigns",
        headers={"X-Forwarded-For": "203.0.113.24"},
        environ_overrides=environ,
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert repeat_first.status_code == 429


def test_rate_limited_endpoint_groups_are_configured():
    from app.middleware.rate_limit_middleware import RateLimitMiddleware

    configured_prefixes = {
        prefix
        for _, prefixes, _ in RateLimitMiddleware.GROUPS
        for prefix in prefixes
    }

    assert "/api/auth/login" in configured_prefixes
    assert "/api/auth/register" in configured_prefixes
    assert "/api/demo" in configured_prefixes
    assert "/api/status" in configured_prefixes
    assert "/api/decision" in configured_prefixes
    assert "/api/brief" in configured_prefixes
    assert "/api/competitor" in configured_prefixes
    assert "/api/settings/readiness" in configured_prefixes
    assert "/api/settings/providers" in configured_prefixes
    assert "/api/simulation" in configured_prefixes


def test_response_safety_strips_tracebacks_and_redacts_secret_like_values():
    from app.utils.response_safety import sanitize_api_payload

    payload = {
        "success": False,
        "error": "Provider failed with api_key=sk-testsecret123456789 and password=hunter2",
        "traceback": "Traceback (most recent call last): private stack",
        "nested": {"message": "Authorization: Bearer token1234567890"},
    }

    sanitized, removed = sanitize_api_payload(payload)
    rendered = str(sanitized)

    assert "traceback" not in rendered.lower()
    assert "sk-testsecret" not in rendered
    assert "hunter2" not in rendered
    assert "token1234567890" not in rendered
    assert sanitized["error"] == "Provider failed with api_key=*** and password=***"
    assert sanitized["nested"]["message"] == "Authorization: Bearer ***"
    assert removed
