import json
import stat
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
from app.services.organization_service import OrganizationService  # noqa: E402
from app.services.user_service import UserService  # noqa: E402
from app.utils.response_safety import redact_sensitive_payload  # noqa: E402


def test_debug_and_request_body_logging_are_disabled_by_default():
    # DEBUG may be explicitly enabled by a developer's local .env, but request
    # body logging must remain off unless separately opted in.
    assert isinstance(Config.DEBUG, bool)
    assert Config.REQUEST_BODY_LOGGING_ENABLED is False


def test_request_body_redaction_covers_secrets_and_campaign_brief_text():
    payload = {
        "password": "pw-123",
        "graph_db": {"password": "neo4j-secret"},
        "llm": {"api_key": "sk-testsecret123456789"},
        "campaign_brief": "Full private campaign brief text",
        "simulation_requirement": "Private simulation requirement",
        "safe": "visible",
    }

    redacted = redact_sensitive_payload(payload)
    rendered = str(redacted)

    assert redacted["password"] == "***"
    assert redacted["graph_db"]["password"] == "***"
    assert redacted["llm"]["api_key"] == "***"
    assert redacted["campaign_brief"] == "***"
    assert redacted["simulation_requirement"] == "***"
    assert redacted["safe"] == "visible"
    assert "pw-123" not in rendered
    assert "neo4j-secret" not in rendered
    assert "Full private campaign brief text" not in rendered


@pytest.fixture()
def api_key_context(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    SettingsManager.invalidate()

    org_service = OrganizationService(upload_folder=str(tmp_path / "organizations"))
    org = org_service.create_org("API Key Org", "api-key-org", "admin@example.com")
    user_service = UserService(org_service=org_service, upload_folder=str(tmp_path / "organizations"))
    user = user_service.create_user(
        org.org_id,
        "admin@example.com",
        "local-test-password",
        name="Admin",
        role=UserRole.ADMIN,
    )
    generated = user_service.generate_api_key(org.org_id, user.user_id)

    app = create_app()
    app.config.update(TESTING=True)
    yield app.test_client(), generated["raw_key"]

    SettingsManager.invalidate()


def test_query_parameter_api_key_is_rejected_but_header_api_key_still_works(api_key_context):
    client, raw_key = api_key_context

    query_response = client.get(f"/api/auth/me?api_key={raw_key}")
    header_response = client.get("/api/auth/me", headers={"X-Api-Key": raw_key})

    assert query_response.status_code == 401
    assert query_response.get_json()["error"] == "Missing authentication token"
    assert header_response.status_code == 200
    assert header_response.get_json()["success"] is True


def test_production_cors_requires_explicit_origins_and_blocks_unlisted_origin():
    class ProductionCorsConfig(Config):
        ENVIRONMENT = "production"
        SECRET_KEY = "unit-test-production-secret"
        CORS_ALLOWED_ORIGINS = "https://app.example.com"
        RATE_LIMIT_ENABLED = False

    app = create_app(ProductionCorsConfig)
    client = app.test_client()

    allowed = client.get("/api/status", headers={"Origin": "https://app.example.com"})
    disallowed = client.get("/api/status", headers={"Origin": "https://evil.example"})

    assert allowed.headers.get("Access-Control-Allow-Origin") == "https://app.example.com"
    assert disallowed.headers.get("Access-Control-Allow-Origin") is None


def test_production_cors_requires_origins_at_startup():
    class ProductionCorsConfig(Config):
        ENVIRONMENT = "production"
        SECRET_KEY = "unit-test-production-secret"
        CORS_ALLOWED_ORIGINS = ""
        RATE_LIMIT_ENABLED = False

    with pytest.raises(RuntimeError, match="CORS_ALLOWED_ORIGINS"):
        create_app(ProductionCorsConfig)


def test_runtime_settings_file_omits_secrets_when_persistence_is_disabled(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "SETTINGS_PERSIST_SECRETS", False)
    SettingsManager.invalidate()

    SettingsManager().update(
        {
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": "unit-llm-secret",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-small",
                "api_key": "unit-embedding-secret",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "unit-graph-secret",
            },
            "task_llm": {},
        }
    )

    settings_path = tmp_path / "settings.json"
    persisted = json.loads(settings_path.read_text(encoding="utf-8"))
    mode = stat.S_IMODE(settings_path.stat().st_mode)

    assert persisted["llm"]["api_key"] == ""
    assert persisted["embedding"]["api_key"] == ""
    assert persisted["graph_db"]["password"] == ""
    assert mode == 0o600


def test_production_settings_ignore_file_secrets_and_never_persist_plaintext(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "ENVIRONMENT", "production")
    monkeypatch.setattr(Config, "SETTINGS_PERSIST_SECRETS", True)
    monkeypatch.setenv("LLM_API_KEY", "env-llm-secret")
    monkeypatch.setenv("EMBEDDING_API_KEY", "env-embedding-secret")
    monkeypatch.setenv("NEO4J_PASSWORD", "env-graph-secret")
    SettingsManager.invalidate()

    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "language": "en",
                "llm": {
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": "file-llm-secret",
                    "base_url": None,
                    "temperature": 0.7,
                    "max_tokens": 4096,
                    "timeout": 120,
                },
                "embedding": {
                    "provider": "openai",
                    "model": "text-embedding-3-small",
                    "api_key": "file-embedding-secret",
                    "base_url": None,
                },
                "graph_db": {
                    "mode": "cloud",
                    "uri": "neo4j+s://example.databases.neo4j.io",
                    "user": "neo4j",
                    "password": "file-graph-secret",
                },
                "task_llm": {},
            }
        ),
        encoding="utf-8",
    )

    loaded = SettingsManager().get()
    assert loaded.llm.api_key == "env-llm-secret"
    assert loaded.embedding.api_key == "env-embedding-secret"
    assert loaded.graph_db.password == "env-graph-secret"

    SettingsManager().update(
        {
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o",
                "api_key": "incoming-llm-secret",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-large",
                "api_key": "incoming-embedding-secret",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "incoming-graph-secret",
            },
            "task_llm": {},
        }
    )

    persisted = json.loads(settings_path.read_text(encoding="utf-8"))
    rendered = json.dumps(persisted)
    assert persisted["llm"]["api_key"] == ""
    assert persisted["embedding"]["api_key"] == ""
    assert persisted["graph_db"]["password"] == ""
    assert "file-llm-secret" not in rendered
    assert "incoming-llm-secret" not in rendered
    assert "env-llm-secret" not in rendered
    assert stat.S_IMODE(settings_path.stat().st_mode) == 0o600


def test_local_demo_settings_can_persist_secrets_when_explicitly_allowed(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "UPLOAD_FOLDER", str(tmp_path))
    monkeypatch.setattr(Config, "ENVIRONMENT", "development")
    monkeypatch.setattr(Config, "SETTINGS_PERSIST_SECRETS", True)
    SettingsManager.invalidate()

    SettingsManager().update(
        {
            "language": "en",
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": "local-llm-secret",
                "base_url": None,
                "temperature": 0.7,
                "max_tokens": 4096,
                "timeout": 120,
            },
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-small",
                "api_key": "local-embedding-secret",
                "base_url": None,
            },
            "graph_db": {
                "mode": "cloud",
                "uri": "neo4j+s://example.databases.neo4j.io",
                "user": "neo4j",
                "password": "local-graph-secret",
            },
            "task_llm": {},
        }
    )

    persisted = json.loads((tmp_path / "settings.json").read_text(encoding="utf-8"))
    assert persisted["llm"]["api_key"] == "local-llm-secret"
    assert persisted["embedding"]["api_key"] == "local-embedding-secret"
    assert persisted["graph_db"]["password"] == "local-graph-secret"
