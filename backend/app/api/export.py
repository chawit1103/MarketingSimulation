"""Export API — generate PPTX/PDF slides from simulation data."""

from flask import Blueprint, request, jsonify, send_file
import io

from ..services.export_engine import PPTXGenerator
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.export")

export_bp = Blueprint("export", __name__)


@export_bp.route("/pptx", methods=["POST"])
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

    return send_file(
        buffer,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        as_attachment=True,
        download_name=filename,
    )


@export_bp.route("/csv", methods=["POST"])
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

    wrapper.detach()
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"{data.get('filename', 'report')}.csv",
    )
