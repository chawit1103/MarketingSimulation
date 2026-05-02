"""Industry Template Loader — loads industry-specific persona/scenario templates.

Architecture:
    industry_templates/
        __init__.py          ← this file (loader + validators)
        energy.json          ← Built-in: Energy/Oil/Utilities
        finance.json         ← Built-in: Banking/Finance (future)

    uploads/industry_templates/  ← User-imported templates (hot-reloaded)
        any_name.json

Each JSON file defines:
    - Persona segments with archetypes (TH-specific consumer personas)
    - Crisis scenarios specific to that industry
    - Document seed templates (press releases, statements)
    - Default campaign configurations (platform, rounds, language)
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger('mirofish.industry_templates')

BUILTIN_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "uploads", "industry_templates"
)

# ── JSON Schema for template validation ──────────────────
REQUIRED_TOP_KEYS = {"id", "name_th", "name_en", "persona_segments", "crisis_scenarios", "document_seeds"}
REQUIRED_SEGMENT_KEYS = {"id", "name_th", "name_en", "archetypes"}
REQUIRED_ARCHETYPE_KEYS = {"id", "name_th", "name_en", "age_range", "income", "regions", "occupation_th", "channels", "narrative_th", "purchase_style"}
REQUIRED_CRISIS_KEYS = {"id", "name_th", "name_en", "trigger", "impact"}
REQUIRED_SEED_KEYS = {"id", "name_th", "description_th", "content"}
REQUIRED_DEEP_PRESET_KEYS = {
    "target_segment_archetypes",
    "common_objections",
    "crisis_triggers",
    "typical_kpis",
    "channel_behavior",
    "competitor_archetypes",
    "legal_regulatory_sensitivities",
    "proof_point_requirements",
    "sample_brief",
    "sample_risk_checklist",
    "sample_action_plan_hints",
    "assumptions",
    "limitations",
}
VALID_IMPACTS = {"negative", "positive", "mixed"}
VALID_PURCHASE_STYLES = {"impulsive", "price_sensitive", "researcher", "early_adopter", "social_proof", "brand_loyal", "traditional"}
VALID_INCOMES = {"low", "lower_middle", "middle", "upper_middle", "high"}


class TemplateValidationError(Exception):
    """Raised when imported template JSON fails validation."""
    pass


class IndustryTemplateLoader:
    """Loads and caches industry template definitions from builtin + uploads."""

    _templates: Dict[str, Dict[str, Any]] = {}
    _loaded = False

    # ── Public API ──────────────────────────────────────────

    @classmethod
    def list_templates(cls) -> List[Dict[str, Any]]:
        cls._ensure_loaded()
        return [
            {
                "id": tid,
                "name_th": tmpl.get("name_th", tid),
                "name_en": tmpl.get("name_en", tid),
                "description_th": tmpl.get("description_th", ""),
                "description_en": tmpl.get("description_en", ""),
                "icon": tmpl.get("icon", "📋"),
                "color": tmpl.get("color", "#000"),
                "source": tmpl.get("_source", "builtin"),
                "objectives": tmpl.get("objectives", []),
                "industry_depth": tmpl.get("industry_depth", "standard"),
                "assumptions": tmpl.get("deep_preset", {}).get("assumptions", []),
                "limitations": tmpl.get("deep_preset", {}).get("limitations", []),
                "persona_segment_count": len(tmpl.get("persona_segments", [])),
                "crisis_scenario_count": len(tmpl.get("crisis_scenarios", [])),
                "document_seed_count": len(tmpl.get("document_seeds", [])),
            }
            for tid, tmpl in cls._templates.items()
        ]

    @classmethod
    def get_template(cls, template_id: str) -> Optional[Dict[str, Any]]:
        cls._ensure_loaded()
        return cls._templates.get(template_id)

    @classmethod
    def get_persona_segments(cls, template_id: str) -> List[Dict[str, Any]]:
        tmpl = cls.get_template(template_id)
        return tmpl.get("persona_segments", []) if tmpl else []

    @classmethod
    def get_crisis_scenarios(cls, template_id: str) -> List[Dict[str, Any]]:
        tmpl = cls.get_template(template_id)
        return tmpl.get("crisis_scenarios", []) if tmpl else []

    @classmethod
    def get_document_seeds(cls, template_id: str) -> List[Dict[str, Any]]:
        tmpl = cls.get_template(template_id)
        return tmpl.get("document_seeds", []) if tmpl else []

    @classmethod
    def build_campaign_preset(cls, template_id: str) -> Optional[Dict[str, Any]]:
        tmpl = cls.get_template(template_id)
        if not tmpl:
            return None
        return {
            "template_id": template_id,
            "name_th": tmpl.get("name_th"),
            "name_en": tmpl.get("name_en"),
            "description_th": tmpl.get("description_th"),
            "description_en": tmpl.get("description_en"),
            "icon": tmpl.get("icon"),
            "color": tmpl.get("color"),
            "target": tmpl.get("target_audience", {}),
            "sim_config": {
                "platform": tmpl.get("default_platform", "both"),
                "max_rounds": tmpl.get("default_max_rounds", 20),
                "language": tmpl.get("default_language", "th"),
            },
            "default_objective": tmpl.get("default_objective", "crisis_simulation"),
            "campaign_duration": tmpl.get("campaign_duration", ""),
            "budget_range": tmpl.get("budget_range", ""),
            "primary_kpi": tmpl.get("primary_kpi", ""),
            "competitor_context": tmpl.get("competitor_context", ""),
            "brand_constraints": tmpl.get("brand_constraints", ""),
            "risk_legal_notes": tmpl.get("risk_legal_notes", ""),
            "industry_depth": tmpl.get("industry_depth", "standard"),
            "deep_preset": tmpl.get("deep_preset", {}),
            "available_objectives": tmpl.get("objectives", []),
            "persona_segments": tmpl.get("persona_segments", []),
            "crisis_scenarios": tmpl.get("crisis_scenarios", []),
            "document_seeds": [
                {
                    "id": ds["id"],
                    "name_th": ds.get("name_th", ds["id"]),
                    "name_en": ds.get("name_en", ds.get("name_th", ds["id"])),
                    "description_th": ds.get("description_th", ""),
                    "description_en": ds.get("description_en", ds.get("description_th", "")),
                }
                for ds in tmpl.get("document_seeds", [])
            ],
        }

    @classmethod
    def generate_seed_document(cls, template_id: str, seed_id: str) -> Optional[Dict[str, str]]:
        tmpl = cls.get_template(template_id)
        if not tmpl:
            return None
        for seed in tmpl.get("document_seeds", []):
            if seed["id"] == seed_id:
                return {
                    "name": f"{seed.get('name_th', seed_id)}.md",
                    "content": seed.get("content", ""),
                    "type": "text/markdown",
                }
        return None

    # ── Import / Delete ─────────────────────────────────────

    @classmethod
    def import_template(cls, data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Validate and save a user-imported template JSON. Returns (template_id, metadata)."""
        cls._validate_template(data)
        template_id = data["id"]

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filepath = os.path.join(UPLOAD_DIR, f"{template_id}.json")

        if os.path.exists(filepath):
            raise TemplateValidationError(f"Template '{template_id}' already exists. Delete it first or change the id.")

        data["_source"] = "upload"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Hot-reload into cache
        cls._templates[template_id] = data
        logger.info(f"Imported user template: {template_id}")

        return template_id, {
            "id": template_id,
            "name_th": data.get("name_th", template_id),
            "name_en": data.get("name_en", template_id),
            "source": "upload",
            "persona_segment_count": len(data.get("persona_segments", [])),
            "crisis_scenario_count": len(data.get("crisis_scenarios", [])),
            "document_seed_count": len(data.get("document_seeds", [])),
        }

    @classmethod
    def delete_template(cls, template_id: str) -> bool:
        """Delete a user-uploaded template. Returns True if deleted."""
        filepath = os.path.join(UPLOAD_DIR, f"{template_id}.json")
        if not os.path.exists(filepath):
            return False
        os.remove(filepath)
        cls._templates.pop(template_id, None)
        logger.info(f"Deleted user template: {template_id}")
        return True

    # ── Validation ──────────────────────────────────────────

    @classmethod
    def validate_template_json(cls, data: Dict[str, Any]) -> List[str]:
        """Validate template JSON without saving. Returns list of error messages."""
        errors = []
        try:
            cls._validate_template(data)
        except TemplateValidationError as e:
            errors.append(str(e))
            return errors
        return []

    @classmethod
    def _validate_template(cls, data: Dict[str, Any]):
        """Full schema validation. Raises TemplateValidationError on failure."""
        if not isinstance(data, dict):
            raise TemplateValidationError("Template must be a JSON object")

        # Top-level required keys
        for key in REQUIRED_TOP_KEYS:
            if key not in data:
                raise TemplateValidationError(f"Missing required top-level key: '{key}'")

        if not isinstance(data.get("persona_segments"), list) or len(data["persona_segments"]) < 2:
            raise TemplateValidationError("persona_segments must be an array with at least 2 segments")

        if not isinstance(data.get("crisis_scenarios"), list) or len(data["crisis_scenarios"]) < 2:
            raise TemplateValidationError("crisis_scenarios must be an array with at least 2 scenarios")

        if not isinstance(data.get("document_seeds"), list) or len(data["document_seeds"]) < 1:
            raise TemplateValidationError("document_seeds must be an array with at least 1 seed document")

        # Validate segments
        for i, seg in enumerate(data["persona_segments"]):
            for key in REQUIRED_SEGMENT_KEYS:
                if key not in seg:
                    raise TemplateValidationError(f"Segment {i}: missing key '{key}'")
            if not isinstance(seg.get("archetypes"), list) or len(seg["archetypes"]) < 1:
                raise TemplateValidationError(f"Segment {i} ({seg.get('name_th', '?')}): must have at least 1 archetype")
            for j, arch in enumerate(seg["archetypes"]):
                for key in REQUIRED_ARCHETYPE_KEYS:
                    if key not in arch:
                        raise TemplateValidationError(f"Segment {i}, archetype {j}: missing key '{key}'")
                if arch.get("purchase_style") not in VALID_PURCHASE_STYLES:
                    raise TemplateValidationError(
                        f"Segment {i}, archetype {j}: invalid purchase_style '{arch.get('purchase_style')}'. "
                        f"Must be one of: {', '.join(sorted(VALID_PURCHASE_STYLES))}"
                    )
                if arch.get("income") not in VALID_INCOMES:
                    raise TemplateValidationError(
                        f"Segment {i}, archetype {j}: invalid income '{arch.get('income')}'. "
                        f"Must be one of: {', '.join(sorted(VALID_INCOMES))}"
                    )

        # Validate crises
        for i, crisis in enumerate(data["crisis_scenarios"]):
            for key in REQUIRED_CRISIS_KEYS:
                if key not in crisis:
                    raise TemplateValidationError(f"Crisis {i}: missing key '{key}'")
            if crisis.get("impact") not in VALID_IMPACTS:
                raise TemplateValidationError(f"Crisis {i}: invalid impact '{crisis.get('impact')}'")

        # Validate seeds
        for i, seed in enumerate(data["document_seeds"]):
            for key in REQUIRED_SEED_KEYS:
                if key not in seed:
                    raise TemplateValidationError(f"Seed {i}: missing key '{key}'")

        deep_preset = data.get("deep_preset")
        if deep_preset is not None:
            if not isinstance(deep_preset, dict):
                raise TemplateValidationError("deep_preset must be an object when provided")
            for key in REQUIRED_DEEP_PRESET_KEYS:
                if key not in deep_preset:
                    raise TemplateValidationError(f"deep_preset missing key '{key}'")
            for key in REQUIRED_DEEP_PRESET_KEYS - {"sample_brief"}:
                value = deep_preset.get(key)
                if not isinstance(value, list) or not value:
                    raise TemplateValidationError(f"deep_preset.{key} must be a non-empty array")
            if not isinstance(deep_preset.get("sample_brief"), str) or not deep_preset["sample_brief"].strip():
                raise TemplateValidationError("deep_preset.sample_brief must be a non-empty string")

        # Check ID uniqueness across segments
        all_ids = set()
        for seg in data["persona_segments"]:
            if seg["id"] in all_ids:
                raise TemplateValidationError(f"Duplicate segment id: '{seg['id']}'")
            all_ids.add(seg["id"])

        # Check ID uniqueness across archetypes
        all_arch_ids = set()
        for seg in data["persona_segments"]:
            for arch in seg["archetypes"]:
                if arch["id"] in all_arch_ids:
                    raise TemplateValidationError(f"Duplicate archetype id: '{arch['id']}'")
                all_arch_ids.add(arch["id"])

    # ── Internal ────────────────────────────────────────────

    @classmethod
    def _ensure_loaded(cls):
        if cls._loaded:
            return

        # 1. Load built-in templates
        cls._load_from_dir(BUILTIN_DIR, source="builtin")

        # 2. Load user-imported templates (override built-in with same id)
        cls._load_from_dir(UPLOAD_DIR, source="upload")

        cls._loaded = True

    @classmethod
    def _load_from_dir(cls, directory: str, source: str):
        if not os.path.isdir(directory):
            return
        for filename in sorted(os.listdir(directory)):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                tid = data.get("id", filename.replace(".json", ""))
                data["_source"] = source
                cls._templates[tid] = data
                logger.debug(f"Loaded template: {tid} (source={source}, file={filename})")
            except (json.JSONDecodeError, OSError) as e:
                logger.error(f"Failed to load template {filename}: {e}")

    @classmethod
    def invalidate(cls):
        cls._templates.clear()
        cls._loaded = False
