"""
Dashboard API Routes — Executive KPIs, full reports, timeline, and segment data.

All endpoints require authentication (tenant-scoped via TenantMiddleware).
"""
import traceback
from flask import request, jsonify, g

from ..models.report import ExecutiveReport
from ..services.action_plan import ActionPlanService
from ..services.kpi_calculator import KPICalculator
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.dashboard")

# Import the blueprint defined in api/__init__.py
from . import dashboard_bp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_calculator() -> KPICalculator:
    """Return a KPICalculator instance (can be cached on app later)."""
    return KPICalculator()


def _get_org_id() -> str:
    """Extract org_id from Flask g (set by TenantMiddleware)."""
    org = getattr(g, "current_org", None)
    if org:
        return org.get("org_id", "unknown") if isinstance(org, dict) else getattr(org, "org_id", "unknown")
    user = getattr(g, "current_user", None)
    if user:
        return user.get("org_id", "unknown") if isinstance(user, dict) else getattr(user, "org_id", "unknown")
    return "unknown"


# ---------------------------------------------------------------------------
# GET /api/dashboard/campaign/<campaign_id>/kpi
# ---------------------------------------------------------------------------

@dashboard_bp.route("/campaign/<campaign_id>/kpi", methods=["GET"])
def get_campaign_kpi(campaign_id: str):
    """Return calculated KPIs for a campaign (lightweight — just the numbers)."""
    try:
        org_id = _get_org_id()
        calc = _get_calculator()
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)

        kpi_payload = {
            "campaign_id": campaign_id,
            "report_id": report.report_id,
            "overall_sentiment": report.overall_sentiment,
            "conversion_probability": report.conversion_probability,
            "social_influence_index": report.social_influence_index,
            "message_resonance": report.message_resonance,
            "crisis_risk": report.crisis_risk,
            "brand_perception_shift": report.brand_perception_shift,
            "opinion_polarization": report.opinion_polarization,
            "generated_at": report.generated_at,
            "action_plan": ActionPlanService().generate(
                campaign={"id": campaign_id},
                kpis=report.model_dump(),
                segments=[seg.model_dump() for seg in report.sentiment_by_segment],
                evidence={},
                source={"type": "backend_verified"},
            ),
        }
        return jsonify({"success": True, "data": kpi_payload})

    except Exception as e:
        logger.error(f"KPI fetch failed for campaign {campaign_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500


# ---------------------------------------------------------------------------
# GET /api/dashboard/campaign/<campaign_id>/report
# ---------------------------------------------------------------------------

@dashboard_bp.route("/campaign/<campaign_id>/report", methods=["GET"])
def get_campaign_report(campaign_id: str):
    """Return the full executive report for a campaign."""
    try:
        org_id = _get_org_id()
        calc = _get_calculator()
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)

        data = report.to_dict()
        data["action_plan"] = ActionPlanService().generate(
            campaign={"id": campaign_id},
            kpis=data,
            segments=data.get("sentiment_by_segment", []),
            evidence={},
            source={"type": "backend_verified"},
        )

        return jsonify({"success": True, "data": data})

    except Exception as e:
        logger.error(f"Report fetch failed for campaign {campaign_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500


# ---------------------------------------------------------------------------
# GET /api/dashboard/campaign/<campaign_id>/timeline
# ---------------------------------------------------------------------------

@dashboard_bp.route("/campaign/<campaign_id>/timeline", methods=["GET"])
def get_campaign_timeline(campaign_id: str):
    """Return sentiment timeline data for a campaign."""
    try:
        org_id = _get_org_id()
        calc = _get_calculator()
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)

        timeline = [pt.model_dump() for pt in report.sentiment_timeline]

        return jsonify({
            "success": True,
            "data": {
                "campaign_id": campaign_id,
                "points": len(timeline),
                "timeline": timeline,
            },
        })

    except Exception as e:
        logger.error(f"Timeline fetch failed for campaign {campaign_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500


# ---------------------------------------------------------------------------
# GET /api/dashboard/campaign/<campaign_id>/segments
# ---------------------------------------------------------------------------

@dashboard_bp.route("/campaign/<campaign_id>/segments", methods=["GET"])
def get_campaign_segments(campaign_id: str):
    """Return segment sentiment breakdown for a campaign."""
    try:
        org_id = _get_org_id()
        calc = _get_calculator()
        report = calc.calculate(campaign_id=campaign_id, org_id=org_id)

        segments = [seg.model_dump() for seg in report.sentiment_by_segment]

        return jsonify({
            "success": True,
            "data": {
                "campaign_id": campaign_id,
                "count": len(segments),
                "segments": segments,
            },
        })

    except Exception as e:
        logger.error(f"Segments fetch failed for campaign {campaign_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500
