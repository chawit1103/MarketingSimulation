"""Deterministic decision engine for campaign strategy recommendations.

The goal is to translate simulation KPIs into business decisions without
depending on an LLM. This gives the product a consistent, auditable decision
layer that can later be calibrated with real outcomes.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _crisis_score(value: Any) -> float:
    if isinstance(value, str):
        mapping = {"low": 18, "medium": 48, "high": 78}
        return float(mapping.get(value.lower(), 35))
    return _clamp(_number(value, 35))


def _severity(score: float) -> str:
    if score >= 70:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def _kpis(data: Dict[str, Any]) -> Dict[str, float]:
    return {
        "overall_sentiment": _number(data.get("overall_sentiment"), 0),
        "conversion_probability": _clamp(_number(data.get("conversion_probability"), 0)),
        "social_influence": _clamp(_number(data.get("social_influence", data.get("social_influence_index")), 0)),
        "message_resonance": _clamp(_number(data.get("message_resonance"), 0)),
        "crisis_risk": _crisis_score(data.get("crisis_risk")),
        "brand_perception_shift": _number(data.get("brand_perception_shift"), 0),
        "opinion_polarization": _clamp(_number(data.get("opinion_polarization"), 0)),
    }


class DecisionEngine:
    """Convert simulation output into strategy, business impact, and what-if deltas."""

    DEFAULT_BUSINESS = {
        "market_size": 100000,
        "unit_price": 120,
        "current_market_share": 12,
        "base_conversion_rate": 4,
        "campaign_budget": 500000,
        "crisis_response_cost": 1500000,
    }

    def analyze(
        self,
        campaign: Dict[str, Any] | None,
        kpis: Dict[str, Any],
        segments: List[Dict[str, Any]] | None = None,
        evidence: Dict[str, Any] | None = None,
        business_params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        metrics = _kpis(kpis or {})
        segments = segments or []
        evidence = evidence or {}
        business = {**self.DEFAULT_BUSINESS, **(business_params or {})}

        top_positive = self._top_segment(segments, reverse=True)
        top_negative = self._top_segment(segments, reverse=False)
        business_impact = self._business_impact(metrics, business)
        risk = self._primary_risk(metrics, top_negative, evidence)
        strategy = self._strategy(metrics, top_positive, risk)

        return {
            "recommended_strategy": strategy,
            "business_impact": business_impact,
            "business_mapping": self._business_mapping(metrics, business_impact),
            "top_positive_segment": top_positive,
            "top_risk_segment": top_negative,
            "primary_risk": risk,
            "actions": self._actions(metrics, risk, top_positive, top_negative),
            "audit": {
                "method": "deterministic_rule_engine_v1",
                "inputs": ["kpis", "segments", "evidence", "business_params"],
                "confidence_basis": "message resonance, segment spread, crisis risk, and evidence coverage",
            },
        }

    def simulate_what_if(
        self,
        kpis: Dict[str, Any],
        scenario: Dict[str, Any],
        business_params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        base = _kpis(kpis or {})
        adjusted = deepcopy(base)
        business = {**self.DEFAULT_BUSINESS, **(business_params or {})}

        price_discount = _number(scenario.get("price_discount_pct"), 0)
        price_increase = _number(scenario.get("price_increase_pct"), 0)
        proof_points = bool(scenario.get("proof_points"))
        testimonials = bool(scenario.get("testimonials"))
        competitor_launch = bool(scenario.get("competitor_launch"))
        budget_increase = _number(scenario.get("budget_increase_pct"), 0)

        if price_discount:
            adjusted["conversion_probability"] += min(price_discount * 0.65, 10)
            adjusted["crisis_risk"] -= min(price_discount * 0.35, 6)
            adjusted["brand_perception_shift"] -= min(price_discount * 0.12, 3)
        if price_increase:
            adjusted["conversion_probability"] -= min(price_increase * 0.7, 12)
            adjusted["crisis_risk"] += min(price_increase * 0.8, 15)
        if proof_points:
            adjusted["message_resonance"] += 8
            adjusted["crisis_risk"] -= 9
            adjusted["overall_sentiment"] += 4
        if testimonials:
            adjusted["conversion_probability"] += 5
            adjusted["overall_sentiment"] += 5
            adjusted["social_influence"] += 4
        if competitor_launch:
            adjusted["conversion_probability"] -= 7
            adjusted["social_influence"] -= 5
            adjusted["crisis_risk"] += 8
            adjusted["brand_perception_shift"] -= 4
        if budget_increase:
            adjusted["social_influence"] += min(budget_increase * 0.18, 12)
            adjusted["conversion_probability"] += min(budget_increase * 0.08, 5)

        adjusted = {
            key: round(_clamp(value) if key != "overall_sentiment" and key != "brand_perception_shift" else max(-100, min(100, value)), 1)
            for key, value in adjusted.items()
        }

        return {
            "scenario": scenario,
            "base_kpis": base,
            "adjusted_kpis": adjusted,
            "delta": {key: round(adjusted[key] - base[key], 1) for key in adjusted},
            "decision": self._strategy(adjusted, {}, self._primary_risk(adjusted, {}, {})),
            "business_impact": self._business_impact(adjusted, business),
        }

    def _strategy(self, metrics: Dict[str, float], top_positive: Dict[str, Any], risk: Dict[str, Any]) -> Dict[str, Any]:
        conversion = metrics["conversion_probability"]
        crisis = metrics["crisis_risk"]
        resonance = metrics["message_resonance"]

        if conversion >= 65 and crisis < 50 and resonance >= 65:
            verdict = "launch_with_guardrails"
            headline = "Launch, but keep proof and response guardrails active."
        elif crisis >= 60:
            verdict = "revise_before_launch"
            headline = "Do not launch as-is. Reduce crisis triggers first."
        elif conversion < 45:
            verdict = "optimize_message"
            headline = "Do not scale yet. Improve the message before adding media budget."
        else:
            verdict = "controlled_pilot"
            headline = "Run a controlled pilot before full launch."

        segment = top_positive.get("name") or top_positive.get("segment_name") or "the strongest positive segment"
        return {
            "verdict": verdict,
            "headline": headline,
            "recommended_campaign": "Current campaign with revisions" if verdict != "launch_with_guardrails" else "Current campaign",
            "rationale": f"Conversion is {conversion:.0f}%, crisis risk is {_severity(crisis)}, and strongest response comes from {segment}.",
            "next_best_action": risk.get("recommended_action", "Add proof points and test one revised message variant."),
            "confidence": round(_clamp((resonance * 0.45) + ((100 - crisis) * 0.25) + (conversion * 0.3)), 1),
        }

    def _business_impact(self, metrics: Dict[str, float], business: Dict[str, Any]) -> Dict[str, Any]:
        market_size = _number(business.get("market_size"), self.DEFAULT_BUSINESS["market_size"])
        unit_price = _number(business.get("unit_price"), self.DEFAULT_BUSINESS["unit_price"])
        current_share = _number(business.get("current_market_share"), self.DEFAULT_BUSINESS["current_market_share"])
        base_conversion = _number(business.get("base_conversion_rate"), self.DEFAULT_BUSINESS["base_conversion_rate"])
        campaign_budget = _number(business.get("campaign_budget"), self.DEFAULT_BUSINESS["campaign_budget"])
        crisis_response_cost = _number(business.get("crisis_response_cost"), self.DEFAULT_BUSINESS["crisis_response_cost"])

        share_shift = (metrics["brand_perception_shift"] * 0.08) + ((metrics["overall_sentiment"] - 20) * 0.025)
        projected_share = max(0, current_share + share_shift)
        effective_conversion = metrics["conversion_probability"] * (0.65 + metrics["message_resonance"] / 200)
        base_units = market_size * (current_share / 100) * (base_conversion / 100)
        projected_units = market_size * (projected_share / 100) * (effective_conversion / 100)
        revenue_uplift = (projected_units - base_units) * unit_price
        crisis_loss = crisis_response_cost * (metrics["crisis_risk"] / 100) + max(revenue_uplift, 0) * (metrics["crisis_risk"] / 100) * 0.18
        roi = ((revenue_uplift - campaign_budget) / campaign_budget * 100) if campaign_budget else 0

        return {
            "estimated_revenue_impact": round(revenue_uplift, 0),
            "estimated_crisis_loss": round(crisis_loss, 0),
            "market_share_shift_pct": round(share_shift, 2),
            "projected_market_share_pct": round(projected_share, 2),
            "roi_pct": round(roi, 1),
            "business_readout": self._business_readout(revenue_uplift, crisis_loss, roi),
        }

    def _business_mapping(self, metrics: Dict[str, float], impact: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "kpi": "Sentiment",
                "business_meaning": "Brand perception",
                "value": round(metrics["overall_sentiment"], 1),
                "interpretation": "Positive brand lift" if metrics["overall_sentiment"] >= 20 else "Needs stronger trust signal",
            },
            {
                "kpi": "Conversion",
                "business_meaning": "Revenue impact",
                "value": round(metrics["conversion_probability"], 1),
                "interpretation": f"Estimated revenue impact {impact['estimated_revenue_impact']:,.0f}",
            },
            {
                "kpi": "Crisis Risk",
                "business_meaning": "PR cost exposure",
                "value": round(metrics["crisis_risk"], 1),
                "interpretation": f"Estimated crisis loss {impact['estimated_crisis_loss']:,.0f}",
            },
            {
                "kpi": "Polarization",
                "business_meaning": "Long-term brand damage risk",
                "value": round(metrics["opinion_polarization"], 1),
                "interpretation": "High split in audience opinion" if metrics["opinion_polarization"] >= 50 else "Manageable audience split",
            },
            {
                "kpi": "Brand Shift",
                "business_meaning": "Market share movement",
                "value": round(metrics["brand_perception_shift"], 1),
                "interpretation": f"Projected share shift {impact['market_share_shift_pct']} pts",
            },
        ]

    def _primary_risk(self, metrics: Dict[str, float], top_negative: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
        risk_drivers = evidence.get("risk_drivers") or []
        segment_name = top_negative.get("name") or top_negative.get("segment_name") or "Risk-sensitive segment"
        segment_sentiment = _number(top_negative.get("sentiment", top_negative.get("avg_sentiment")), 0)
        driver = risk_drivers[0] if risk_drivers else f"{segment_name} shows weak or negative reaction."

        if metrics["crisis_risk"] >= 55 or segment_sentiment < -20:
            action = "Rewrite the riskiest claim and add proof before scaling."
        elif metrics["conversion_probability"] < 50:
            action = "Create one sharper value-proposition variant and retest."
        else:
            action = "Launch with monitoring, FAQ, and influencer response guardrails."

        return {
            "segment": segment_name,
            "severity": _severity(max(metrics["crisis_risk"], abs(min(segment_sentiment, 0)))),
            "driver": driver,
            "recommended_action": action,
        }

    def _actions(
        self,
        metrics: Dict[str, float],
        risk: Dict[str, Any],
        top_positive: Dict[str, Any],
        top_negative: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        actions = [
            {
                "priority": "critical" if risk["severity"] in ("critical", "high") else "high",
                "description": risk["recommended_action"],
                "timeline": "Before launch",
            },
            {
                "priority": "high",
                "description": f"Build a segment-specific creative for {top_positive.get('name') or top_positive.get('segment_name') or 'the strongest positive segment'}.",
                "timeline": "This week",
            },
            {
                "priority": "medium",
                "description": f"Prepare objection handling for {top_negative.get('name') or top_negative.get('segment_name') or 'the highest-risk segment'}.",
                "timeline": "Within 10 days",
            },
        ]
        if metrics["opinion_polarization"] >= 45:
            actions.append({
                "priority": "medium",
                "description": "Split the launch into audience cohorts instead of one broad national message.",
                "timeline": "Pilot phase",
            })
        return actions

    def _top_segment(self, segments: List[Dict[str, Any]], reverse: bool) -> Dict[str, Any]:
        if not segments:
            return {}

        def sentiment(segment: Dict[str, Any]) -> float:
            return _number(segment.get("sentiment", segment.get("avg_sentiment")), 0)

        return sorted(segments, key=sentiment, reverse=reverse)[0]

    def _business_readout(self, revenue_uplift: float, crisis_loss: float, roi: float) -> str:
        if roi >= 25 and revenue_uplift > crisis_loss:
            return "Business upside is stronger than modeled crisis exposure."
        if crisis_loss > max(revenue_uplift, 1):
            return "Crisis exposure can erase the campaign upside. Fix risk drivers first."
        return "Upside exists, but launch should be staged and monitored."

