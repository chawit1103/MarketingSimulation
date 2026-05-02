import json
from pathlib import Path
import sys


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.services.industry_templates import (  # noqa: E402
    REQUIRED_DEEP_PRESET_KEYS,
    IndustryTemplateLoader,
)


TEMPLATE_DIR = BACKEND_DIR / "app" / "services" / "industry_templates"
PRIORITY_TEMPLATE_IDS = {
    "fmcg_cpg",
    "insurance_insurtech",
    "retail_ecommerce",
    "real_estate",
    "ev_automotive",
    "healthcare_wellness",
}


def _load_template(template_id: str) -> dict:
    return json.loads((TEMPLATE_DIR / f"{template_id}.json").read_text(encoding="utf-8"))


def test_priority_deep_industry_presets_are_listed():
    IndustryTemplateLoader.invalidate()
    templates = IndustryTemplateLoader.list_templates()
    listed_ids = {template["id"] for template in templates}

    assert PRIORITY_TEMPLATE_IDS.issubset(listed_ids)
    for template in templates:
        if template["id"] in PRIORITY_TEMPLATE_IDS:
            assert template["industry_depth"] == "deep_preset"
            assert template["assumptions"]
            assert template["limitations"]


def test_priority_deep_industry_presets_pass_template_validation():
    for template_id in PRIORITY_TEMPLATE_IDS:
        template = _load_template(template_id)
        errors = IndustryTemplateLoader.validate_template_json(template)

        assert errors == []
        assert set(template["deep_preset"]) >= REQUIRED_DEEP_PRESET_KEYS
        assert len(template["persona_segments"]) >= 2
        assert len(template["crisis_scenarios"]) >= 2
        assert template["deep_preset"]["assumptions"]
        assert template["deep_preset"]["limitations"]


def test_campaign_preset_exposes_deep_prefill_and_provenance_safe_fields():
    IndustryTemplateLoader.invalidate()
    preset = IndustryTemplateLoader.build_campaign_preset("fmcg_cpg")

    assert preset["template_id"] == "fmcg_cpg"
    assert preset["industry_depth"] == "deep_preset"
    assert preset["campaign_duration"]
    assert preset["budget_range"]
    assert preset["primary_kpi"]
    assert preset["competitor_context"]
    assert preset["brand_constraints"]
    assert preset["risk_legal_notes"]
    assert preset["deep_preset"]["sample_brief"]
    assert preset["deep_preset"]["sample_risk_checklist"]
    assert preset["document_seeds"][0]["name_en"]
    assert preset["document_seeds"][0]["description_en"]


def test_deep_preset_schema_rejects_incomplete_deep_preset():
    template = _load_template("retail_ecommerce")
    template["deep_preset"].pop("proof_point_requirements")

    errors = IndustryTemplateLoader.validate_template_json(template)

    assert errors
    assert "deep_preset missing key 'proof_point_requirements'" in errors[0]


def test_healthcare_wellness_preset_uses_conservative_non_predictive_language():
    template = _load_template("healthcare_wellness")
    serialized = json.dumps(template, ensure_ascii=False).lower()

    prohibited_claims = [
        "guaranteed outcome",
        "guaranteed cure",
        "cure disease",
        "replace doctor",
    ]

    for phrase in prohibited_claims:
        assert phrase not in serialized
    assert "qualified professional" in serialized
    assert "does not provide medical" in serialized
