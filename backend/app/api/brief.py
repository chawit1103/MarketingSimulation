"""Brief quality API — deterministic pre-simulation trust checks."""

from flask import Blueprint, jsonify, request

from ..services.brief_quality import BriefQualityService
from ..services.revised_brief import RevisedBriefService
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


@brief_bp.route("/revise", methods=["POST"])
def revise_brief_from_action_plan():
    data = request.get_json(silent=True) or {}

    try:
        result = RevisedBriefService().generate(
            campaign=data.get("campaign") or {},
            original_brief=data.get("original_brief") or data.get("brief") or {},
            action_plan=data.get("action_plan") or {},
            evidence=data.get("evidence") or {},
            source=data.get("source") or {},
        )
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        logger.error("Revised brief generation failed: %s", exc)
        return jsonify({"success": False, "error": "Revised brief generation failed"}), 500
