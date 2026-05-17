import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402
from app.config import Config  # noqa: E402
from app.services.revised_brief import RevisedBriefService  # noqa: E402


def _payload():
    return {
        "campaign": {
            "campaign_id": "cmp_demo",
            "name": "Premium Water Launch",
            "objective": "product_launch",
            "description": "Launch a premium hydration product.",
            "target": {
                "segment_name": "Urban health buyers",
                "channels": ["instagram", "tiktok", "facebook"],
            },
        },
        "action_plan": {
            "id": "ap_demo",
            "source": {
                "type": "demo_mode",
                "source_mode": "demo_mode",
                "data_basis": "demo_fixture",
                "campaign_id": "cmp_demo",
                "recommended_next_validation_step": "Run a proof-led concept test.",
            },
            "sections": {
                "creative_adjustment": {
                    "items": [
                        {
                            "recommendation": "Rewrite the lead claim around hydration proof and premium taste.",
                            "reason": "Proof-seeking buyers need a concrete reason to believe.",
                            "risk": "Generic proof may feel like health overclaiming.",
                        }
                    ]
                },
                "channel_allocation": {
                    "items": [
                        {
                            "recommendation": "Test TikTok creator proof videos and Instagram proof cards.",
                        }
                    ]
                },
                "crisis_prevention": {
                    "items": [
                        {
                            "recommendation": "Prepare claim substantiation and price FAQ before launch.",
                        }
                    ]
                },
                "validation_plan": {
                    "items": [
                        {
                            "recommendation": "Run a 2-cell audience test before media scale.",
                        }
                    ]
                },
            },
        },
        "evidence": {
            "assumptions": ["Synthetic demo evidence."],
            "limitations": ["Not a live market test."],
            "risk_drivers": ["Premium price sensitivity."],
            "quotes": ["I need proof before paying more."],
        },
    }


def test_revised_brief_generation_has_required_sections_and_provenance():
    result = RevisedBriefService().generate(**_payload())
    revised = result["revised_brief"]

    assert result["version"] == "revised_brief_v2"
    assert result["campaign_id"] == "cmp_demo"
    assert revised["objective"]
    assert revised["target_segments"] == ["Urban health buyers"]
    assert revised["key_message"].startswith("Rewrite the lead claim")
    assert revised["tone_and_voice"]
    assert revised["proof_points"]
    assert revised["channel_recommendations"]
    assert revised["risk_guardrails"]
    assert revised["validation_plan"]
    assert revised["creative_team_notes"]
    assert result["comparison"]["key_message"]["v2"] == revised["key_message"]
    assert result["provenance"]["source_action_plan_id"] == "ap_demo"
    assert result["provenance"]["source_mode"] == "demo_mode"
    assert result["provenance"]["data_basis"] == "demo_fixture"
    assert result["provenance"]["assumptions"]
    assert result["provenance"]["limitations"]
    assert result["provenance"]["recommended_next_validation_step"] == "Run a proof-led concept test."
    assert "guaranteed" in result["disclaimer"]


def test_revised_brief_endpoint_returns_safe_contract(monkeypatch):
    monkeypatch.setattr(Config, "RATE_LIMIT_ENABLED", False)
    app = create_app()
    app.config.update(TESTING=True)

    response = app.test_client().post("/api/brief/revise", json=_payload())
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["success"] is True
    assert payload["data"]["version"] == "revised_brief_v2"
    assert payload["data"]["provenance"]["source_mode"] == "demo_mode"
    assert "traceback" not in str(payload).lower()
