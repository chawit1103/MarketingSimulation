"""Structured action plan generation for simulation dashboards.

The service is deterministic and intentionally conservative. It translates
available KPI, segment, evidence, and source metadata into action items that are
useful for planning, while avoiding claims that the recommendations are
guaranteed predictions.
"""

from __future__ import annotations

from typing import Any, Dict, List


SOURCE_TYPES = {"demo_mode", "local_estimate", "live_backend", "backend_verified", "unknown"}


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _crisis_score(value: Any) -> float:
    if isinstance(value, str):
        return {"low": 18.0, "medium": 48.0, "high": 78.0}.get(value.lower(), 35.0)
    return max(0.0, min(100.0, _number(value, 35.0)))


def _source_type(source: Dict[str, Any] | None) -> str:
    value = (source or {}).get("type") or "unknown"
    return value if value in SOURCE_TYPES else "unknown"


def _top_segment(segments: List[Dict[str, Any]], reverse: bool) -> Dict[str, Any]:
    if not segments:
        return {}

    def sentiment(row: Dict[str, Any]) -> float:
        return _number(row.get("sentiment", row.get("avg_sentiment")), 0.0)

    return sorted(segments, key=sentiment, reverse=reverse)[0]


class ActionPlanService:
    """Build structured action plans with sectioned recommendation items."""

    SECTION_ORDER = [
        "creative_adjustment",
        "channel_allocation",
        "crisis_prevention",
        "validation_plan",
    ]

    def generate(
        self,
        *,
        campaign: Dict[str, Any] | None = None,
        kpis: Dict[str, Any] | None = None,
        segments: List[Dict[str, Any]] | None = None,
        evidence: Dict[str, Any] | None = None,
        source: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        campaign = campaign or {}
        kpis = kpis or {}
        segments = segments or []
        evidence = evidence or {}
        source_type = _source_type(source)

        conversion = _number(kpis.get("conversion_probability"), 0.0)
        sentiment = _number(kpis.get("overall_sentiment"), 0.0)
        resonance = _number(kpis.get("message_resonance"), 0.0)
        crisis = _crisis_score(kpis.get("crisis_risk"))
        social = _number(kpis.get("social_influence", kpis.get("social_influence_index")), 0.0)
        confidence = _number(evidence.get("confidence_score", kpis.get("confidence_score")), 0.0)
        positive_segment = _top_segment(segments, reverse=True)
        risk_segment = _top_segment(segments, reverse=False)

        sections = {
            "creative_adjustment": {
                "title": "Creative Adjustment",
                "items": [
                    self._creative_item(resonance, sentiment, positive_segment, evidence),
                ],
            },
            "channel_allocation": {
                "title": "Channel Allocation",
                "items": [
                    self._channel_item(conversion, social, campaign, positive_segment),
                ],
            },
            "crisis_prevention": {
                "title": "Crisis Prevention",
                "items": [
                    self._crisis_item(crisis, risk_segment, evidence),
                ],
            },
            "validation_plan": {
                "title": "Validation Plan",
                "items": [
                    self._validation_item(confidence, source_type, campaign),
                ],
            },
        }

        headline = self._headline(conversion, crisis, resonance)
        return {
            "version": "structured_action_plan_v1",
            "source": {
                "type": source_type,
                "warning": (source or {}).get("warning", ""),
            },
            "headline": headline,
            "disclaimer": "Recommendations are deterministic planning guidance, not guaranteed market predictions.",
            "sections": sections,
            "summary_items": [
                sections[key]["items"][0]
                for key in self.SECTION_ORDER
            ],
        }

    def _creative_item(
        self,
        resonance: float,
        sentiment: float,
        positive_segment: Dict[str, Any],
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        segment = positive_segment.get("name") or positive_segment.get("segment_name") or "the strongest positive segment"
        proof_gap = (evidence.get("risk_drivers") or ["proof points are not explicit enough"])[0]
        if resonance >= 70 and sentiment >= 20:
            recommendation = "Keep the core message, but add proof cards and segment-specific variants."
            impact = "Preserves current resonance while reducing interpretation risk."
            risk = "Over-expanding creative variants may dilute the winning claim."
        else:
            recommendation = "Rewrite the lead claim around one concrete proof point and one audience pain point."
            impact = "Should improve message clarity before additional media spend."
            risk = "If proof is weak or generic, skeptical segments may react more negatively."
        return {
            "recommendation": recommendation,
            "reason": f"Message resonance is {resonance:.0f}% and strongest response comes from {segment}; key gap: {proof_gap}.",
            "expected_impact": impact,
            "risk": risk,
            "priority": "high" if resonance < 70 else "medium",
        }

    def _channel_item(
        self,
        conversion: float,
        social: float,
        campaign: Dict[str, Any],
        positive_segment: Dict[str, Any],
    ) -> Dict[str, Any]:
        channels = (
            (campaign.get("target") or {}).get("channels")
            or (campaign.get("audience") or {}).get("channels")
            or (campaign.get("sim_config") or {}).get("audience_channels")
            or ["highest-response social channels"]
        )
        top_channels = ", ".join(str(item) for item in channels[:3])
        segment = positive_segment.get("name") or positive_segment.get("segment_name") or "the best-responding segment"
        if conversion >= 65 and social >= 60:
            recommendation = f"Shift incremental budget toward {top_channels} and retarget {segment}."
            impact = "Improves efficiency by concentrating spend where response and influence are already visible."
            risk = "May under-serve slower-building channels if moved too aggressively."
        else:
            recommendation = f"Run a small channel split test across {top_channels} before scaling."
            impact = "Finds the least risky channel mix before committing full spend."
            risk = "Short tests can miss delayed conversion or offline effects."
        return {
            "recommendation": recommendation,
            "reason": f"Conversion is {conversion:.0f}% and social influence is {social:.0f}/100.",
            "expected_impact": impact,
            "risk": risk,
            "priority": "high" if conversion >= 65 else "medium",
        }

    def _crisis_item(
        self,
        crisis: float,
        risk_segment: Dict[str, Any],
        evidence: Dict[str, Any],
    ) -> Dict[str, Any]:
        segment = risk_segment.get("name") or risk_segment.get("segment_name") or "the highest-risk audience"
        risk_driver = (evidence.get("risk_drivers") or [f"{segment} may amplify unresolved objections"])[0]
        if crisis >= 60:
            recommendation = "Pause broad launch until risky claims, FAQ, and escalation owners are approved."
            impact = "Reduces the probability of a preventable launch-day backlash."
            risk = "Delays speed-to-market and may give competitors more response time."
            priority = "critical"
        else:
            recommendation = "Prepare a lightweight response pack before scaling the strongest variant."
            impact = "Keeps momentum while adding guardrails for negative interpretation."
            risk = "A lightweight pack may be insufficient if the issue becomes regulatory or influencer-led."
            priority = "medium"
        return {
            "recommendation": recommendation,
            "reason": f"Crisis risk is {crisis:.0f}/100; primary driver: {risk_driver}.",
            "expected_impact": impact,
            "risk": risk,
            "priority": priority,
        }

    def _validation_item(
        self,
        confidence: float,
        source_type: str,
        campaign: Dict[str, Any],
    ) -> Dict[str, Any]:
        objective = campaign.get("objective") or "campaign decision"
        if source_type in {"demo_mode", "local_estimate", "unknown"}:
            recommendation = "Validate this plan with a backend run or controlled audience test before budget approval."
            impact = "Separates demo/local planning signals from evidence suitable for business approval."
            risk = "Skipping validation can turn directional guidance into overconfident execution."
        else:
            recommendation = "Run one live-market or audience holdout test against the highest-priority action."
            impact = "Checks whether simulated direction survives contact with real audience behavior."
            risk = "Small samples may under-detect slow-building trust or crisis effects."
        return {
            "recommendation": recommendation,
            "reason": f"Source mode is {source_type}; confidence signal is {confidence:.0f}/100 for {objective}.",
            "expected_impact": impact,
            "risk": risk,
            "priority": "high" if source_type in {"demo_mode", "local_estimate", "unknown"} else "medium",
        }

    def _headline(self, conversion: float, crisis: float, resonance: float) -> str:
        if crisis >= 60:
            return "Revise and de-risk before launch."
        if conversion >= 65 and resonance >= 65:
            return "Launch with guardrails and validation."
        return "Pilot the revised message before scaling."
