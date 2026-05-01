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

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', '3c-simulator-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    ENVIRONMENT = (
        os.environ.get("APP_ENV")
        or os.environ.get("FLASK_ENV")
        or os.environ.get("ENV")
        or "development"
    ).lower()

    # Lightweight in-memory rate limiting. Values are requests per window.
    RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
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
    def validate_security(cls, logger=None):
        """Validate production-sensitive security configuration.

        Development can run with the historical fallback secret to preserve the
        local demo flow, but production must provide a real SECRET_KEY.
        """
        logger = logger or logging.getLogger("mirofish.config")
        has_env_secret = bool(os.environ.get("SECRET_KEY"))
        uses_known_secret = cls.SECRET_KEY in cls.KNOWN_FALLBACK_SECRET_KEYS

        if cls.is_production() and (not has_env_secret or uses_known_secret):
            raise RuntimeError(
                "Production requires SECRET_KEY to be set to a non-default value."
            )

        if not cls.is_production() and uses_known_secret:
            logger.warning(
                "Development is using the default SECRET_KEY. Set SECRET_KEY before production."
            )
