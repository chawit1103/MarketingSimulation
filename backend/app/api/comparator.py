"""Campaign Comparator — A/B test comparison API.

Compares KPIs across multiple campaigns and identifies winners per metric.
"""

from flask import Blueprint, request, jsonify, g

from ..models.report import ExecutiveReport
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


# ── Helpers ──────────────────────────────────────────────

def _fetch_kpi(campaign_id: str, org_id: str) -> dict:
    """Fetch KPI data for one campaign. Returns dict or error dict."""
    try:
        calc = _get_calculator()
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)
        return {
            "campaign_id": campaign_id,
            "report_id": report.report_id,
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
    except Exception as e:
        logger.warning(f"KPI fetch failed for campaign {campaign_id}: {e}")
        return {"campaign_id": campaign_id, "error": str(e)}


# ── Comparison metrics ───────────────────────────────────

COMPARISON_METRICS = [
    {"key": "overall_sentiment",         "label": "Overall Sentiment",      "unit": "",  "higher_is_better": True},
    {"key": "conversion_probability",     "label": "Conversion Probability", "unit": "%", "higher_is_better": True},
    {"key": "social_influence_index",     "label": "Social Influence",       "unit": "",  "higher_is_better": True},
    {"key": "message_resonance",          "label": "Message Resonance",      "unit": "%", "higher_is_better": True},
    {"key": "crisis_risk",                "label": "Crisis Risk",            "unit": "%", "higher_is_better": False},
    {"key": "brand_perception_shift",     "label": "Brand Perception Shift", "unit": "",  "higher_is_better": True},
    {"key": "opinion_polarization",       "label": "Opinion Polarization",   "unit": "",  "higher_is_better": False},
]


def _compute_comparison(kpis: list) -> dict:
    """Compute side-by-side comparison + winners from a list of KPI dicts."""
    if not kpis or len(kpis) < 2:
        return {"error": "Need at least 2 campaigns to compare"}

    valid = [k for k in kpis if "error" not in k]
    if len(valid) < 2:
        return {"error": "At least 2 campaigns must have valid data", "details": kpis}

    # Build per-metric comparison
    metrics_comparison = []
    for metric in COMPARISON_METRICS:
        key = metric["key"]
        values = []
        for k in valid:
            values.append({
                "campaign_id": k["campaign_id"],
                "value": round(k.get(key, 0), 1),
            })

        # Find winner
        if metric["higher_is_better"]:
            winner = max(values, key=lambda v: v["value"])
        else:
            winner = min(values, key=lambda v: v["value"])

        # Calculate diff
        if len(values) >= 2:
            best = winner["value"]
            worst = min(v["value"] for v in values) if metric["higher_is_better"] else max(v["value"] for v in values)
            diff = abs(best - worst) if best != worst else 0

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

    # Overall winner — campaign with most metric wins
    win_counts = {}
    for mc in metrics_comparison:
        wid = mc["winner_campaign_id"]
        win_counts[wid] = win_counts.get(wid, 0) + 1

    overall_winner_id = max(win_counts, key=win_counts.get)
    overall_winner_name = _get_campaign_name(overall_winner_id)

    # Build summary per campaign
    campaign_summaries = []
    for k in valid:
        wins = win_counts.get(k["campaign_id"], 0)
        campaign_summaries.append({
            "campaign_id": k["campaign_id"],
            "campaign_name": _get_campaign_name(k["campaign_id"]),
            "kpi": k,
            "metric_wins": wins,
            "is_overall_winner": k["campaign_id"] == overall_winner_id,
        })

    return {
        "campaign_count": len(valid),
        "metrics_comparison": metrics_comparison,
        "campaign_summaries": campaign_summaries,
        "overall_winner": {
            "campaign_id": overall_winner_id,
            "campaign_name": overall_winner_name,
            "metric_wins": win_counts[overall_winner_id],
            "total_metrics": len(COMPARISON_METRICS),
        },
    }


def _get_campaign_name(campaign_id: str) -> str:
    """Get campaign name from storage."""
    try:
        from ..services.campaign_service import CampaignService
        svc = CampaignService()
        for org_dir in ["organizations"]:  # simplified
            camp = svc.get_campaign(campaign_id)
            if camp:
                return camp.name
    except Exception:
        pass
    return campaign_id[:12]


# ── API Routes ───────────────────────────────────────────

@comparator_bp.route("/compare", methods=["POST"])
def compare_campaigns():
    """POST /api/comparator/compare
    
    Body: { "campaign_ids": ["cmp_xxx", "cmp_yyy"] }
    
    Returns side-by-side KPI comparison with winner detection.
    """
    data = request.get_json(silent=True) or {}
    campaign_ids = data.get("campaign_ids", [])

    if not campaign_ids or len(campaign_ids) < 2:
        return jsonify({"error": "Provide at least 2 campaign_ids"}), 400

    org_id = _get_org_id()

    # Fetch KPIs for all campaigns
    kpis = [_fetch_kpi(cid, org_id) for cid in campaign_ids]

    # Compute comparison
    result = _compute_comparison(kpis)

    return jsonify({"success": True, "data": result})


@comparator_bp.route("/metrics", methods=["GET"])
def get_comparison_metrics():
    """GET /api/comparator/metrics — list comparable metrics."""
    return jsonify({"success": True, "metrics": COMPARISON_METRICS})
