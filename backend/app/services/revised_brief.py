"""Deterministic revised brief generation from an action plan."""

from __future__ import annotations

from typing import Any, Dict, List


SOURCE_TYPES = {"demo_mode", "local_estimate", "live_backend", "backend_verified", "unknown"}


def _source_mode(source: Dict[str, Any] | None) -> str:
    raw = (source or {}).get("source_mode") or (source or {}).get("type") or "unknown"
    if raw == "unknown_source":
        raw = "unknown"
    return raw if raw in SOURCE_TYPES else "unknown"


def _as_list(value: Any, fallback: List[str] | None = None) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return fallback or []


def _first_text(values: List[Any], fallback: str) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def _section_items(action_plan: Dict[str, Any], key: str) -> List[Dict[str, Any]]:
    section = (action_plan.get("sections") or {}).get(key) or {}
    return section.get("items") if isinstance(section.get("items"), list) else []


def _recommendations(action_plan: Dict[str, Any], key: str) -> List[str]:
    return [
        str(item.get("recommendation") or item.get("action") or item.get("description") or "").strip()
        for item in _section_items(action_plan, key)
        if str(item.get("recommendation") or item.get("action") or item.get("description") or "").strip()
    ]


class RevisedBriefService:
    """Build a reviewable campaign brief v2 from an existing action plan."""

    def generate(
        self,
        *,
        campaign: Dict[str, Any] | None = None,
        original_brief: Dict[str, Any] | None = None,
        action_plan: Dict[str, Any] | None = None,
        evidence: Dict[str, Any] | None = None,
        source: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        campaign = campaign or {}
        original = original_brief or campaign
        plan = action_plan or {}
        evidence = evidence or {}
        source = source or plan.get("source") or {}
        provenance = self._provenance(campaign, plan, evidence, source)
        target = original.get("target") or original.get("audience") or {}

        creative = _recommendations(plan, "creative_adjustment")
        channels = _recommendations(plan, "channel_allocation")
        crisis = _recommendations(plan, "crisis_prevention")
        validation = _recommendations(plan, "validation_plan")

        revised = {
            "objective": _first_text(
                [original.get("objective"), campaign.get("objective"), "Validate a revised campaign direction before scaling spend."],
                "Validate a revised campaign direction before scaling spend.",
            ),
            "target_segments": self._target_segments(target, evidence),
            "key_message": _first_text(
                creative,
                "Lead with one concrete proof point, one audience pain point, and a clear value promise.",
            ),
            "tone_and_voice": self._tone_and_voice(original, crisis),
            "proof_points": self._proof_points(creative, evidence),
            "channel_recommendations": self._channels(target, campaign, channels),
            "risk_guardrails": self._risk_guardrails(crisis, evidence),
            "validation_plan": validation or [provenance["recommended_next_validation_step"]],
            "creative_team_notes": self._creative_notes(plan, evidence),
        }

        return {
            "version": "revised_brief_v2",
            "campaign_id": campaign.get("campaign_id") or campaign.get("id") or provenance.get("campaign_id"),
            "title": f"{_first_text([campaign.get('name'), original.get('name')], 'Campaign')} — Revised Brief v2",
            "original_brief": self._original_snapshot(original, target),
            "revised_brief": revised,
            "comparison": self._comparison(original, revised),
            "provenance": provenance,
            "disclaimer": "This revised brief is deterministic planning guidance from the action plan, not a guaranteed performance improvement.",
        }

    def _provenance(
        self,
        campaign: Dict[str, Any],
        action_plan: Dict[str, Any],
        evidence: Dict[str, Any],
        source: Dict[str, Any],
    ) -> Dict[str, Any]:
        mode = _source_mode(source)
        assumptions = (
            source.get("assumptions")
            or evidence.get("assumptions")
            or ["Action plan recommendations are translated into a brief structure deterministically."]
        )
        limitations = (
            source.get("limitations")
            or evidence.get("limitations")
            or [
                "The revised brief has not been validated with a new simulation or live audience test.",
                "Use this as a draft for review, not as a guaranteed winning creative brief.",
            ]
        )
        next_step = (
            source.get("recommended_next_validation_step")
            or evidence.get("recommended_next_validation_step")
            or "Review the revised brief with campaign, creative, legal, and research owners before running another simulation."
        )
        return {
            "source_action_plan_id": action_plan.get("id") or action_plan.get("action_plan_id"),
            "campaign_id": campaign.get("campaign_id") or campaign.get("id") or source.get("campaign_id"),
            "source_mode": mode,
            "type": mode,
            "data_basis": source.get("data_basis") or ("demo_fixture" if mode == "demo_mode" else "local_estimate" if mode == "local_estimate" else "unknown"),
            "run_id": source.get("run_id") or evidence.get("run_id"),
            "simulation_id": source.get("simulation_id") or evidence.get("simulation_id"),
            "assumptions": _as_list(assumptions),
            "limitations": _as_list(limitations),
            "recommended_next_validation_step": str(next_step),
        }

    def _target_segments(self, target: Dict[str, Any], evidence: Dict[str, Any]) -> List[str]:
        segments = _as_list(target.get("segments") or target.get("segment_name"))
        if segments:
            return segments
        evidence_segments = evidence.get("segments") or evidence.get("target_segments")
        if isinstance(evidence_segments, list):
            names = [item.get("name") if isinstance(item, dict) else item for item in evidence_segments]
            return _as_list(names, ["Primary audience segment"])
        return ["Primary audience segment"]

    def _tone_and_voice(self, original: Dict[str, Any], crisis_recommendations: List[str]) -> str:
        if crisis_recommendations:
            return "Clear, proof-led, calm, and specific. Avoid overclaiming or defensive language."
        return _first_text(
            [original.get("tone_and_voice"), original.get("tone"), original.get("voice")],
            "Confident, useful, human, and evidence-led.",
        )

    def _proof_points(self, creative_recommendations: List[str], evidence: Dict[str, Any]) -> List[str]:
        proof = _as_list(evidence.get("proof_points"))
        if proof:
            return proof
        if creative_recommendations:
            return [
                "Add proof for the lead claim.",
                "Show one audience-specific reason to believe.",
                "Use testimonials, data, certification, or product demonstration where available.",
            ]
        return ["Define proof points before creative production."]

    def _channels(self, target: Dict[str, Any], campaign: Dict[str, Any], channel_recommendations: List[str]) -> List[str]:
        if channel_recommendations:
            return channel_recommendations
        sim_config = campaign.get("sim_config") or {}
        channels = _as_list(target.get("channels") or sim_config.get("audience_channels") or campaign.get("channels"))
        return channels or ["Run a small channel split test before scaling spend."]

    def _risk_guardrails(self, crisis_recommendations: List[str], evidence: Dict[str, Any]) -> List[str]:
        drivers = _as_list(evidence.get("risk_drivers"))
        guardrails = crisis_recommendations + [f"Address risk driver: {driver}" for driver in drivers[:3]]
        return guardrails or [
            "Avoid claims that cannot be substantiated.",
            "Prepare FAQ, escalation owners, and legal review before launch.",
        ]

    def _creative_notes(self, action_plan: Dict[str, Any], evidence: Dict[str, Any]) -> List[str]:
        notes = []
        for section_key in ["creative_adjustment", "channel_allocation", "crisis_prevention"]:
            for item in _section_items(action_plan, section_key):
                reason = item.get("reason")
                risk = item.get("risk")
                if reason:
                    notes.append(f"Reason: {reason}")
                if risk:
                    notes.append(f"Watchout: {risk}")
        quotes = _as_list(evidence.get("quotes"))
        notes.extend([f"Audience cue: {quote}" for quote in quotes[:2]])
        return notes[:8] or ["Create at least two revised message routes before the next simulation."]

    def _original_snapshot(self, original: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "objective": original.get("objective", ""),
            "description": original.get("description", ""),
            "target_segments": self._target_segments(target, {}),
            "channels": _as_list(target.get("channels") or original.get("channels")),
            "constraints": _as_list(original.get("brand_constraints") or original.get("constraints")),
        }

    def _comparison(self, original: Dict[str, Any], revised: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "objective": {
                "v1": original.get("objective", ""),
                "v2": revised["objective"],
            },
            "key_message": {
                "v1": original.get("key_message") or original.get("description", ""),
                "v2": revised["key_message"],
            },
            "risk_guardrails": {
                "v1": _as_list(original.get("risk_guardrails") or original.get("risk_notes")),
                "v2": revised["risk_guardrails"],
            },
            "validation_plan": {
                "v1": _as_list(original.get("validation_plan")),
                "v2": revised["validation_plan"],
            },
        }
