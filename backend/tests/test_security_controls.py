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
    assert "/api/simulation" in configured_prefixes
