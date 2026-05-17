"""Competitor Simulation API — multi-brand war gaming."""

from flask import Blueprint, request, jsonify
from ..services.competitor_engine import (
    CompetitorSimEngine, BrandProfile, SimulationEvent,
    SCENARIO_LIBRARY,
)
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.competitor")

competitor_bp = Blueprint("competitor", __name__)


@competitor_bp.route("/scenarios", methods=["GET"])
def list_scenarios():
    """GET /api/competitor/scenarios — pre-built simulation scenarios."""
    scenarios = []
    seen = set()
    for scenario_id, scenario in SCENARIO_LIBRARY.items():
        # Keep backward-compatible aliases available for simulate, but only list
        # the canonical templates in the UI catalogue.
        if id(scenario) in seen or scenario_id in {"creator_backlash", "rumor_amplification"}:
            continue
        seen.add(id(scenario))
        scenarios.append({
            "id": scenario_id,
            "name": scenario.get("name", scenario_id),
            "description": scenario.get("description", ""),
            "brands": len(scenario.get("brands", [])),
            "events": len(scenario.get("events", [])),
            "affected_segments": scenario.get("metadata", {}).get("affected_segments", []),
            "amplification_channels": scenario.get("metadata", {}).get("amplification_channels", []),
        })

    return jsonify({
        "success": True,
        "scenarios": scenarios,
    })


@competitor_bp.route("/simulate", methods=["POST"])
def run_simulation():
    """POST /api/competitor/simulate
    
    Body: { "scenario": "price_war" | { "brands": [...], "events": [...], "rounds": 12 } }
    
    Returns full simulation timeline + market share shifts.
    """
    data = request.get_json(silent=True) or {}

    try:
        brands, events, rounds, name, metadata = _simulation_inputs(data)
        if len(brands) < 2:
            return jsonify({"success": False, "error": "Need at least 2 brands"}), 400

        result = CompetitorSimEngine.simulate(
            brands=brands,
            events=events,
            rounds=rounds,
            scenario_name=name,
            scenario_metadata=metadata,
        )
        return jsonify({"success": True, "data": _dump_model(result)})
    except Exception as e:
        logger.exception("Competitor simulation failed: %s", e)
        return jsonify({"success": False, "error": "Competitor simulation failed"}), 500


def _simulation_inputs(data):
    scenario_id = data.get("scenario", "")
    scenario = SCENARIO_LIBRARY.get(scenario_id)

    if scenario:
        brands_data = _rename_our_brand(scenario["brands"], _campaign_name(data))
        brands = [BrandProfile(**b) for b in brands_data]
        events_data = _rename_event_targets(scenario.get("events", []), _campaign_name(data))
        events = [SimulationEvent(**e) for e in events_data]
        return brands, events, _bounded_rounds(data.get("rounds", 12)), scenario["name"], scenario.get("metadata", {})

    brands_data = data.get("brands", [])
    events_data = data.get("events", [])
    brands = [BrandProfile(**b) for b in brands_data] if brands_data else [
        BrandProfile(name="Our Brand", base_sentiment=40, price_position=50, brand_strength=60, market_share=35),
        BrandProfile(name="Competitor A", base_sentiment=35, price_position=55, brand_strength=70, market_share=35),
        BrandProfile(name="Competitor B", base_sentiment=20, price_position=25, brand_strength=40, market_share=30),
    ]
    events = [SimulationEvent(**e) for e in events_data]
    metadata = {
        "affected_segments": data.get("affected_segments", []),
        "amplification_channels": data.get("amplification_channels", []),
        "key_drivers": data.get("key_drivers", []),
        "recommended_response": data.get("recommended_response", ""),
        "response_playbook": data.get("response_playbook", []),
    }
    return brands, events, _bounded_rounds(data.get("rounds", 12)), data.get("scenario_name", "Custom Scenario"), metadata


def _dump_model(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _bounded_rounds(raw_rounds) -> int:
    try:
        rounds = int(raw_rounds)
    except (TypeError, ValueError):
        rounds = 12
    return max(3, min(rounds, 20))


def _campaign_name(data) -> str:
    campaign = data.get("campaign") if isinstance(data.get("campaign"), dict) else {}
    return (
        data.get("campaign_name")
        or campaign.get("name")
        or campaign.get("campaign_name")
        or "Our Brand"
    )


def _rename_our_brand(brands, campaign_name: str):
    return [
        {**brand, "name": campaign_name if brand.get("name") == "Our Brand" else brand.get("name")}
        for brand in brands
    ]


def _rename_event_targets(events, campaign_name: str):
    return [
        {**event, "target_brand": campaign_name if event.get("target_brand") == "Our Brand" else event.get("target_brand")}
        for event in events
    ]
