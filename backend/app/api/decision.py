"""Decision API — deterministic strategy recommendations and what-if analysis."""

from flask import Blueprint, jsonify, request

from ..services.budget_scenario_planner import BudgetScenarioPlanner
from ..services.decision_engine import DecisionEngine
from ..utils.logger import get_logger


logger = get_logger("mirofish.api.decision")
decision_bp = Blueprint("decision", __name__)


def _engine() -> DecisionEngine:
    return DecisionEngine()


@decision_bp.route("/analyze", methods=["POST"])
def analyze_decision():
    data = request.get_json(silent=True) or {}
    try:
        result = _engine().analyze(
            campaign=data.get("campaign") or {},
            kpis=data.get("kpis") or {},
            segments=data.get("segments") or [],
            evidence=data.get("evidence") or {},
            business_params=data.get("business_params") or {},
        )
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        logger.error("Decision analysis failed: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


@decision_bp.route("/what-if", methods=["POST"])
def what_if():
    data = request.get_json(silent=True) or {}
    try:
        result = _engine().simulate_what_if(
            kpis=data.get("kpis") or {},
            scenario=data.get("scenario") or {},
            business_params=data.get("business_params") or {},
        )
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        logger.error("What-if simulation failed: %s", exc)
        return jsonify({"success": False, "error": "What-if simulation failed"}), 500


@decision_bp.route("/budget-scenario", methods=["POST"])
def budget_scenario():
    """Create a deterministic budget/channel planning scenario."""
    data = request.get_json(silent=True) or {}
    try:
        result = BudgetScenarioPlanner().plan(data.get("inputs") or data)
        return jsonify({"success": True, "data": result})
    except Exception as exc:
        logger.error("Budget scenario planning failed: %s", exc)
        return jsonify({"success": False, "error": "Budget scenario planning failed"}), 500
