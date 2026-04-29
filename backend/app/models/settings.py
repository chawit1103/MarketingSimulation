"""Runtime settings model — persisted to settings.json, with .env fallback."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


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
        import os
        from ..config import Config

        settings_path = os.path.join(Config.UPLOAD_FOLDER, 'settings.json')

        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._settings = AppSettings(**data)
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
                    base_url=Config.EMBEDDING_BASE_URL,
                ),
                graph_db=GraphDBSettings(
                    uri=Config.NEO4J_URI,
                    user=Config.NEO4J_USER,
                    password=Config.NEO4J_PASSWORD,
                ),
            )
            self.save()

    def save(self):
        """Persist current settings to settings.json."""
        import json
        import os
        from ..config import Config

        settings_path = os.path.join(Config.UPLOAD_FOLDER, 'settings.json')
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(self._settings.model_dump(), f, indent=2, ensure_ascii=False)

    def get(self) -> AppSettings:
        return self._settings

    def update(self, data: Dict[str, Any]):
        """Update settings from dict — validates, saves, invalidates caches."""
        self._settings = AppSettings(**data)
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
