"""Industry Template API — list, import, validate, delete industry templates."""

from flask import Blueprint, request, jsonify

from ..authz import ADMIN_ROLES, role_required
from ..services.industry_templates import IndustryTemplateLoader, TemplateValidationError

industry_bp = Blueprint("industry", __name__)


# ── List all templates ────────────────────────────────────

@industry_bp.route("/templates", methods=["GET"])
def list_templates():
    """GET /api/industry/templates — list all industry templates (metadata only)."""
    try:
        templates = IndustryTemplateLoader.list_templates()
        builtin = sum(1 for t in templates if t.get("source") == "builtin")
        uploaded = len(templates) - builtin
        return jsonify({"templates": templates, "count": len(templates), "builtin_count": builtin, "uploaded_count": uploaded})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Import template JSON ──────────────────────────────────

@industry_bp.route("/templates/import", methods=["POST"])
@role_required(*ADMIN_ROLES)
def import_template():
    """POST /api/industry/templates/import — upload a JSON template file or raw JSON body.

    Accepts:
        - multipart/form-data with a file field named 'file' (recommended)
        - application/json body with the template JSON

    Returns the imported template metadata on success, or validation errors.
    """
    template_data = None

    # Option 1: file upload
    if "file" in request.files:
        file = request.files["file"]
        if file.filename == "" or not file.filename.lower().endswith(".json"):
            return jsonify({"error": "Please upload a .json file"}), 400
        try:
            import json
            template_data = json.loads(file.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400

    # Option 2: raw JSON body
    elif request.is_json:
        template_data = request.get_json()
    else:
        return jsonify({"error": "Send a JSON file (multipart/form-data field 'file') or JSON body"}), 400

    if not template_data:
        return jsonify({"error": "Empty template data"}), 400

    try:
        template_id, metadata = IndustryTemplateLoader.import_template(template_data)
        return jsonify({"success": True, "template_id": template_id, "metadata": metadata}), 201
    except TemplateValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 422


# ── Validate template JSON (without saving) ───────────────

@industry_bp.route("/templates/validate", methods=["POST"])
@role_required(*ADMIN_ROLES)
def validate_template():
    """POST /api/industry/templates/validate — validate template JSON without importing."""
    if not request.is_json:
        return jsonify({"error": "Send JSON body"}), 400

    data = request.get_json()
    errors = IndustryTemplateLoader.validate_template_json(data)

    if errors:
        return jsonify({"valid": False, "errors": errors}), 422
    return jsonify({"valid": True, "message": "Template is valid and ready for import"})


# ── Delete user-uploaded template ─────────────────────────

@industry_bp.route("/templates/<template_id>", methods=["DELETE"])
@role_required(*ADMIN_ROLES)
def delete_template(template_id: str):
    """DELETE /api/industry/templates/{id} — remove a user-uploaded template."""
    # Prevent deleting built-in templates
    tmpl = IndustryTemplateLoader.get_template(template_id)
    if not tmpl:
        return jsonify({"error": f"Template '{template_id}' not found"}), 404
    if tmpl.get("_source") == "builtin":
        return jsonify({"error": "Cannot delete built-in templates"}), 403

    if IndustryTemplateLoader.delete_template(template_id):
        return jsonify({"success": True, "message": f"Template '{template_id}' deleted"})
    return jsonify({"error": f"Failed to delete template '{template_id}'"}), 500


# ── Get full campaign preset ──────────────────────────────

@industry_bp.route("/templates/<template_id>/preset", methods=["GET"])
def get_campaign_preset(template_id: str):
    preset = IndustryTemplateLoader.build_campaign_preset(template_id)
    if preset is None:
        return jsonify({"error": f"Template '{template_id}' not found"}), 404
    return jsonify(preset)


# ── Get persona segments ──────────────────────────────────

@industry_bp.route("/templates/<template_id>/personas", methods=["GET"])
def get_persona_segments(template_id: str):
    segments = IndustryTemplateLoader.get_persona_segments(template_id)
    if not segments:
        return jsonify({"error": f"Template '{template_id}' not found"}), 404
    return jsonify({"template_id": template_id, "segments": segments, "total_archetypes": sum(len(s.get("archetypes", [])) for s in segments)})


# ── Get crisis scenarios ──────────────────────────────────

@industry_bp.route("/templates/<template_id>/crises", methods=["GET"])
def get_crisis_scenarios(template_id: str):
    scenarios = IndustryTemplateLoader.get_crisis_scenarios(template_id)
    if not scenarios:
        return jsonify({"error": f"Template '{template_id}' not found"}), 404
    return jsonify({"template_id": template_id, "scenarios": scenarios})


# ── Get document seeds ────────────────────────────────────

@industry_bp.route("/templates/<template_id>/seeds", methods=["GET"])
def get_document_seeds(template_id: str):
    seeds = IndustryTemplateLoader.get_document_seeds(template_id)
    if not seeds:
        return jsonify({"error": f"Template '{template_id}' not found"}), 404
    return jsonify({"template_id": template_id, "seeds": [
        {"id": s["id"], "name_th": s.get("name_th", s["id"]), "description_th": s.get("description_th", "")}
        for s in seeds
    ]})


# ── Get seed document content ─────────────────────────────

@industry_bp.route("/templates/<template_id>/seeds/<seed_id>/content", methods=["GET"])
def get_seed_content(template_id: str, seed_id: str):
    doc = IndustryTemplateLoader.generate_seed_document(template_id, seed_id)
    if doc is None:
        return jsonify({"error": f"Seed document '{seed_id}' not found in template '{template_id}'"}), 404
    return jsonify(doc)
