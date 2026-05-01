"""Competitor Simulation API — multi-brand war gaming."""

from flask import Blueprint, request, jsonify
from ..services.competitor_engine import (
    CompetitorSimEngine, BrandProfile, SimulationEvent,
    PRICE_WAR_SCENARIO, FIRST_MOVER_SCENARIO, SCANDAL_SCENARIO,
)
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.competitor")

competitor_bp = Blueprint("competitor", __name__)


@competitor_bp.route("/scenarios", methods=["GET"])
def list_scenarios():
    """GET /api/competitor/scenarios — pre-built simulation scenarios."""
    return jsonify({
        "success": True,
        "scenarios": [
            {"id": "price_war", "name": "Price War — สงครามราคา", "brands": 4, "events": 1, **{k: v for k, v in PRICE_WAR_SCENARIO.items() if k != "brands" and k != "events"}},
            {"id": "first_mover", "name": "First Mover Advantage", "brands": 4, "events": 2, **{k: v for k, v in FIRST_MOVER_SCENARIO.items() if k != "brands" and k != "events"}},
            {"id": "scandal", "name": "Crisis — Scandal คู่แข่ง", "brands": 4, "events": 1, **{k: v for k, v in SCANDAL_SCENARIO.items() if k != "brands" and k != "events"}},
        ],
    })


@competitor_bp.route("/simulate", methods=["POST"])
def run_simulation():
    """POST /api/competitor/simulate
    
    Body: { "scenario": "price_war" | { "brands": [...], "events": [...], "rounds": 12 } }
    
    Returns full simulation timeline + market share shifts.
    """
    data = request.get_json(silent=True) or {}

    # Option 1: Use pre-built scenario
    scenario_id = data.get("scenario", "")
    if scenario_id == "price_war":
        scenario = PRICE_WAR_SCENARIO
    elif scenario_id == "first_mover":
        scenario = FIRST_MOVER_SCENARIO
    elif scenario_id == "scandal":
        scenario = SCANDAL_SCENARIO
    else:
        scenario = None

    if scenario:
        brands = [BrandProfile(**b) for b in scenario["brands"]]
        events = [SimulationEvent(**e) for e in scenario.get("events", [])]
        rounds = data.get("rounds", 12)
        name = scenario["name"]
    else:
        # Custom simulation
        brands_data = data.get("brands", [])
        events_data = data.get("events", [])
        brands = [BrandProfile(**b) for b in brands_data] if brands_data else [
            BrandProfile(name="Our Brand", base_sentiment=40, price_position=50, brand_strength=60, market_share=35),
            BrandProfile(name="Competitor A", base_sentiment=35, price_position=55, brand_strength=70, market_share=35),
            BrandProfile(name="Competitor B", base_sentiment=20, price_position=25, brand_strength=40, market_share=30),
        ]
        events = [SimulationEvent(**e) for e in events_data]
        rounds = data.get("rounds", 12)
        name = data.get("scenario_name", "Custom Scenario")

    if len(brands) < 2:
        return jsonify({"error": "Need at least 2 brands"}), 400

    try:
        result = CompetitorSimEngine.simulate(
            brands=brands,
            events=events,
            rounds=rounds,
            scenario_name=name,
        )
        return jsonify({"success": True, "data": result.dict()})
    except Exception as e:
        logger.error(f"Competitor simulation failed: {e}")
        return jsonify({"error": str(e)}), 500
