"""Calibration API for manual actual-results import."""

from __future__ import annotations

from flask import Blueprint, g, jsonify, request

from ..authz import ANALYST_ROLES, ANY_AUTHENTICATED_ROLES, role_required
from ..services.audit_log_service import record_audit_event
from ..services.calibration_service import CalibrationService, CalibrationValidationError
from ..utils.logger import get_logger


logger = get_logger("mirofish.api.calibration")
calibration_bp = Blueprint("calibration", __name__)
calibration_service = CalibrationService()


def _current_org_id() -> str:
    org_id = g.get("current_org_id")
    if not org_id:
        raise CalibrationValidationError("Organization context is required")
    return str(org_id)


def _payload_from_request():
    if request.files.get("file"):
        uploaded = request.files["file"]
        filename = (uploaded.filename or "").lower()
        text = uploaded.read().decode("utf-8")
        if filename.endswith(".json"):
            return calibration_service.parse_json_text(text)
        if filename.endswith(".csv"):
            return calibration_service.parse_csv_text(text)
        raise CalibrationValidationError("Only CSV and JSON actual-results uploads are supported")

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise CalibrationValidationError("Request body must be a JSON object or CSV/JSON file upload")
    return data


@calibration_bp.route("/actual-results", methods=["POST"])
@role_required(*ANALYST_ROLES)
def import_actual_results():
    """Import aggregate actual campaign results and compare with estimates."""
    try:
        payload = _payload_from_request()
        result = calibration_service.import_actual_results(
            org_id=_current_org_id(),
            payload=payload,
        )
        record_audit_event(
            org_id=_current_org_id(),
            event_type="calibration_imported",
            resource_type="calibration_record",
            resource_id=result.get("record_id"),
            metadata={
                "campaign_id": result.get("campaign_id"),
                "calibration_status": result.get("calibration_status"),
                "source_mode": (result.get("source") or {}).get("source_mode"),
                "data_basis": (result.get("source") or {}).get("data_basis"),
            },
        )
        return jsonify({"success": True, "data": result}), 201
    except CalibrationValidationError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
            "code": "calibration_validation_failed",
        }), 422
    except UnicodeDecodeError:
        return jsonify({
            "success": False,
            "error": "Uploaded file must be UTF-8 encoded",
            "code": "calibration_file_encoding_failed",
        }), 422
    except Exception as exc:
        logger.exception("Calibration import failed: %s", exc.__class__.__name__)
        return jsonify({
            "success": False,
            "error": "Calibration import failed",
            "code": "calibration_import_failed",
        }), 500


@calibration_bp.route("/status/<campaign_id>", methods=["GET"])
@role_required(*ANY_AUTHENTICATED_ROLES)
def get_calibration_status(campaign_id):
    """Return calibration status for a campaign in the current organization."""
    try:
        result = calibration_service.get_status(
            org_id=_current_org_id(),
            campaign_id=campaign_id,
        )
        return jsonify({"success": True, "data": result})
    except CalibrationValidationError as exc:
        return jsonify({
            "success": False,
            "error": str(exc),
            "code": "calibration_context_missing",
        }), 422
    except Exception as exc:
        logger.exception("Calibration status failed: %s", exc.__class__.__name__)
        return jsonify({
            "success": False,
            "error": "Calibration status failed",
            "code": "calibration_status_failed",
        }), 500
