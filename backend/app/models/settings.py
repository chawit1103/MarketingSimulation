"""Runtime settings model with production-safe secret handling.

Non-secret runtime preferences are persisted to settings.json. Provider secrets
may be persisted only for local/demo use. Production resolves secrets from the
environment and writes blank secret fields to local JSON.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import os


def _is_masked_secret(value: Any) -> bool:
    return isinstance(value, str) and ("••••" in value or "****" in value)


class SecretProvider:
    """Provider-neutral interface for runtime secrets."""

    def llm_api_key(self) -> str:
        return ""

    def embedding_api_key(self) -> str:
        return ""

    def graph_db_password(self) -> str:
        return ""


class EnvironmentSecretProvider(SecretProvider):
    """Read production secrets from environment/config only."""

    def llm_api_key(self) -> str:
        from ..config import Config

        return os.environ.get("LLM_API_KEY") or getattr(Config, "LLM_API_KEY", "") or ""

    def embedding_api_key(self) -> str:
        from ..config import Config

        return os.environ.get("EMBEDDING_API_KEY") or getattr(Config, "EMBEDDING_API_KEY", "") or ""

    def graph_db_password(self) -> str:
        from ..config import Config

        if Config.is_production():
            return os.environ.get("NEO4J_PASSWORD", "")
        return os.environ.get("NEO4J_PASSWORD") or getattr(Config, "NEO4J_PASSWORD", "") or ""


class LocalDemoFileSecretProvider(SecretProvider):
    """Read secrets from local settings for non-production demo workflows."""

    def __init__(self, settings: "AppSettings"):
        self._settings = settings

    def llm_api_key(self) -> str:
        return self._settings.llm.api_key or ""

    def embedding_api_key(self) -> str:
        return self._settings.embedding.api_key or ""

    def graph_db_password(self) -> str:
        return self._settings.graph_db.password or ""


class ProviderType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    XAI = "xai"
    MISTRAL = "mistral"
    TOGETHER = "together"
    GLM = "glm"
    MINIMAX = "minimax"
    KIMI = "kimi"
    DASHSCOPE = "dashscope"
    HUGGINGFACE = "huggingface"
    BEDROCK = "bedrock"
    VERCEL = "vercel"


class EmbeddingProviderType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GOOGLE = "google"
    COHERE = "cohere"


class GraphDBMode(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"


class Language(str, Enum):
    EN = "en"
    ZH_CN = "zh-CN"
    HI = "hi"
    ES = "es"
    FR = "fr"
    AR = "ar"
    BN = "bn"
    PT = "pt"
    RU = "ru"
    UR = "ur"
    TH = "th"


class LLMSettings(BaseModel):
    provider: ProviderType = ProviderType.OLLAMA
    model: str = "qwen2.5:7b"
    api_key: str = ""
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 600


class TaskLLMOverride(BaseModel):
    """Per-task model override (NER, Report, Simulation, Ontology)."""
    provider: Optional[ProviderType] = None
    model: Optional[str] = None


class TaskLLMSettings(BaseModel):
    ner: Optional[TaskLLMOverride] = None
    report: Optional[TaskLLMOverride] = None
    simulation: Optional[TaskLLMOverride] = None
    ontology: Optional[TaskLLMOverride] = None


class EmbeddingSettings(BaseModel):
    provider: EmbeddingProviderType = EmbeddingProviderType.OLLAMA
    model: str = "nomic-embed-text"
    api_key: str = ""
    base_url: Optional[str] = None


class GraphDBSettings(BaseModel):
    mode: GraphDBMode = GraphDBMode.LOCAL
    uri: str = "bolt://localhost:7687"
    user: str = "neo4j"
    password: str = "mirofish"


class AppSettings(BaseModel):
    language: Language = Language.EN
    llm: LLMSettings = Field(default_factory=LLMSettings)
    task_llm: TaskLLMSettings = Field(default_factory=TaskLLMSettings)
    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    graph_db: GraphDBSettings = Field(default_factory=GraphDBSettings)


class SettingsManager:
    """Singleton settings manager — loads from settings.json, falls back to .env."""

    _instance: Optional["SettingsManager"] = None
    _settings: AppSettings

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    @classmethod
    def invalidate(cls):
        """Force reload on next access (useful for testing)."""
        cls._instance = None

    def _load(self):
        """Load from settings.json, with .env fallback for missing values."""
        import json
        from ..config import Config

        settings_path = os.path.join(Config.UPLOAD_FOLDER, 'settings.json')

        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._settings = AppSettings(**data)
            self._apply_secret_policy()
        else:
            # First run — initialize from .env / defaults
            self._settings = AppSettings(
                llm=LLMSettings(
                    provider=ProviderType.OLLAMA,
                    model=Config.LLM_MODEL_NAME,
                    api_key=Config.LLM_API_KEY,
                    base_url=Config.LLM_BASE_URL,
                ),
                embedding=EmbeddingSettings(
                    provider=EmbeddingProviderType.OLLAMA,
                    model=Config.EMBEDDING_MODEL,
                    api_key=Config.EMBEDDING_API_KEY or "",
                    base_url=Config.EMBEDDING_BASE_URL,
                ),
                graph_db=GraphDBSettings(
                    uri=Config.NEO4J_URI,
                    user=Config.NEO4J_USER,
                    password=Config.NEO4J_PASSWORD,
                ),
            )
            self._apply_secret_policy()
            self.save()

    def _apply_secret_policy(self):
        """Apply local-vs-production secret rules to in-memory settings."""
        from ..config import Config

        env_provider = EnvironmentSecretProvider()
        if Config.is_production():
            self._settings.llm.api_key = env_provider.llm_api_key()
            self._settings.embedding.api_key = env_provider.embedding_api_key()
            self._settings.graph_db.password = env_provider.graph_db_password()
            return

        local_provider = LocalDemoFileSecretProvider(self._settings)
        if not local_provider.llm_api_key() and env_provider.llm_api_key():
            self._settings.llm.api_key = env_provider.llm_api_key()
        if not local_provider.embedding_api_key() and env_provider.embedding_api_key():
            self._settings.embedding.api_key = env_provider.embedding_api_key()
        if not local_provider.graph_db_password() and env_provider.graph_db_password():
            self._settings.graph_db.password = env_provider.graph_db_password()

    @staticmethod
    def _may_persist_secrets() -> bool:
        """Return True only when local/demo file secret storage is allowed."""
        from ..config import Config

        return bool(Config.SETTINGS_PERSIST_SECRETS) and not Config.is_production()

    def save(self):
        """Persist current settings to settings.json."""
        import json
        from ..config import Config

        settings_path = os.path.join(Config.UPLOAD_FOLDER, 'settings.json')
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        try:
            os.chmod(os.path.dirname(settings_path), 0o700)
        except OSError:
            pass
        data = self._settings.model_dump()
        if not self._may_persist_secrets():
            data["llm"]["api_key"] = ""
            data["embedding"]["api_key"] = ""
            data["graph_db"]["password"] = ""

        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        try:
            os.chmod(settings_path, 0o600)
        except OSError:
            pass

    def get(self) -> AppSettings:
        return self._settings

    def update(self, data: Dict[str, Any]):
        """Update settings from dict — validates, saves, invalidates caches."""
        existing = self._settings.model_dump()
        for section, field in (("llm", "api_key"), ("embedding", "api_key"), ("graph_db", "password")):
            incoming_section = data.get(section)
            if not isinstance(incoming_section, dict):
                continue
            if _is_masked_secret(incoming_section.get(field)):
                incoming_section[field] = (existing.get(section) or {}).get(field, "")

        self._settings = AppSettings(**data)
        self._apply_secret_policy()
        self.save()
        # Signal provider reinitialization (lazy import to avoid circular)
        try:
            from ..llm.provider_factory import LLMProviderFactory
            LLMProviderFactory.invalidate_cache()
        except ImportError:
            pass  # LLM module not yet created — fine, will pick up on next get_provider
        try:
            from ..llm.embedding_factory import EmbeddingProviderFactory
            EmbeddingProviderFactory.invalidate_cache()
        except ImportError:
            pass


# Convenience accessor
def get_settings() -> AppSettings:
    return SettingsManager().get()
