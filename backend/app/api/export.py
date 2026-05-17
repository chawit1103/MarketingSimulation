"""Export API — generate PPTX/PDF slides from simulation data."""

from flask import Blueprint, request, jsonify, send_file, g
import io
import re

from ..services.export_engine import PPTXGenerator
from ..services.strategy_pack import StrategyPackService
from ..services.audit_log_service import record_audit_event
from ..authz import ANALYST_ROLES, role_required
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.export")

export_bp = Blueprint("export", __name__)

_ALLOWED_EXPORT_TYPES = {
    "dashboard",
    "strategy_pack",
    "report",
    "generic",
    "comparison",
    "war_room",
    "budget_scenario",
    "calibration",
}
_ALLOWED_SOURCE_MODES = {
    "demo_mode",
    "local_estimate",
    "live_backend",
    "backend_verified",
    "unknown",
}
_ALLOWED_DATA_BASIS = {
    "demo_fixture",
    "local_estimate",
    "real_simulation",
    "manual_input",
    "rule_based",
    "unknown",
}


def _safe_pptx_filename(value: str | None, fallback: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or fallback)).strip("._-")
    base = base or fallback
    return base if base.lower().endswith(".pptx") else f"{base}.pptx"


def _safe_category(value: object, allowed: set[str], fallback: str = "unknown") -> str:
    normalized = re.sub(r"[^a-z0-9_]+", "_", str(value or fallback).strip().lower()).strip("_")
    if normalized in allowed:
        return normalized
    return fallback


def _safe_export_type(value: object, fallback: str = "generic") -> str:
    """Return a categorical export type safe for audit metadata."""
    return _safe_category(value, _ALLOWED_EXPORT_TYPES, fallback=fallback)


def _safe_source_metadata(source: dict | None) -> dict:
    source = source or {}
    return {
        "source_mode": _safe_category(source.get("source_mode"), _ALLOWED_SOURCE_MODES),
        "data_basis": _safe_category(source.get("data_basis"), _ALLOWED_DATA_BASIS),
    }


def _get_org_id() -> str | None:
    return str(g.current_org_id) if g.get("current_org_id") else None


def _audit_export(format_name: str, export_type: str, metadata: dict | None = None) -> None:
    org_id = _get_org_id()
    if not org_id:
        return
    record_audit_event(
        org_id=org_id,
        event_type="export_generated",
        resource_type="export",
        metadata={
            "format": format_name,
            "export_type": _safe_export_type(export_type),
            **(metadata or {}),
        },
    )


@export_bp.route("/strategy-pack", methods=["POST"])
@role_required(*ANALYST_ROLES)
def export_strategy_pack():
    """POST /api/export/strategy-pack — build a client-ready strategy payload."""
    data = request.get_json(silent=True) or {}

    try:
        pack = StrategyPackService().build(data)
        _audit_export(
            "json",
            "strategy_pack",
            _safe_source_metadata(pack.get("source")),
        )
        return jsonify({
            "success": True,
            "data": pack,
        })
    except Exception:
        logger.exception("Failed to build strategy pack export")
        return jsonify({
            "success": False,
            "error": "Could not build strategy pack export.",
        }), 500


@export_bp.route("/strategy-pack/pptx", methods=["POST"])
@role_required(*ANALYST_ROLES)
def export_strategy_pack_pptx():
    """POST /api/export/strategy-pack/pptx — render strategy pack payload as PPTX."""
    data = request.get_json(silent=True) or {}

    try:
        pack = data.get("strategy_pack")
        if not isinstance(pack, dict) or pack.get("version") != "strategy_pack_v1":
            pack = StrategyPackService().build(data)

        buffer = PPTXGenerator().generate({
            "slide_type": "strategy_pack",
            "strategy_pack": pack,
        })
        white_label = pack.get("white_label") or {}
        filename = _safe_pptx_filename(
            data.get("filename") or white_label.get("campaign_name"),
            "strategy_pack",
        )
        _audit_export(
            "pptx",
            "strategy_pack",
            _safe_source_metadata(pack.get("source")),
        )
        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            as_attachment=True,
            download_name=filename,
        )
    except Exception:
        logger.exception("Failed to render strategy pack PPTX")
        return jsonify({
            "success": False,
            "error": "Could not render strategy pack PPTX.",
        }), 500


@export_bp.route("/pptx", methods=["POST"])
@role_required(*ANALYST_ROLES)
def export_pptx():
    """POST /api/export/pptx — generate and download a PPTX deck.

    Body: { "slide_type": "dashboard", "title": "...", "kpis": {...}, ... }

    Returns: Binary .pptx file download.
    """
    data = request.get_json(silent=True) or {}

    generator = PPTXGenerator()
    buffer = generator.generate(data)

    filename = data.get("filename", "msaas_report")
    if not filename.endswith(".pptx"):
        filename += ".pptx"
    _audit_export("pptx", _safe_export_type(data.get("slide_type"), "generic"))

    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        as_attachment=True,
        download_name=filename,
    )


@export_bp.route("/csv", methods=["POST"])
@role_required(*ANALYST_ROLES)
def export_csv():
    """POST /api/export/csv — lightweight CSV export as fallback."""
    import csv

    data = request.get_json(silent=True) or {}

    buffer = io.BytesIO()
    wrapper = io.TextIOWrapper(buffer, write_through=True, encoding='utf-8', newline='')
    writer = csv.writer(wrapper)

    writer.writerow([data.get("title", "MSaaS Report")])
    writer.writerow([])

    kpis = data.get("kpis", {})
    if kpis:
        writer.writerow(["KPI", "Value"])
        for k, v in kpis.items():
            writer.writerow([k, v])

    timeline = data.get("timeline", [])
    if timeline:
        writer.writerow([])
        writer.writerow(["Round", "Sentiment", "Actions"])
        for pt in timeline:
            writer.writerow([pt.get("round_num", ""), pt.get("avg_sentiment", ""), pt.get("action_count", "")])

    action_plan = data.get("action_plan") or {}
    sections = action_plan.get("sections") or {}
    if sections:
        writer.writerow([])
        writer.writerow(["Action Plan Source", (action_plan.get("source") or {}).get("type", "unknown")])
        writer.writerow(["Action Plan Disclaimer", action_plan.get("disclaimer", "")])
        writer.writerow([])
        writer.writerow(["Section", "Recommendation", "Reason", "Expected Impact", "Risk"])
        for section_key, section in sections.items():
            for item in section.get("items", []):
                writer.writerow([
                    section.get("title", section_key),
                    item.get("recommendation", ""),
                    item.get("reason", ""),
                    item.get("expected_impact", ""),
                    item.get("risk", ""),
                ])

    wrapper.detach()
    buffer.seek(0)
    _audit_export("csv", "report")

    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{data.get('filename', 'report')}.csv",
    )
