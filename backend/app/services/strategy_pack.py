"""Client-ready strategy pack export builder.

This service turns existing simulation/dashboard payloads into a structured
meeting pack. It is deterministic and provenance-first: every section carries
the same source metadata so demo/local outputs are never presented as verified
simulation evidence.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List


SOURCE_TYPES = {"demo_mode", "local_estimate", "live_backend", "backend_verified", "unknown"}
MODE_ALIASES = {
    "brand": "brand_executive_summary",
    "brand_executive": "brand_executive_summary",
    "brand_executive_summary": "brand_executive_summary",
    "agency": "agency_client_pitch_summary",
    "agency_pitch": "agency_client_pitch_summary",
    "agency_client_pitch_summary": "agency_client_pitch_summary",
}


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_text(values: List[Any], fallback: str) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def _source_mode(source: Dict[str, Any] | None) -> str:
    raw = (source or {}).get("source_mode") or (source or {}).get("type") or "unknown"
    if raw == "unknown_source":
        raw = "unknown"
    return raw if raw in SOURCE_TYPES else "unknown"


def _data_basis(source_mode: str, source: Dict[str, Any] | None) -> str:
    explicit = (source or {}).get("data_basis")
    if explicit:
        return str(explicit)
    return {
        "demo_mode": "demo_fixture",
        "local_estimate": "local_estimate",
        "live_backend": "backend_generated",
        "backend_verified": "real_simulation",
        "unknown": "unknown",
    }.get(source_mode, "unknown")


def _confidence_level(source: Dict[str, Any] | None, evidence: Dict[str, Any], kpis: Dict[str, Any]) -> str:
    explicit = (source or {}).get("confidence_level") or evidence.get("confidence_level")
    if explicit:
        return str(explicit)

    score = evidence.get("confidence_score", kpis.get("confidence_score"))
    if score is None:
        return "unknown"
    numeric = _number(score, -1)
    if numeric >= 80:
        return "high"
    if numeric >= 55:
        return "medium"
    if numeric >= 0:
        return "low"
    return "unknown"


def _segment_name(segment: Dict[str, Any]) -> str:
    return str(segment.get("name") or segment.get("segment_name") or segment.get("label") or "Audience segment")


def _sentiment(segment: Dict[str, Any]) -> float:
    return _number(segment.get("sentiment", segment.get("avg_sentiment")), 0.0)


def _risk_score(value: Any) -> float:
    if isinstance(value, str):
        return {"low": 18.0, "medium": 48.0, "high": 78.0, "critical": 88.0}.get(value.lower(), 35.0)
    return max(0.0, min(100.0, _number(value, 35.0)))


class StrategyPackService:
    """Build a client-ready strategy pack for brand or agency meetings."""

    SECTION_KEYS = [
        "executive_decision_summary",
        "launch_recommendation",
        "kpi_summary",
        "segment_reactions",
        "risk_drivers",
        "crisis_watchouts",
        "recommended_action_plan",
        "next_validation_steps",
    ]

    def build(self, payload: Dict[str, Any] | None) -> Dict[str, Any]:
        payload = payload or {}
        mode = self._mode(payload.get("mode"))
        campaign = payload.get("campaign") or {}
        kpis = payload.get("kpis") or payload.get("metrics") or {}
        segments = payload.get("segments") or []
        evidence = payload.get("evidence") or {}
        action_plan = payload.get("action_plan") or {}
        source = payload.get("source") or action_plan.get("source") or {}
        provenance = self._provenance(source, evidence, kpis, campaign)

        sections = {
            "executive_decision_summary": self._section(
                "Executive Decision Summary",
                self._executive_summary(mode, campaign, kpis, provenance),
                self._executive_items(mode, campaign, kpis, provenance),
                provenance,
            ),
            "launch_recommendation": self._section(
                "Launch / Revise / Do-Not-Launch Recommendation",
                "Decision guidance for the next campaign gate.",
                [self._launch_recommendation(kpis, provenance, payload.get("recommendation"))],
                provenance,
            ),
            "kpi_summary": self._section(
                "KPI Summary",
                "Key planning signals from the submitted result payload.",
                self._kpi_items(kpis),
                provenance,
            ),
            "segment_reactions": self._section(
                "Segment Reactions",
                "Audience groups that appear strongest or riskiest in the current result.",
                self._segment_items(segments),
                provenance,
            ),
            "risk_drivers": self._section(
                "Risk Drivers",
                "Issues that should be resolved before scaling spend.",
                self._risk_items(evidence, kpis),
                provenance,
            ),
            "crisis_watchouts": self._section(
                "Crisis Watchouts",
                "Signals that need monitoring if the campaign moves forward.",
                self._crisis_items(evidence, kpis),
                provenance,
            ),
            "recommended_action_plan": self._section(
                "Recommended Action Plan",
                "Structured actions for creative, channels, crisis prevention, and validation.",
                self._action_items(action_plan, provenance),
                provenance,
            ),
            "next_validation_steps": self._section(
                "Next Validation Steps",
                provenance["recommended_next_validation_step"],
                self._validation_items(provenance),
                provenance,
            ),
        }

        return {
            "version": "strategy_pack_v1",
            "mode": mode,
            "mode_label": self._mode_label(mode),
            "audience": "brand_leadership" if mode == "brand_executive_summary" else "agency_client_team",
            "white_label": self._white_label(payload, campaign),
            "source": provenance,
            "sections": sections,
            "section_order": self.SECTION_KEYS,
            "disclaimer": "This strategy pack is decision-support scenario planning, not a guaranteed market prediction.",
        }

    def _mode(self, value: Any) -> str:
        return MODE_ALIASES.get(str(value or "").strip().lower(), "brand_executive_summary")

    def _mode_label(self, mode: str) -> str:
        if mode == "agency_client_pitch_summary":
            return "Agency Client Pitch Summary"
        return "Brand Executive Summary"

    def _white_label(self, payload: Dict[str, Any], campaign: Dict[str, Any]) -> Dict[str, Any]:
        metadata = payload.get("metadata") or payload.get("report_metadata") or {}
        logo_url_present = bool(metadata.get("logo_url") or payload.get("logo_url"))
        return {
            "agency_name": _first_text([metadata.get("agency_name"), payload.get("agency_name")], ""),
            "client_name": _first_text([metadata.get("client_name"), payload.get("client_name")], ""),
            "prepared_by": _first_text([metadata.get("prepared_by"), payload.get("prepared_by")], ""),
            "report_date": _first_text([metadata.get("report_date"), payload.get("report_date")], date.today().isoformat()),
            "campaign_name": _first_text(
                [
                    metadata.get("campaign_name"),
                    payload.get("campaign_name"),
                    campaign.get("name"),
                    campaign.get("campaign_name"),
                ],
                "Untitled campaign",
            ),
            "scenario_name": _first_text([metadata.get("scenario_name"), payload.get("scenario_name")], ""),
            "logo_placeholder": bool(metadata.get("logo_placeholder", True) or logo_url_present),
            "logo_url_present": logo_url_present,
        }

    def _provenance(
        self,
        source: Dict[str, Any] | None,
        evidence: Dict[str, Any],
        kpis: Dict[str, Any],
        campaign: Dict[str, Any],
    ) -> Dict[str, Any]:
        mode = _source_mode(source)
        assumptions = (source or {}).get("assumptions") or evidence.get("assumptions") or [
            "Inputs are interpreted as planning signals, not observed market outcomes.",
        ]
        limitations = (source or {}).get("limitations") or evidence.get("limitations") or [
            "Results need validation with audience data, live tests, or verified simulation runs before budget approval.",
        ]
        next_step = (
            (source or {}).get("recommended_next_validation_step")
            or evidence.get("recommended_next_validation_step")
            or campaign.get("next_validation_step")
            or self._default_validation_step(mode)
        )
        return {
            "type": mode,
            "source_mode": mode,
            "data_basis": _data_basis(mode, source),
            "run_id": (source or {}).get("run_id") or evidence.get("run_id"),
            "campaign_id": campaign.get("campaign_id") or campaign.get("id") or (source or {}).get("campaign_id"),
            "simulation_id": (source or {}).get("simulation_id") or evidence.get("simulation_id"),
            "confidence_level": _confidence_level(source, evidence, kpis),
            "assumptions": assumptions if isinstance(assumptions, list) else [str(assumptions)],
            "limitations": limitations if isinstance(limitations, list) else [str(limitations)],
            "recommended_next_validation_step": str(next_step),
        }

    def _default_validation_step(self, source_mode: str) -> str:
        if source_mode in {"demo_mode", "local_estimate", "unknown"}:
            return "Run a backend simulation or controlled audience test before treating this as decision evidence."
        return "Validate the recommendation with a small audience holdout or launch-readiness review."

    def _section(
        self,
        title: str,
        summary: str,
        items: List[Dict[str, Any]],
        provenance: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "title": title,
            "summary": summary,
            "items": items,
            "provenance": provenance.copy(),
        }

    def _executive_summary(
        self,
        mode: str,
        campaign: Dict[str, Any],
        kpis: Dict[str, Any],
        provenance: Dict[str, Any],
    ) -> str:
        name = campaign.get("name") or campaign.get("campaign_name") or "this campaign"
        audience = "leadership decision review" if mode == "brand_executive_summary" else "client pitch discussion"
        crisis = _risk_score(kpis.get("crisis_risk"))
        sentiment = _number(kpis.get("overall_sentiment"), 0.0)
        return (
            f"{name} is packaged for {audience}. Current source is {provenance['source_mode']} "
            f"with {provenance['data_basis']} basis, sentiment {sentiment:.0f}, and crisis risk {crisis:.0f}/100."
        )

    def _executive_items(
        self,
        mode: str,
        campaign: Dict[str, Any],
        kpis: Dict[str, Any],
        provenance: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        objective = campaign.get("objective") or "campaign decision"
        framing = (
            "Use this pack to align leadership on a launch gate."
            if mode == "brand_executive_summary"
            else "Use this pack to explain the recommended route and evidence gaps to the client."
        )
        return [
            {
                "recommendation": framing,
                "reason": f"Objective: {objective}. Source mode: {provenance['source_mode']}.",
                "expected_impact": "Improves decision clarity before spend is committed.",
                "risk": "Over-reliance without validation can turn planning guidance into false certainty.",
            },
            self._launch_recommendation(kpis, provenance, None),
        ]

    def _launch_recommendation(
        self,
        kpis: Dict[str, Any],
        provenance: Dict[str, Any],
        provided: Any,
    ) -> Dict[str, Any]:
        if isinstance(provided, dict):
            recommendation = str(provided.get("recommendation") or provided.get("decision") or "")
            reason = str(provided.get("reason") or provided.get("rationale") or "")
            if recommendation:
                return {
                    "recommendation": recommendation,
                    "reason": reason or "Recommendation was provided by the upstream result.",
                    "expected_impact": str(provided.get("expected_impact") or "Clarifies the next campaign decision."),
                    "risk": str(provided.get("risk") or "Needs validation before final budget commitment."),
                }
        if isinstance(provided, str) and provided.strip():
            return {
                "recommendation": provided.strip(),
                "reason": "Recommendation was provided by the upstream result.",
                "expected_impact": "Clarifies the next campaign decision.",
                "risk": "Needs validation before final budget commitment.",
            }

        crisis = _risk_score(kpis.get("crisis_risk"))
        conversion = _number(kpis.get("conversion_probability"), 0.0)
        sentiment = _number(kpis.get("overall_sentiment"), 0.0)
        cautious_source = provenance["source_mode"] in {"demo_mode", "local_estimate", "unknown"}

        if crisis >= 70 or sentiment < -20:
            decision = "Do not launch until core risks are resolved."
            reason = f"Crisis risk is {crisis:.0f}/100 and sentiment is {sentiment:.0f}."
        elif crisis >= 45 or conversion < 45 or cautious_source:
            decision = "Revise before launch and validate with a controlled test."
            reason = f"Conversion is {conversion:.0f}%, crisis risk is {crisis:.0f}/100, source is {provenance['source_mode']}."
        else:
            decision = "Launch with guardrails and a validation checkpoint."
            reason = f"Conversion is {conversion:.0f}% and crisis risk is {crisis:.0f}/100."

        return {
            "recommendation": decision,
            "reason": reason,
            "expected_impact": "Supports a clearer go/no-go decision without claiming guaranteed outcomes.",
            "risk": "The decision can change if real audience or operational data contradicts the simulation.",
        }

    def _kpi_items(self, kpis: Dict[str, Any]) -> List[Dict[str, Any]]:
        fields = [
            ("overall_sentiment", "Overall sentiment", ""),
            ("conversion_probability", "Conversion probability", "%"),
            ("message_resonance", "Message resonance", "%"),
            ("crisis_risk", "Crisis risk", "/100"),
            ("brand_perception_shift", "Brand perception shift", ""),
            ("opinion_polarization", "Opinion polarization", "/100"),
        ]
        items = []
        for key, label, unit in fields:
            if key in kpis:
                items.append({
                    "metric": label,
                    "value": kpis.get(key),
                    "unit": unit,
                    "interpretation": self._kpi_interpretation(key, kpis.get(key)),
                })
        return items or [{
            "metric": "KPI summary",
            "value": "not available",
            "unit": "",
            "interpretation": "No KPI payload was provided for this export.",
        }]

    def _kpi_interpretation(self, key: str, value: Any) -> str:
        numeric = _risk_score(value) if key == "crisis_risk" else _number(value, 0.0)
        if key == "crisis_risk":
            return "High risk requires response planning." if numeric >= 60 else "Risk appears manageable with guardrails."
        if key == "conversion_probability":
            return "Scale only after validation." if numeric < 55 else "Commercial signal is directionally positive."
        if key == "overall_sentiment":
            return "Message may face resistance." if numeric < 0 else "Audience tone is directionally positive."
        return "Use as a planning signal and validate before budget commitment."

    def _segment_items(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not segments:
            return [{
                "segment": "not available",
                "reaction": "Segment-level reactions were not provided.",
                "recommended_focus": "Run a segmented simulation or audience test before final targeting.",
            }]
        ordered = sorted(segments, key=_sentiment)
        risk = ordered[0]
        positive = ordered[-1]
        return [
            {
                "segment": _segment_name(positive),
                "reaction": f"Strongest positive signal, sentiment {_sentiment(positive):.0f}.",
                "recommended_focus": "Use this segment to refine proof points and channel allocation.",
            },
            {
                "segment": _segment_name(risk),
                "reaction": f"Highest resistance signal, sentiment {_sentiment(risk):.0f}.",
                "recommended_focus": "Address objections before scaling broad launch spend.",
            },
        ]

    def _risk_items(self, evidence: Dict[str, Any], kpis: Dict[str, Any]) -> List[Dict[str, Any]]:
        drivers = evidence.get("risk_drivers") or []
        if not drivers:
            drivers = [f"Crisis risk score: {_risk_score(kpis.get('crisis_risk')):.0f}/100."]
        return [
            {
                "driver": str(driver),
                "recommended_response": "Resolve the driver with clearer proof, claims review, or response ownership.",
            }
            for driver in drivers[:5]
        ]

    def _crisis_items(self, evidence: Dict[str, Any], kpis: Dict[str, Any]) -> List[Dict[str, Any]]:
        watchouts = evidence.get("crisis_watchouts") or evidence.get("watchouts") or []
        if not watchouts:
            crisis = _risk_score(kpis.get("crisis_risk"))
            watchouts = [
                "Monitor creator/influencer amplification." if crisis >= 50 else "Monitor early comments for recurring objections.",
                "Prepare claims, FAQ, and escalation owner before launch.",
            ]
        return [
            {
                "watchout": str(item),
                "owner_hint": "Assign PR, legal, or campaign owner before launch review.",
            }
            for item in watchouts[:5]
        ]

    def _action_items(self, action_plan: Dict[str, Any], provenance: Dict[str, Any]) -> List[Dict[str, Any]]:
        sections = action_plan.get("sections") or {}
        if not sections:
            return [{
                "section": "Validation Plan",
                "recommendation": provenance["recommended_next_validation_step"],
                "reason": "No structured action plan payload was provided.",
                "expected_impact": "Prevents over-committing to unvalidated guidance.",
                "risk": "Skipping validation can create false confidence.",
            }]

        items: List[Dict[str, Any]] = []
        for section_key, section in sections.items():
            title = section.get("title") or section_key.replace("_", " ").title()
            for item in section.get("items", [])[:2]:
                items.append({
                    "section": title,
                    "recommendation": item.get("recommendation", ""),
                    "reason": item.get("reason", ""),
                    "expected_impact": item.get("expected_impact", ""),
                    "risk": item.get("risk", ""),
                })
        return items or [{
            "section": "Validation Plan",
            "recommendation": provenance["recommended_next_validation_step"],
            "reason": "Action plan sections were empty.",
            "expected_impact": "Keeps the next decision grounded in evidence.",
            "risk": "Empty action plans are not sufficient for approval.",
        }]

    def _validation_items(self, provenance: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "step": provenance["recommended_next_validation_step"],
                "reason": f"Current source mode is {provenance['source_mode']} with {provenance['data_basis']} basis.",
                "expected_impact": "Improves trust in the recommendation before launch or client approval.",
                "risk": "Decision quality remains limited if validation is skipped.",
            }
        ]
