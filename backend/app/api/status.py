"""System status API for operator confidence checks."""

import os
import shutil
from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify

from ..config import Config


status_bp = Blueprint("status", __name__)


def _check_path(path: str) -> dict:
    exists = os.path.exists(path)
    try:
        usage = shutil.disk_usage(path if exists else os.path.dirname(path) or ".")
        free_gb = round(usage.free / (1024 ** 3), 2)
    except OSError:
        free_gb = None
    return {"exists": exists, "free_gb": free_gb}


@status_bp.route("", methods=["GET"])
def get_status():
    neo4j_storage = current_app.extensions.get("neo4j_storage")
    neo4j_ok = False
    if neo4j_storage is not None:
        try:
            neo4j_ok = bool(neo4j_storage.health_check())
        except Exception:
            neo4j_ok = False

    llm_provider = getattr(Config, "LLM_PROVIDER", None) or os.environ.get("LLM_PROVIDER", "ollama")
    embedding_provider = getattr(Config, "EMBEDDING_PROVIDER", None) or os.environ.get("EMBEDDING_PROVIDER", "ollama")
    upload_folder = getattr(Config, "UPLOAD_FOLDER", "uploads")

    services = [
        {
            "key": "api",
            "label": "Backend API",
            "status": "ok",
            "detail": "Flask app is responding",
        },
        {
            "key": "neo4j",
            "label": "Neo4j",
            "status": "ok" if neo4j_ok else "warning",
            "detail": "Connected" if neo4j_ok else "Not connected or unavailable",
        },
        {
            "key": "llm",
            "label": "LLM Provider",
            "status": "configured" if llm_provider else "warning",
            "detail": llm_provider or "Not configured",
        },
        {
            "key": "embedding",
            "label": "Embedding Provider",
            "status": "configured" if embedding_provider else "warning",
            "detail": embedding_provider or "Not configured",
        },
        {
            "key": "storage",
            "label": "Storage",
            "status": "ok" if _check_path(upload_folder)["exists"] else "warning",
            "detail": upload_folder,
            "meta": _check_path(upload_folder),
        },
    ]

    return jsonify({
        "success": True,
        "data": {
            "status": "ok" if all(item["status"] in ("ok", "configured") for item in services) else "degraded",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "services": services,
            "estimate": {
                "cost_per_100_personas_usd": 0 if llm_provider == "ollama" else 1.2,
                "default_model": getattr(Config, "LLM_MODEL_NAME", None) or os.environ.get("LLM_MODEL_NAME", "not set"),
            },
        },
    })

