"""Multi-Country Persona Context Registry.

Loads the correct persona context data based on language/country code.
Each context file exposes the same structure: archetypes, regions, names, etc.
"""
from typing import Dict, Any
import importlib
import logging

logger = logging.getLogger('mirofish.persona_context')

LANG_TO_MODULE = {
    "en": "english_context",
    "zh-CN": "chinese_context",
    "zh": "chinese_context",
    "hi": "indian_context",
    "es": "spanish_context",
    "fr": "french_context",
    "ar": "arabic_context",
    "bn": "bengali_context",
    "pt": "brazilian_context",
    "ru": "russian_context",
    "ur": "pakistani_context",
    "th": "thai_context",
}


class ContextRegistry:
    """Registry that loads and caches persona context by language."""

    _cache: Dict[str, Any] = {}

    @classmethod
    def get_context(cls, language: str = "en"):
        module_name = LANG_TO_MODULE.get(language, "english_context")

        if module_name in cls._cache:
            return cls._cache[module_name]

        try:
            mod = importlib.import_module(
                f".{module_name}",
                package="app.services.persona_context",
            )
            cls._cache[module_name] = mod
            logger.info(f"Loaded persona context: {module_name} for language {language}")
            return mod
        except ImportError as e:
            logger.warning(f"No persona context for {language} ({module_name}): {e}, falling back to English")
            if module_name != "english_context":
                return cls.get_context("en")
            raise

    @classmethod
    def available_languages(cls) -> list:
        return list(LANG_TO_MODULE.keys())

    @classmethod
    def invalidate(cls):
        cls._cache.clear()
