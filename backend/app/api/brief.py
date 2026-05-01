"""Brief quality API — deterministic pre-simulation trust checks."""

from flask import Blueprint, jsonify, request

from ..services.brief_quality import BriefQualityService
from ..utils.logger import get_logger


logger = get_logger("mirofish.api.brief")
brief_bp = Blueprint("brief", __name__)


@brief_bp.route("/quality", methods=["POST"])
def score_brief_quality():
    data = request.get_json(silent=True) or {}
    brief = data.get("brief") or data.get("campaign") or data

    try:
        result = BriefQualityService().score(brief)
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        logger.error("Brief quality scoring failed: %s", exc)
        return jsonify({"success": False, "error": "Brief quality scoring failed"}), 500
