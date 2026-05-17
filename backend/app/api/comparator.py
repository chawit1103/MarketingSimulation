"""Campaign Comparator API.

Compares 2-5 campaign directions and keeps provenance explicit. Demo fixtures
are labeled as demo data, local deterministic estimates are labeled as local
estimates, and backend-verified is reserved for persisted real simulation KPI
records.
"""

from flask import Blueprint, request, jsonify, g

from ..models.report import ExecutiveReport
from ..services.campaign_service import CampaignService
from ..services.kpi_calculator import KPICalculator
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.comparator")

comparator_bp = Blueprint("comparator", __name__)


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


COMPARISON_METRICS = [
    {"key": "overall_sentiment", "label": "Overall Sentiment", "unit": "", "higher_is_better": True},
    {"key": "conversion_probability", "label": "Conversion Probability", "unit": "%", "higher_is_better": True},
    {"key": "social_influence_index", "label": "Social Influence", "unit": "", "higher_is_better": True},
    {"key": "message_resonance", "label": "Message Resonance", "unit": "%", "higher_is_better": True},
    {"key": "crisis_risk", "label": "Crisis Risk", "unit": "%", "higher_is_better": False},
    {"key": "brand_perception_shift", "label": "Brand Perception Shift", "unit": "", "higher_is_better": True},
    {"key": "opinion_polarization", "label": "Opinion Polarization", "unit": "", "higher_is_better": False},
]


COMPARATOR_DEMO_VARIANTS = [
    {
        "campaign_id": "cmp_demo_emotional_story",
        "campaign_name": "Variant A: Emotional Storytelling",
        "direction": "emotional_storytelling",
        "overall_sentiment": 46,
        "conversion_probability": 57,
        "social_influence_index": 73,
        "message_resonance": 76,
        "crisis_risk": 34,
        "brand_perception_shift": 18,
        "opinion_polarization": 44,
        "segment_strengths": ["Urban lifestyle buyers", "Brand loyalists"],
        "segment_weaknesses": ["Proof-seeking skeptics", "Price-sensitive families"],
        "trade_offs": ["High memorability, but weaker factual proof for skeptical buyers."],
        "recommended_use_case": "Use for awareness, brand warmth, and upper-funnel creative testing.",
    },
    {
        "campaign_id": "cmp_demo_proof_trust",
        "campaign_name": "Variant B: Proof-Led Trust",
        "direction": "proof_led_trust",
        "overall_sentiment": 38,
        "conversion_probability": 69,
        "social_influence_index": 66,
        "message_resonance": 71,
        "crisis_risk": 18,
        "brand_perception_shift": 23,
        "opinion_polarization": 28,
        "segment_strengths": ["Health-conscious professionals", "Risk-aware parents"],
        "segment_weaknesses": ["Impulse buyers who prefer simpler emotional hooks"],
        "trade_offs": ["Lower excitement than emotional creative, but stronger trust and lower crisis exposure."],
        "recommended_use_case": "Use for launch approval, regulated claims, premium pricing, and trust repair.",
    },
    {
        "campaign_id": "cmp_demo_price_promo",
        "campaign_name": "Variant C: Price / Promotion",
        "direction": "price_promotion",
        "overall_sentiment": 25,
        "conversion_probability": 74,
        "social_influence_index": 58,
        "message_resonance": 63,
        "crisis_risk": 41,
        "brand_perception_shift": 6,
        "opinion_polarization": 52,
        "segment_strengths": ["Value hunters", "Trial-oriented shoppers"],
        "segment_weaknesses": ["Premium-brand buyers", "Long-term loyalty segment"],
        "trade_offs": ["Strong short-term conversion estimate, but higher brand dilution and polarization risk."],
        "recommended_use_case": "Use for limited-time trials or tactical retailer pushes, not as the main brand idea.",
    },
]


def _source(
    *,
    source_mode: str,
    data_basis: str,
    campaign_id: str | None = None,
    run_id: str | None = None,
    simulation_id: str | None = None,
    warning: str = "",
    limitations: list | None = None,
) -> dict:
    allowed = {"demo_mode", "local_estimate", "live_backend", "backend_verified", "unknown"}
    mode = source_mode if source_mode in allowed else "unknown"
    return {
        "type": mode,
        "source_mode": mode,
        "data_basis": data_basis or "unknown",
        "campaign_id": campaign_id,
        "run_id": run_id,
        "simulation_id": simulation_id,
        "warning": warning,
        "limitations": limitations or [],
    }


def _demo_variant_payload(row: dict) -> dict:
    payload = row.copy()
    payload["source"] = _source(
        source_mode="demo_mode",
        data_basis="demo_fixture",
        campaign_id=row["campaign_id"],
        warning="Synthetic comparator demo fixture; not a live simulation or real A/B test result.",
        limitations=[
            "Demo variants are deterministic product fixtures.",
            "Validate with real simulation output or controlled audience testing before launch decisions.",
        ],
    )
    payload["source_mode"] = "demo_mode"
    payload["data_basis"] = "demo_fixture"
    return payload


def _source_from_kpi(kpi: dict) -> dict:
    source_data = kpi.get("source") or {}
    return _source(
        source_mode=source_data.get("source_mode") or source_data.get("type") or kpi.get("source_mode", "unknown"),
        data_basis=source_data.get("data_basis") or kpi.get("data_basis", "unknown"),
        campaign_id=kpi.get("campaign_id"),
        run_id=source_data.get("run_id") or kpi.get("run_id"),
        simulation_id=source_data.get("simulation_id") or kpi.get("simulation_id"),
        warning=source_data.get("warning", ""),
        limitations=source_data.get("limitations") or kpi.get("limitations") or [],
    )


def _comparison_source(valid: list) -> dict:
    sources = [_source_from_kpi(k) for k in valid]
    modes = {source["source_mode"] for source in sources}
    bases = {source["data_basis"] for source in sources}

    if modes == {"demo_mode"}:
        return _source(
            source_mode="demo_mode",
            data_basis="demo_fixture",
            warning="Comparison uses deterministic demo fixtures only.",
            limitations=["Demo comparison is for product walkthroughs, not live market evidence."],
        )
    if modes == {"backend_verified"} and bases == {"real_simulation"}:
        return _source(
            source_mode="backend_verified",
            data_basis="real_simulation",
            warning="Comparison uses persisted backend-verified simulation KPI output.",
        )
    if "local_estimate" in modes or "demo_mode" in modes:
        return _source(
            source_mode="local_estimate",
            data_basis="local_estimate",
            warning="One or more variants use deterministic local estimate data; do not treat this as backend-verified evidence.",
            limitations=["Run or attach real simulation KPI records before final approval."],
        )
    if "live_backend" in modes:
        return _source(
            source_mode="live_backend",
            data_basis="backend_generated",
            warning="Comparison was generated by the backend, but evidence basis varies by variant.",
        )
    return _source(
        source_mode="unknown",
        data_basis="unknown",
        warning="Comparison source metadata is incomplete.",
    )


def _risk_level(value) -> str:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 35.0
    if score >= 70:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def _campaign_name_for_row(row: dict, org_id: str) -> str:
    if row.get("campaign_name"):
        return row["campaign_name"]
    return _get_campaign_name_for_org(row["campaign_id"], org_id)


def _rank_score(row: dict, win_counts: dict) -> float:
    return (
        (win_counts.get(row["campaign_id"], 0) * 12)
        + (float(row.get("conversion_probability", 0)) * 0.28)
        + (float(row.get("message_resonance", 0)) * 0.20)
        + (float(row.get("overall_sentiment", 0)) * 0.16)
        + (float(row.get("social_influence_index", 0)) * 0.12)
        - (float(row.get("crisis_risk", 0)) * 0.18)
        - (float(row.get("opinion_polarization", 0)) * 0.08)
    )


def _fetch_kpi(campaign_id: str, org_id: str) -> dict:
    """Fetch KPI data for one campaign. Returns dict or error dict."""
    try:
        campaign = CampaignService().get_campaign(campaign_id, org_id=org_id)
        if campaign is None:
            return {"campaign_id": campaign_id, "error": "Resource not found"}

        report = None
        if isinstance(campaign.results_summary, dict):
            try:
                report = ExecutiveReport.from_dict(campaign.results_summary)
            except Exception:
                logger.warning("Ignoring malformed comparison report for campaign %s", campaign_id)
        if report is None:
            report = _get_calculator().calculate(
                campaign_id=campaign_id,
                org_id=org_id,
                simulation_id=campaign.simulation_id,
            )

        source_data = _source(
            source_mode=report.source_mode or "unknown",
            data_basis=report.data_basis or "unknown",
            campaign_id=campaign_id,
            run_id=report.run_id,
            simulation_id=report.simulation_id or campaign.simulation_id,
            warning=(
                "Local deterministic estimate because no persisted real simulation KPI output is available."
                if report.source_mode == "local_estimate"
                else "Backend-verified persisted simulation KPI output."
                if report.source_mode == "backend_verified" and report.data_basis == "real_simulation"
                else ""
            ),
            limitations=report.limitations,
        )
        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign.name,
            "report_id": report.report_id,
            "run_id": report.run_id,
            "simulation_id": report.simulation_id or campaign.simulation_id,
            "source": source_data,
            "source_mode": source_data["source_mode"],
            "data_basis": source_data["data_basis"],
            "overall_sentiment": report.overall_sentiment,
            "conversion_probability": report.conversion_probability,
            "social_influence_index": report.social_influence_index,
            "message_resonance": report.message_resonance,
            "crisis_risk": report.crisis_risk,
            "brand_perception_shift": report.brand_perception_shift,
            "opinion_polarization": report.opinion_polarization,
            "winning_strategy": getattr(report, "winning_strategy", ""),
            "executive_summary": getattr(report, "executive_summary", ""),
        }
    except Exception as exc:
        logger.warning("KPI fetch failed for campaign %s: %s", campaign_id, exc)
        return {"campaign_id": campaign_id, "error": "KPI data unavailable"}


def _compute_comparison(kpis: list, org_id: str = "unknown") -> dict:
    """Compute side-by-side comparison, ranking, and source provenance."""
    if not kpis or len(kpis) < 2:
        return {"error": "Need at least 2 campaigns to compare"}

    valid = [k for k in kpis if "error" not in k]
    if len(valid) < 2:
        return {"error": "At least 2 campaigns must have valid data", "details": kpis}

    metrics_comparison = []
    for metric in COMPARISON_METRICS:
        key = metric["key"]
        values = [{"campaign_id": k["campaign_id"], "value": round(k.get(key, 0), 1)} for k in valid]
        winner = max(values, key=lambda v: v["value"]) if metric["higher_is_better"] else min(values, key=lambda v: v["value"])
        worst = min(v["value"] for v in values) if metric["higher_is_better"] else max(v["value"] for v in values)
        diff = abs(winner["value"] - worst)
        metrics_comparison.append({
            "key": key,
            "label": metric["label"],
            "unit": metric["unit"],
            "higher_is_better": metric["higher_is_better"],
            "values": values,
            "winner_campaign_id": winner["campaign_id"],
            "winner_value": winner["value"],
            "max_diff": round(diff, 1),
        })

    win_counts = {}
    for metric in metrics_comparison:
        winner_id = metric["winner_campaign_id"]
        win_counts[winner_id] = win_counts.get(winner_id, 0) + 1

    campaign_summaries = []
    for row in valid:
        source_data = _source_from_kpi(row)
        campaign_summaries.append({
            "campaign_id": row["campaign_id"],
            "campaign_name": _campaign_name_for_row(row, org_id),
            "direction": row.get("direction", ""),
            "kpi": row,
            "metric_wins": win_counts.get(row["campaign_id"], 0),
            "conversion_estimate": round(row.get("conversion_probability", 0), 1),
            "engagement_estimate": round(
                ((row.get("message_resonance", 0) or 0) + (row.get("social_influence_index", 0) or 0)) / 2,
                1,
            ),
            "risk_level": _risk_level(row.get("crisis_risk")),
            "segment_strengths": row.get("segment_strengths") or [],
            "segment_weaknesses": row.get("segment_weaknesses") or [],
            "trade_offs": row.get("trade_offs") or [],
            "recommended_use_case": row.get("recommended_use_case") or "Use for directional campaign planning after validation.",
            "source": source_data,
        })

    for row in campaign_summaries:
        row["rank_score"] = round(_rank_score(row["kpi"], win_counts), 2)

    ranked = sorted(campaign_summaries, key=lambda row: row["rank_score"], reverse=True)
    overall_winner = ranked[0]
    result_source = _comparison_source(valid)

    for row in campaign_summaries:
        row["is_overall_winner"] = row["campaign_id"] == overall_winner["campaign_id"]

    return {
        "source": result_source,
        "source_mode": result_source["source_mode"],
        "data_basis": result_source["data_basis"],
        "campaign_count": len(valid),
        "metrics_comparison": metrics_comparison,
        "campaign_summaries": campaign_summaries,
        "ranked_recommendation": [
            {
                "rank": idx + 1,
                "campaign_id": row["campaign_id"],
                "campaign_name": row["campaign_name"],
                "recommendation": row["recommended_use_case"],
                "reason": f"{row['metric_wins']} metric wins, conversion estimate {row['conversion_estimate']}%, risk {row['risk_level']}.",
                "source": row["source"],
            }
            for idx, row in enumerate(ranked)
        ],
        "trade_offs": [
            {
                "campaign_id": row["campaign_id"],
                "campaign_name": row["campaign_name"],
                "trade_offs": row["trade_offs"],
            }
            for row in campaign_summaries
        ],
        "risk_comparison": [
            {
                "campaign_id": row["campaign_id"],
                "campaign_name": row["campaign_name"],
                "crisis_risk": row["kpi"].get("crisis_risk", 0),
                "risk_level": row["risk_level"],
                "source": row["source"],
            }
            for row in campaign_summaries
        ],
        "overall_winner": {
            "campaign_id": overall_winner["campaign_id"],
            "campaign_name": overall_winner["campaign_name"],
            "metric_wins": overall_winner["metric_wins"],
            "total_metrics": len(COMPARISON_METRICS),
            "recommendation": "Use this direction as the lead route, then validate the highest-risk assumptions before launch.",
            "source": overall_winner["source"],
        },
    }


def _get_campaign_name_for_org(campaign_id: str, org_id: str) -> str:
    camp = CampaignService().get_campaign(campaign_id, org_id=org_id)
    return camp.name if camp else campaign_id[:12]


@comparator_bp.route("/demo/campaigns", methods=["GET"])
def get_demo_comparator_campaigns():
    """GET /api/comparator/demo/campaigns — public demo comparator variants."""
    campaigns = [
        {
            "id": row["campaign_id"],
            "campaign_id": row["campaign_id"],
            "name": row["campaign_name"],
            "direction": row["direction"],
            "source": _demo_variant_payload(row)["source"],
        }
        for row in COMPARATOR_DEMO_VARIANTS
    ]
    return jsonify({"success": True, "data": campaigns, "source": _comparison_source([_demo_variant_payload(row) for row in COMPARATOR_DEMO_VARIANTS])})


@comparator_bp.route("/demo/compare", methods=["POST"])
def compare_demo_campaigns():
    """POST /api/comparator/demo/compare — compare deterministic demo variants."""
    data = request.get_json(silent=True) or {}
    selected_ids = data.get("campaign_ids") or [row["campaign_id"] for row in COMPARATOR_DEMO_VARIANTS]
    if len(selected_ids) < 2:
        return jsonify({"success": False, "error": "Provide at least 2 campaign_ids"}), 400

    fixture_by_id = {row["campaign_id"]: _demo_variant_payload(row) for row in COMPARATOR_DEMO_VARIANTS}
    selected = [fixture_by_id[campaign_id] for campaign_id in selected_ids if campaign_id in fixture_by_id]
    if len(selected) < 2:
        return jsonify({"success": False, "error": "Demo comparator variants not found"}), 404

    result = _compute_comparison(selected, org_id="demo")
    return jsonify({"success": True, "data": result})


@comparator_bp.route("/compare", methods=["POST"])
def compare_campaigns():
    """POST /api/comparator/compare — compare authenticated organization campaigns."""
    data = request.get_json(silent=True) or {}
    campaign_ids = data.get("campaign_ids", [])

    if not campaign_ids or len(campaign_ids) < 2:
        return jsonify({"error": "Provide at least 2 campaign_ids"}), 400

    org_id = _get_org_id()
    missing = [cid for cid in campaign_ids if CampaignService().get_campaign(cid, org_id=org_id) is None]
    if missing:
        return jsonify({"success": False, "error": "Resource not found"}), 404

    kpis = [_fetch_kpi(cid, org_id) for cid in campaign_ids]
    result = _compute_comparison(kpis, org_id=org_id)
    if "error" in result:
        return jsonify({"success": False, "error": result["error"]}), 400

    return jsonify({"success": True, "data": result})


@comparator_bp.route("/metrics", methods=["GET"])
def get_comparison_metrics():
    """GET /api/comparator/metrics — list comparable metrics."""
    return jsonify({"success": True, "metrics": COMPARISON_METRICS})
