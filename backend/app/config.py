"""
Configuration Management
Loads configuration from .env file in project root directory
"""

import os
import logging
from dotenv import load_dotenv

# Load .env file from project root
# Path: 3C-Simulator/.env (relative to backend/app/config.py)
project_root_env = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    # If no .env in root, try to load environment variables (for production)
    load_dotenv(override=True)


class Config:
    """Flask configuration class"""

    KNOWN_FALLBACK_SECRET_KEYS = {
        "3c-simulator-secret-key",
        "3c-simulator-auth-fallback",
        "change-me",
        "changeme",
        "secret",
    }

    ENVIRONMENT = (
        os.environ.get("APP_ENV")
        or os.environ.get("FLASK_ENV")
        or os.environ.get("ENV")
        or "development"
    ).lower()
    IS_PRODUCTION_ENV = ENVIRONMENT in {"prod", "production"}

    # Flask configuration. Debug/body logging are opt-in so production and
    # shared development environments do not accidentally log sensitive briefs.
    SECRET_KEY = os.environ.get('SECRET_KEY', '3c-simulator-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() in {"1", "true", "yes", "on"}
    REQUEST_BODY_LOGGING_ENABLED = (
        os.environ.get('REQUEST_BODY_LOGGING_ENABLED', 'false').lower() in {"1", "true", "yes", "on"}
    )
    CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").strip()
    SECURITY_HEADERS_ENABLED = os.environ.get("SECURITY_HEADERS_ENABLED", "true").lower() in {
        "1", "true", "yes", "on"
    }
    CONTENT_SECURITY_POLICY = os.environ.get(
        "CONTENT_SECURITY_POLICY",
        "default-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "font-src 'self' data:; "
        "connect-src 'self' http://localhost:* http://127.0.0.1:* ws://localhost:* ws://127.0.0.1:*; "
        "form-action 'self'; "
        "upgrade-insecure-requests"
    )
    AUTH_TOKEN_EXPIRY_SECONDS = int(
        os.environ.get(
            "AUTH_TOKEN_EXPIRY_SECONDS",
            "28800" if IS_PRODUCTION_ENV else "86400",
        )
    )
    SETTINGS_PERSIST_SECRETS = (
        os.environ.get("SETTINGS_PERSIST_SECRETS", "false" if IS_PRODUCTION_ENV else "true").lower()
        in {"1", "true", "yes", "on"}
    )

    # Lightweight in-memory rate limiting. Values are requests per window.
    RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_BACKEND = os.environ.get("RATE_LIMIT_BACKEND", "memory").strip().lower()
    RATE_LIMIT_TRUSTED_PROXIES = os.environ.get("RATE_LIMIT_TRUSTED_PROXIES", "").strip()
    RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", "60"))
    RATE_LIMIT_AUTH_PER_WINDOW = int(os.environ.get("RATE_LIMIT_AUTH_PER_WINDOW", "20"))
    RATE_LIMIT_DEMO_PER_WINDOW = int(os.environ.get("RATE_LIMIT_DEMO_PER_WINDOW", "120"))
    RATE_LIMIT_STATUS_PER_WINDOW = int(os.environ.get("RATE_LIMIT_STATUS_PER_WINDOW", "120"))
    RATE_LIMIT_DECISION_PER_WINDOW = int(os.environ.get("RATE_LIMIT_DECISION_PER_WINDOW", "60"))
    RATE_LIMIT_SIMULATION_PER_WINDOW = int(os.environ.get("RATE_LIMIT_SIMULATION_PER_WINDOW", "30"))

    # JSON configuration - disable ASCII escaping to display Chinese directly (not as \uXXXX)
    JSON_AS_ASCII = False

    # LLM configuration (unified OpenAI format)
    LLM_API_KEY = os.environ.get('LLM_API_KEY')
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'http://localhost:11434/v1')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'qwen2.5:32b')

    # Neo4j configuration
    NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', '3c-simulator')

    # Embedding configuration
    EMBEDDING_API_KEY = os.environ.get('EMBEDDING_API_KEY')
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'nomic-embed-text')
    EMBEDDING_BASE_URL = os.environ.get('EMBEDDING_BASE_URL', 'http://localhost:11434')

    # File upload configuration
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt', 'markdown'}

    # Text processing configuration
    DEFAULT_CHUNK_SIZE = 500  # Default chunk size
    DEFAULT_CHUNK_OVERLAP = 50  # Default overlap size

    # OASIS simulation configuration
    OASIS_DEFAULT_MAX_ROUNDS = int(os.environ.get('OASIS_DEFAULT_MAX_ROUNDS', '10'))
    OASIS_SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), '../uploads/simulations')

    # OASIS platform available actions configuration
    OASIS_TWITTER_ACTIONS = [
        'CREATE_POST', 'LIKE_POST', 'REPOST', 'FOLLOW', 'DO_NOTHING', 'QUOTE_POST'
    ]
    OASIS_REDDIT_ACTIONS = [
        'LIKE_POST', 'DISLIKE_POST', 'CREATE_POST', 'CREATE_COMMENT',
        'LIKE_COMMENT', 'DISLIKE_COMMENT', 'SEARCH_POSTS', 'SEARCH_USER',
        'TREND', 'REFRESH', 'DO_NOTHING', 'FOLLOW', 'MUTE'
    ]

    # Report Agent configuration
    REPORT_AGENT_MAX_TOOL_CALLS = int(os.environ.get('REPORT_AGENT_MAX_TOOL_CALLS', '5'))
    REPORT_AGENT_MAX_REFLECTION_ROUNDS = int(os.environ.get('REPORT_AGENT_MAX_REFLECTION_ROUNDS', '2'))
    REPORT_AGENT_TEMPERATURE = float(os.environ.get('REPORT_AGENT_TEMPERATURE', '0.5'))

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        if not cls.LLM_API_KEY:
            errors.append("LLM_API_KEY not configured (set to any non-empty value, e.g. 'ollama')")
        if not cls.NEO4J_URI:
            errors.append("NEO4J_URI not configured")
        if not cls.NEO4J_PASSWORD:
            errors.append("NEO4J_PASSWORD not configured")
        return errors

    @classmethod
    def is_production(cls) -> bool:
        """Return True when the app is running in a production environment."""
        return cls.ENVIRONMENT in {"prod", "production"}

    @classmethod
    def get_cors_origins(cls):
        """Return configured CORS origins.

        Development preserves easy local testing with '*'. Production never
        defaults to wildcard; operators must set CORS_ALLOWED_ORIGINS.
        """
        configured = getattr(cls, "CORS_ALLOWED_ORIGINS", "")
        if configured:
            return [item.strip() for item in configured.split(",") if item.strip()]
        if cls.is_production():
            return []
        return "*"

    @classmethod
    def validate_security(cls, logger=None):
        """Validate production-sensitive security configuration.

        Development can run with the historical fallback secret to preserve the
        local demo flow, but production must provide a real SECRET_KEY.
        """
        logger = logger or logging.getLogger("mirofish.config")
        uses_known_secret = cls.SECRET_KEY in cls.KNOWN_FALLBACK_SECRET_KEYS
        has_non_default_secret = bool(cls.SECRET_KEY) and not uses_known_secret

        if cls.is_production() and not has_non_default_secret:
            raise RuntimeError(
                "Production requires SECRET_KEY to be set to a non-default value."
            )
        if cls.is_production() and not cls.get_cors_origins():
            raise RuntimeError(
                "Production requires CORS_ALLOWED_ORIGINS to be set to explicit trusted origins."
            )
        if cls.is_production() and cls.get_cors_origins() == "*":
            raise RuntimeError(
                "Production requires CORS_ALLOWED_ORIGINS to be set to explicit trusted origins."
            )

        if not cls.is_production() and uses_known_secret:
            logger.warning(
                "Development is using the default SECRET_KEY. Set SECRET_KEY before production."
            )
        if cls.is_production() and getattr(cls, "REQUEST_BODY_LOGGING_ENABLED", False):
            logger.warning(
                "REQUEST_BODY_LOGGING_ENABLED is enabled in production. Redaction is applied, "
                "but request body logging should remain disabled unless temporarily debugging."
            )
        if cls.is_production() and getattr(cls, "RATE_LIMIT_BACKEND", "memory") == "memory":
            logger.warning(
                "Production is using the in-memory rate limiter. Use edge/API-gateway "
                "or shared-store rate limiting before public internet exposure."
            )
