"""Settings API — read/update runtime configuration at /api/settings."""
import re
from copy import deepcopy
from typing import Any

from flask import Blueprint, request, jsonify
from ..models.settings import SettingsManager, ProviderType, EmbeddingProviderType, GraphDBMode

settings_bp = Blueprint('settings', __name__)

SECRET_FIELD_NAMES = {
    "api_key",
    "apikey",
    "apiKey",
    "password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "credential",
    "credentials",
}
SECRET_PRESENCE_FIELDS = {
    "api_key_present",
    "has_api_key",
    "password_present",
    "has_password",
}


def _sanitize_error(error: Exception | str) -> str:
    """Return an actionable error without leaking keys/tokens/long internals."""
    message = str(error)
    message = re.sub(r"(sk-[A-Za-z0-9_\-]{8,})", "sk-***", message)
    message = re.sub(r"([A-Za-z0-9_\-]{24,})", "***", message)
    message = message.replace("\n", " ")
    return message[:220] or "Connection failed"


def _is_masked_secret(value: str | None) -> bool:
    return bool(value) and ("••••" in value or "****" in value)


def _is_blank_secret(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def _is_secret_field(key: str) -> bool:
    normalized = str(key).replace("-", "_").lower()
    if normalized in SECRET_PRESENCE_FIELDS:
        return False
    return normalized in {item.lower() for item in SECRET_FIELD_NAMES}


def _secret_present(value: Any) -> bool:
    return not _is_blank_secret(value)


def _without_secret_fields(value: Any) -> Any:
    """Remove credential-like fields from nested settings responses."""
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            if _is_secret_field(key):
                continue
            clean[key] = _without_secret_fields(item)
        return clean
    if isinstance(value, list):
        return [_without_secret_fields(item) for item in value]
    return value


def _safe_settings_response(settings) -> dict:
    """Return settings for browsers with secret presence flags only."""
    data = settings.model_dump()

    llm = data.get("llm") or {}
    llm["api_key_present"] = _secret_present(llm.get("api_key"))
    llm.pop("api_key", None)

    embedding = data.get("embedding") or {}
    embedding["api_key_present"] = _secret_present(embedding.get("api_key"))
    embedding.pop("api_key", None)

    graph_db = data.get("graph_db") or {}
    graph_db["password_present"] = _secret_present(graph_db.get("password"))
    graph_db.pop("password", None)

    return _without_secret_fields(data)


def _merge_secret_value(existing: dict, incoming: dict, field: str, clear_flag: str) -> None:
    """Merge one secret field without letting blank/masked placeholders erase it."""
    if incoming.get(clear_flag) is True:
        existing[field] = ""
        return

    if field not in incoming:
        return

    value = incoming.get(field)
    if _is_blank_secret(value) or _is_masked_secret(str(value)):
        return

    existing[field] = str(value)


def _merge_settings_update(existing_settings, incoming: dict) -> dict:
    """Merge browser settings updates while preserving saved secrets by default."""
    merged = deepcopy(existing_settings.model_dump())

    for key, value in incoming.items():
        if key in SECRET_PRESENCE_FIELDS:
            continue
        if key not in {"llm", "embedding", "graph_db"}:
            merged[key] = value

    for section_name in ("llm", "embedding", "graph_db"):
        section_payload = incoming.get(section_name)
        if not isinstance(section_payload, dict):
            continue

        merged_section = merged.setdefault(section_name, {})
        secret_field = "password" if section_name == "graph_db" else "api_key"
        clear_flag = "password_clear" if section_name == "graph_db" else "api_key_clear"

        for key, value in section_payload.items():
            if key in SECRET_PRESENCE_FIELDS or key == clear_flag:
                continue
            if _is_secret_field(key):
                continue
            merged_section[key] = value

        _merge_secret_value(merged_section, section_payload, secret_field, clear_flag)

    return merged


def _safe_provider(provider: str, enum_cls) -> str:
    try:
        return enum_cls(provider).value
    except Exception:
        return ""


def _check_provider_config(config: dict, enum_cls, *, local_provider: str = "ollama") -> dict:
    provider = _safe_provider(str(config.get("provider") or ""), enum_cls)
    model = str(config.get("model") or "").strip()
    api_key = str(config.get("api_key") or config.get("apiKey") or "").strip()
    api_key_present = bool(config.get("api_key_present") or config.get("has_api_key") or api_key)
    base_url = str(config.get("base_url") or config.get("baseUrl") or "").strip()
    issues = []

    if not provider:
        issues.append("Unsupported provider selected.")
    if not model:
        issues.append("Model name is required.")
    if provider == local_provider and not base_url:
        issues.append("Local provider requires a base URL.")
    if provider and provider != local_provider and not api_key_present:
        issues.append("Cloud provider requires an API key.")
    if _is_masked_secret(api_key):
        issues.append("Saved API key is masked; enter the key again before testing or saving.")

    return {
        "status": "ready" if not issues else "needs_attention",
        "provider": provider or config.get("provider") or "unknown",
        "model": model or "not set",
        "issues": issues,
        "safe_detail": "Configuration is complete." if not issues else issues[0],
    }


def _check_graph_config(config: dict) -> dict:
    uri = str(config.get("uri") or "").strip()
    user = str(config.get("user") or "").strip()
    password = str(config.get("password") or "").strip()
    password_present = bool(config.get("password_present") or config.get("has_password") or password)
    mode = str(config.get("mode") or "local")
    issues = []

    if mode not in ("local", "cloud", "neo4j", "bolt"):
        issues.append("Unsupported graph mode selected.")
    if not uri:
        issues.append("Neo4j URI is required.")
    if not user:
        issues.append("Neo4j user is required.")
    if not password_present:
        issues.append("Neo4j password is required.")
    if _is_masked_secret(password):
        issues.append("Saved graph password is masked; enter it again before testing or saving.")

    return {
        "status": "ready" if not issues else "needs_attention",
        "mode": mode,
        "uri": uri or "not set",
        "issues": issues,
        "safe_detail": "Neo4j configuration is complete." if not issues else issues[0],
    }


def _readiness_payload(data: dict) -> dict:
    mode = data.get("mode") or "demo"
    llm = data.get("llm") or {}
    embedding = data.get("embedding") or {}
    graph = data.get("graph_db") or data.get("graphdb") or {}

    if mode == "demo":
        checks = {
            "llm": {"status": "skipped", "safe_detail": "Demo mode does not require an LLM provider."},
            "embedding": {"status": "skipped", "safe_detail": "Demo mode does not require an embedding provider."},
            "neo4j": {"status": "skipped", "safe_detail": "Demo mode does not require Neo4j."},
        }
    else:
        checks = {
            "llm": _check_provider_config(llm, ProviderType),
            "embedding": _check_provider_config(embedding, EmbeddingProviderType),
            "neo4j": _check_graph_config(graph),
        }

    ready = all(item["status"] in ("ready", "skipped") for item in checks.values())
    return {
        "mode": mode,
        "ready": ready,
        "checks": checks,
        "sample_simulation": {
            "status": "available" if ready else "blocked",
            "label": "Try Sample Campaign",
            "detail": "Use a deterministic demo campaign to verify the UI flow before live spend.",
        },
        "cost_estimate": {
            "label": "Directional estimate only",
            "currency": "USD",
            "per_100_personas": 0 if mode in ("demo", "local") else 1.2,
            "disclaimer": "Estimate only. Actual model costs depend on provider pricing, tokens, retries, and prompt length.",
        },
    }


@settings_bp.route('', methods=['GET'])
def get_settings():
    """Get current settings with secret presence flags only."""
    mgr = SettingsManager()
    settings = mgr.get()
    data = _safe_settings_response(settings)

    return jsonify({'success': True, 'settings': data})


@settings_bp.route('', methods=['PUT'])
def update_settings():
    """Update runtime settings. Triggers provider reinitialization."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    try:
        mgr = SettingsManager()
        mgr.update(_merge_settings_update(mgr.get(), data))
        return jsonify({'success': True, 'message': 'Settings updated and providers reinitialized'})
    except Exception as e:
        return jsonify({'success': False, 'error': _sanitize_error(e)}), 400


@settings_bp.route('/providers', methods=['GET'])
def list_providers():
    """List available LLM/embedding providers and their common models."""
    return jsonify({
        'success': True,
        'llm_providers': [
            {
                'id': 'ollama',
                'name': 'Ollama (Local)',
                'needs_base_url': True,
                'default_base_url': 'http://localhost:11434/v1',
                'models': [
                    {'id': 'qwen2.5:7b', 'name': 'Qwen 2.5 7B', 'context': 32768},
                    {'id': 'qwen2.5:14b', 'name': 'Qwen 2.5 14B', 'context': 32768},
                    {'id': 'qwen2.5:32b', 'name': 'Qwen 2.5 32B', 'context': 32768},
                    {'id': 'llama3.2:latest', 'name': 'Llama 3.2', 'context': 131072},
                    {'id': 'gemma3:12b', 'name': 'Gemma 3 12B', 'context': 8192},
                    {'id': 'deepseek-r1:8b', 'name': 'DeepSeek R1 8B', 'context': 131072},
                ]
            },
            {
                'id': 'openai',
                'name': 'OpenAI',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'gpt-4o', 'name': 'GPT-4o', 'context': 128000},
                    {'id': 'gpt-4o-mini', 'name': 'GPT-4o Mini', 'context': 128000},
                    {'id': 'gpt-4.1', 'name': 'GPT-4.1', 'context': 1000000},
                    {'id': 'o4-mini', 'name': 'o4 Mini', 'context': 200000},
                    {'id': 'o3', 'name': 'o3', 'context': 200000},
                ]
            },
            {
                'id': 'anthropic',
                'name': 'Anthropic Claude',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'claude-sonnet-4-20250514', 'name': 'Claude Sonnet 4', 'context': 200000},
                    {'id': 'claude-haiku-3-5-20250514', 'name': 'Claude Haiku 3.5', 'context': 200000},
                    {'id': 'claude-opus-4-20250514', 'name': 'Claude Opus 4', 'context': 200000},
                ]
            },
            {
                'id': 'google',
                'name': 'Google Gemini',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'gemini-2.5-flash', 'name': 'Gemini 2.5 Flash', 'context': 1048576},
                    {'id': 'gemini-2.5-pro', 'name': 'Gemini 2.5 Pro', 'context': 1048576},
                ]
            },
            {
                'id': 'deepseek',
                'name': 'DeepSeek',
                'needs_base_url': False,
                'default_base_url': 'https://api.deepseek.com/v1',
                'models': [
                    {'id': 'deepseek-chat', 'name': 'DeepSeek V3 (Chat)', 'context': 65536},
                    {'id': 'deepseek-reasoner', 'name': 'DeepSeek R1 (Reasoner)', 'context': 65536},
                ]
            },
            {
                'id': 'groq',
                'name': 'Groq',
                'needs_base_url': False,
                'default_base_url': 'https://api.groq.com/openai/v1',
                'models': [
                    {'id': 'llama-3.3-70b-versatile', 'name': 'Llama 3.3 70B', 'context': 128000},
                    {'id': 'mixtral-8x7b-32768', 'name': 'Mixtral 8x7B', 'context': 32768},
                    {'id': 'deepseek-r1-distill-llama-70b', 'name': 'DeepSeek R1 Distill 70B', 'context': 128000},
                ]
            },
            {
                'id': 'openrouter',
                'name': 'OpenRouter',
                'needs_base_url': False,
                'default_base_url': 'https://openrouter.ai/api/v1',
                'models': [
                    {'id': 'openai/gpt-4o', 'name': 'OpenAI GPT-4o', 'context': 128000},
                    {'id': 'anthropic/claude-sonnet-4', 'name': 'Claude Sonnet 4', 'context': 200000},
                    {'id': 'google/gemini-2.5-pro', 'name': 'Gemini 2.5 Pro', 'context': 1048576},
                    {'id': 'deepseek/deepseek-chat', 'name': 'DeepSeek V3', 'context': 65536},
                ]
            },
            {
                'id': 'xai',
                'name': 'xAI (Grok)',
                'needs_base_url': False,
                'default_base_url': 'https://api.x.ai/v1',
                'models': [
                    {'id': 'grok-3-beta', 'name': 'Grok 3 Beta', 'context': 131072},
                    {'id': 'grok-3-mini-beta', 'name': 'Grok 3 Mini Beta', 'context': 131072},
                ]
            },
            {
                'id': 'mistral',
                'name': 'Mistral AI',
                'needs_base_url': False,
                'default_base_url': 'https://api.mistral.ai/v1',
                'models': [
                    {'id': 'mistral-large-latest', 'name': 'Mistral Large', 'context': 128000},
                    {'id': 'mistral-small-latest', 'name': 'Mistral Small', 'context': 32000},
                    {'id': 'codestral-latest', 'name': 'Codestral', 'context': 256000},
                ]
            },
            {
                'id': 'together',
                'name': 'Together AI',
                'needs_base_url': False,
                'default_base_url': 'https://api.together.xyz/v1',
                'models': [
                    {'id': 'meta-llama/Llama-4-Maverick-17B-128E-Instruct', 'name': 'Llama 4 Maverick 17B', 'context': 131072},
                    {'id': 'deepseek-ai/DeepSeek-V3', 'name': 'DeepSeek V3', 'context': 65536},
                ]
            },
            {
                'id': 'glm',
                'name': 'Z.AI / GLM',
                'needs_base_url': False,
                'default_base_url': 'https://open.bigmodel.cn/api/paas/v4',
                'models': [
                    {'id': 'glm-4-plus', 'name': 'GLM-4 Plus', 'context': 128000},
                    {'id': 'glm-4-flash', 'name': 'GLM-4 Flash', 'context': 128000},
                ]
            },
            {
                'id': 'minimax',
                'name': 'MiniMax',
                'needs_base_url': False,
                'default_base_url': 'https://api.minimax.chat/v1',
                'models': [
                    {'id': 'abab7', 'name': 'ABAB7', 'context': 256000},
                    {'id': 'MiniMax-M1', 'name': 'MiniMax M1', 'context': 256000},
                ]
            },
            {
                'id': 'kimi',
                'name': 'Kimi (Moonshot)',
                'needs_base_url': False,
                'default_base_url': 'https://api.moonshot.cn/v1',
                'models': [
                    {'id': 'moonshot-v1-8k', 'name': 'Moonshot v1 8K', 'context': 8192},
                    {'id': 'moonshot-v1-32k', 'name': 'Moonshot v1 32K', 'context': 32768},
                ]
            },
            {
                'id': 'dashscope',
                'name': 'Alibaba DashScope',
                'needs_base_url': False,
                'default_base_url': 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1',
                'models': [
                    {'id': 'qwen-max', 'name': 'Qwen Max', 'context': 32768},
                    {'id': 'qwen-plus', 'name': 'Qwen Plus', 'context': 131072},
                    {'id': 'qwen-turbo', 'name': 'Qwen Turbo', 'context': 131072},
                ]
            },
            {
                'id': 'huggingface',
                'name': 'HuggingFace TGI',
                'needs_base_url': False,
                'default_base_url': 'https://api-inference.huggingface.co/v1',
                'models': [
                    {'id': 'namespace/model-name', 'name': 'User-provided model (namespace/model-name)', 'context': None},
                ]
            },
            {
                'id': 'bedrock',
                'name': 'Amazon Bedrock',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [],
                'note': 'Coming soon — Bedrock uses IAM auth, not API keys. Use LiteLLM/OpenRouter proxy for now.'
            },
            {
                'id': 'vercel',
                'name': 'Vercel AI Gateway',
                'needs_base_url': True,
                'default_base_url': None,
                'models': [],
                'note': 'User provides model via gateway config'
            },
        ],
        'embedding_providers': [
            {
                'id': 'ollama',
                'name': 'Ollama (Local)',
                'needs_base_url': True,
                'default_base_url': 'http://localhost:11434',
                'models': [
                    {'id': 'nomic-embed-text', 'name': 'Nomic Embed Text (768d)', 'dimensions': 768},
                    {'id': 'bge-m3', 'name': 'BGE-M3 Multilingual (1024d)', 'dimensions': 1024},
                    {'id': 'mxbai-embed-large', 'name': 'MXBAI Embed Large (1024d)', 'dimensions': 1024},
                ]
            },
            {
                'id': 'openai',
                'name': 'OpenAI',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'text-embedding-3-small', 'name': 'Embedding 3 Small (1536d)', 'dimensions': 1536},
                    {'id': 'text-embedding-3-large', 'name': 'Embedding 3 Large (3072d)', 'dimensions': 3072},
                ]
            },
            {
                'id': 'google',
                'name': 'Google',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'text-embedding-004', 'name': 'Text Embedding 004 (768d)', 'dimensions': 768},
                ]
            },
            {
                'id': 'cohere',
                'name': 'Cohere',
                'needs_base_url': False,
                'default_base_url': None,
                'models': [
                    {'id': 'embed-english-v3.0', 'name': 'Embed English v3 (1024d)', 'dimensions': 1024},
                    {'id': 'embed-multilingual-v3.0', 'name': 'Embed Multilingual v3 (1024d)', 'dimensions': 1024},
                ]
            },
        ],
        'graph_db_modes': [
            {'id': 'local', 'name': 'Local Neo4j (Docker)', 'description': 'Neo4j Community running in Docker on this machine'},
            {'id': 'cloud', 'name': 'Neo4j AuraDB (Cloud)', 'description': 'Managed Neo4j cloud — enter your AuraDB connection URI'},
        ],
        'languages': [
            {'id': 'en', 'name': 'English', 'native': 'English'},
            {'id': 'zh-CN', 'name': 'Chinese (Simplified)', 'native': '简体中文'},
            {'id': 'hi', 'name': 'Hindi', 'native': 'हिन्दी'},
            {'id': 'es', 'name': 'Spanish', 'native': 'Español'},
            {'id': 'fr', 'name': 'French', 'native': 'Français'},
            {'id': 'ar', 'name': 'Arabic', 'native': 'العربية'},
            {'id': 'bn', 'name': 'Bengali', 'native': 'বাংলা'},
            {'id': 'pt', 'name': 'Portuguese', 'native': 'Português'},
            {'id': 'ru', 'name': 'Russian', 'native': 'Русский'},
            {'id': 'ur', 'name': 'Urdu', 'native': 'اردو'},
            {'id': 'th', 'name': 'Thai', 'native': 'ไทย'},
        ],
    })


@settings_bp.route('/readiness', methods=['POST'])
def check_readiness():
    """Validate setup readiness without making live provider/network calls."""
    data = request.get_json(silent=True) or {}
    return jsonify({'success': True, 'data': _readiness_payload(data)})


@settings_bp.route('/test-llm', methods=['POST'])
def test_llm_connection():
    """Test LLM provider connection with a simple ping message."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No provider config provided'}), 400

    try:
        # Build a temporary provider to test
        provider_type = ProviderType(data.get('provider', 'openai'))
        model = data.get('model', 'gpt-4o-mini')
        api_key = data.get('api_key', '')
        base_url = data.get('base_url')

        if provider_type == ProviderType.OPENAI or provider_type == ProviderType.DEEPSEEK or \
           provider_type == ProviderType.GROQ or provider_type == ProviderType.OPENROUTER or \
           provider_type == ProviderType.XAI or provider_type == ProviderType.MISTRAL or \
           provider_type == ProviderType.TOGETHER or provider_type == ProviderType.GLM or \
           provider_type == ProviderType.MINIMAX or provider_type == ProviderType.KIMI or \
           provider_type == ProviderType.DASHSCOPE or provider_type == ProviderType.HUGGINGFACE or \
           provider_type == ProviderType.VERCEL:
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url=base_url or 'https://api.openai.com/v1',
                timeout=15,
            )
            response = client.chat.completions.create(
                model=model,
                messages=[{'role': 'user', 'content': 'Reply with just "OK"'}],
                max_tokens=5,
            )
            return jsonify({
                'success': True,
                'message': f'Connected! Model: {model}',
                'response': response.choices[0].message.content.strip(),
            })

        elif provider_type == ProviderType.ANTHROPIC:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key, timeout=15)
            response = client.messages.create(
                model=model,
                max_tokens=5,
                messages=[{'role': 'user', 'content': 'Reply with just "OK"'}],
            )
            return jsonify({
                'success': True,
                'message': f'Connected! Model: {model}',
                'response': response.content[0].text.strip(),
            })

        elif provider_type == ProviderType.GOOGLE:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model,
                contents='Reply with just "OK"',
            )
            return jsonify({
                'success': True,
                'message': f'Connected! Model: {model}',
                'response': response.text.strip(),
            })

        elif provider_type == ProviderType.OLLAMA:
            from openai import OpenAI
            client = OpenAI(
                api_key='ollama',
                base_url=base_url or 'http://localhost:11434/v1',
                timeout=15,
            )
            response = client.chat.completions.create(
                model=model,
                messages=[{'role': 'user', 'content': 'Reply with just "OK"'}],
                max_tokens=5,
            )
            return jsonify({
                'success': True,
                'message': f'Connected! Model: {model}',
                'response': response.choices[0].message.content.strip(),
            })

        else:
            return jsonify({'success': False, 'error': f'Provider {provider_type} not supported yet'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': f'Connection failed: {_sanitize_error(e)}'}), 400
