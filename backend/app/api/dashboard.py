"""
Dashboard API Routes — Executive KPIs, full reports, timeline, and segment data.

All endpoints require authentication (tenant-scoped via TenantMiddleware).
"""
import traceback
from flask import request, jsonify, g

from ..models.report import ExecutiveReport
from ..services.action_plan import ActionPlanService
from ..services.campaign_service import CampaignService
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


def _get_owned_campaign(campaign_id: str, org_id: str):
    return CampaignService().get_campaign(campaign_id, org_id=org_id)


def _resource_not_found():
    return jsonify({"success": False, "error": "Resource not found"}), 404


def _source_from_report(report: ExecutiveReport, campaign_id: str, simulation_id: str | None = None) -> dict:
    source_mode = report.source_mode or "unknown"
    data_basis = report.data_basis or "unknown"
    warning = ""
    if source_mode == "local_estimate":
        warning = "Local deterministic estimate because no persisted real simulation KPI output is available."
    elif source_mode == "backend_verified":
        warning = "Backend-verified persisted simulation KPI output."
    elif source_mode == "unknown":
        warning = "Result source is unknown; use this view for orientation only."
    return {
        "type": source_mode,
        "source_mode": source_mode,
        "run_id": report.run_id,
        "campaign_id": campaign_id,
        "simulation_id": report.simulation_id or simulation_id,
        "data_basis": data_basis,
        "confidence": report.confidence,
        "limitations": report.limitations,
        "warning": warning,
    }


def _dashboard_report_for_campaign(campaign, org_id: str) -> ExecutiveReport:
    summary = campaign.results_summary if isinstance(campaign.results_summary, dict) else None
    if summary:
        try:
            report = ExecutiveReport.from_dict(summary)
            if report.source_mode == "backend_verified" and report.data_basis == "real_simulation":
                return report
            if report.source_mode == "local_estimate" and report.data_basis == "local_estimate":
                return report
        except Exception:
            logger.warning("Ignoring malformed campaign results_summary for %s", campaign.campaign_id)

    return _get_calculator().calculate(
        campaign_id=campaign.campaign_id,
        org_id=org_id,
        simulation_id=campaign.simulation_id,
    )


# ---------------------------------------------------------------------------
# GET /api/dashboard/campaign/<campaign_id>/kpi
# ---------------------------------------------------------------------------

@dashboard_bp.route("/campaign/<campaign_id>/kpi", methods=["GET"])
def get_campaign_kpi(campaign_id: str):
    """Return calculated KPIs for a campaign (lightweight — just the numbers)."""
    try:
        org_id = _get_org_id()
        campaign = _get_owned_campaign(campaign_id, org_id)
        if not campaign:
            return _resource_not_found()
        report = _dashboard_report_for_campaign(campaign, org_id)
        source = _source_from_report(report, campaign_id, campaign.simulation_id)

        kpi_payload = {
            "campaign_id": campaign_id,
            "report_id": report.report_id,
            "source": source,
            "source_mode": source["source_mode"],
            "data_basis": source["data_basis"],
            "run_id": source["run_id"],
            "simulation_id": source["simulation_id"],
            "confidence": source["confidence"],
            "limitations": source["limitations"],
            "overall_sentiment": report.overall_sentiment,
            "conversion_probability": report.conversion_probability,
            "social_influence_index": report.social_influence_index,
            "message_resonance": report.message_resonance,
            "crisis_risk": report.crisis_risk,
            "brand_perception_shift": report.brand_perception_shift,
            "opinion_polarization": report.opinion_polarization,
            "platform_engagement_metrics": [
                metric.model_dump() for metric in report.platform_engagement_metrics
            ],
            "generated_at": report.generated_at,
            "action_plan": ActionPlanService().generate(
                campaign={"id": campaign_id, "name": campaign.name},
                kpis=report.model_dump(),
                segments=[seg.model_dump() for seg in report.sentiment_by_segment],
                evidence={},
                source=source,
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
        campaign = _get_owned_campaign(campaign_id, org_id)
        if not campaign:
            return _resource_not_found()
        report = _dashboard_report_for_campaign(campaign, org_id)
        source = _source_from_report(report, campaign_id, campaign.simulation_id)

        data = report.to_dict()
        data["source"] = source
        data["source_mode"] = source["source_mode"]
        data["data_basis"] = source["data_basis"]
        data["action_plan"] = ActionPlanService().generate(
            campaign={"id": campaign_id, "name": campaign.name},
            kpis=data,
            segments=data.get("sentiment_by_segment", []),
            evidence={},
            source=source,
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
        campaign = _get_owned_campaign(campaign_id, org_id)
        if not campaign:
            return _resource_not_found()
        report = _dashboard_report_for_campaign(campaign, org_id)
        source = _source_from_report(report, campaign_id, campaign.simulation_id)

        timeline = [pt.model_dump() for pt in report.sentiment_timeline]

        return jsonify({
            "success": True,
            "data": {
                "campaign_id": campaign_id,
                "points": len(timeline),
                "timeline": timeline,
                "source": source,
                "source_mode": source["source_mode"],
                "data_basis": source["data_basis"],
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
        campaign = _get_owned_campaign(campaign_id, org_id)
        if not campaign:
            return _resource_not_found()
        report = _dashboard_report_for_campaign(campaign, org_id)
        source = _source_from_report(report, campaign_id, campaign.simulation_id)

        segments = [seg.model_dump() for seg in report.sentiment_by_segment]

        return jsonify({
            "success": True,
            "data": {
                "campaign_id": campaign_id,
                "count": len(segments),
                "segments": segments,
                "source": source,
                "source_mode": source["source_mode"],
                "data_basis": source["data_basis"],
            },
        })

    except Exception as e:
        logger.error(f"Segments fetch failed for campaign {campaign_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }), 500
