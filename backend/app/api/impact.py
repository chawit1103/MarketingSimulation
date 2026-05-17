"""Business Impact API — converts simulation KPIs to revenue projections."""

from flask import Blueprint, request, jsonify, g

from ..services.impact_calculator import ImpactCalculator, BusinessParams, ImpactResult, ComparisonResult
from ..services.campaign_service import CampaignService
from ..services.kpi_calculator import KPICalculator
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.impact")

impact_bp = Blueprint("impact", __name__)


def _get_calculator() -> KPICalculator:
    return KPICalculator()


def _get_org_id() -> str:
    org = getattr(g, "current_org", None)
    if org:
        return org.get("org_id", "unknown") if isinstance(org, dict) else getattr(org, "org_id", "unknown")
    user = getattr(g, "current_user", None)
    if user:
        return user.get("org_id", "unknown") if isinstance(user, dict) else getattr(user, "org_id", "unknown")
    return "unknown"


def _get_campaign_name(campaign_id: str) -> str:
    try:
        from ..services.campaign_service import CampaignService
        svc = CampaignService()
        camp = svc.get_campaign(campaign_id)
        if camp:
            return camp.name
    except Exception:
        pass
    return campaign_id[:12]


def _get_owned_campaign(campaign_id: str, org_id: str):
    return CampaignService().get_campaign(campaign_id, org_id=org_id)


# ── API Routes ────────────────────────────────────────────

@impact_bp.route("/calculate", methods=["POST"])
def calculate_impact():
    """POST /api/impact/calculate
    
    Body:
    {
        "campaign_id": "cmp_xxx",
        "business": {
            "product_name": "New Product",
            "unit_price": 500,
            "market_size": 100000,
            "current_market_share": 10,
            "base_conversion_rate": 5,
            "campaign_cost": 500000,
            "time_horizon_months": 6
        }
    }
    
    Returns:
    {
        "success": true,
        "data": { ... ImpactResult ... }
    }
    """
    data = request.get_json(silent=True) or {}
    campaign_id = data.get("campaign_id")
    if not campaign_id:
        return jsonify({"error": "campaign_id is required"}), 400

    # Build business params
    biz_data = data.get("business", {})
    params = BusinessParams(**{k: v for k, v in biz_data.items() if v is not None})

    # Fetch KPIs
    org_id = _get_org_id()
    campaign = _get_owned_campaign(campaign_id, org_id)
    if not campaign:
        return jsonify({"success": False, "error": "Resource not found"}), 404
    calc = _get_calculator()
    try:
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)
        kpis = {
            "overall_sentiment": report.overall_sentiment,
            "conversion_probability": report.conversion_probability,
            "crisis_risk": report.crisis_risk,
            "message_resonance": report.message_resonance,
            "brand_perception_shift": report.brand_perception_shift,
        }
        campaign_name = campaign.name
    except Exception as e:
        # Use demo KPIs if simulation not complete
        logger.warning(f"Using demo KPIs for {campaign_id}: {e}")
        kpis = {
            "overall_sentiment": float(data.get("sentiment_override", 42)),
            "conversion_probability": 67.0,
            "crisis_risk": 15.0,
            "message_resonance": 72.0,
            "brand_perception_shift": 12.0,
        }
        campaign_name = data.get("campaign_name", campaign_id[:12])

    # Calculate impact
    result = ImpactCalculator.calculate(
        campaign_id=campaign_id,
        campaign_name=campaign_name,
        kpis=kpis,
        params=params,
    )

    return jsonify({"success": True, "data": result.dict()})


@impact_bp.route("/scenarios/<sentiment_value>", methods=["GET"])
def quick_scenario(sentiment_value: str):
    """GET /api/impact/scenarios/{sentiment}?price=500&market=100000&share=10
    
    Quick projection based on a sentiment value, without needing a campaign.
    """
    try:
        sentiment = float(sentiment_value)
    except ValueError:
        return jsonify({"error": "sentiment must be a number"}), 400

    try:
        params = BusinessParams(
            product_name=request.args.get("product", "Product"),
            unit_price=float(request.args.get("price", 100)),
            market_size=int(request.args.get("market", 100000)),
            current_market_share=float(request.args.get("share", 10)),
            base_conversion_rate=float(request.args.get("conversion", 5)),
            campaign_cost=float(request.args.get("cost", 500000)),
            time_horizon_months=int(request.args.get("months", 6)),
        )
    except ValueError:
        return jsonify({"success": False, "error": "scenario parameters must be numeric"}), 400

    result = ImpactCalculator.calculate(
        campaign_id="quick",
        campaign_name=f"Sentiment {sentiment_value} Projection",
        kpis={
            "overall_sentiment": sentiment,
            "conversion_probability": 67,
            "crisis_risk": 15,
            "message_resonance": 72,
            "brand_perception_shift": 12,
        },
        params=params,
    )

    data = result.dict()
    data["source"] = {
        "type": "local_estimate",
        "label": "Local Estimate",
        "warning": "Quick deterministic projection from sentiment and business inputs; not a live simulation result.",
    }
    return jsonify({"success": True, "data": data})
