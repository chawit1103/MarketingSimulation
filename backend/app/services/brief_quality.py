"""Deterministic campaign brief quality scoring.

This module intentionally avoids LLM calls. It checks whether a campaign brief
contains the business context needed for a more trustworthy simulation.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return " ".join(_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(_text(item) for item in value.values())
    return str(value)


def _has_text(value: Any, min_len: int = 2) -> bool:
    return len(_text(value).strip()) >= min_len


def _has_any_text(values: Iterable[Any], min_len: int = 2) -> bool:
    return any(_has_text(value, min_len=min_len) for value in values)


def _has_keywords(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def _has_pattern(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


class BriefQualityService:
    """Score campaign brief completeness with transparent rules."""

    CRITERIA = [
        {
            "key": "objective",
            "label": "Objective",
            "recommendation": "Define the decision objective, such as message testing, product launch, competitor response, or crisis prevention.",
        },
        {
            "key": "target_audience",
            "label": "Target audience",
            "recommendation": "Specify the primary audience segment, persona type, age range, or buyer group.",
        },
        {
            "key": "market_region",
            "label": "Market / region",
            "recommendation": "Add the launch market or region so cultural and channel assumptions are clear.",
        },
        {
            "key": "campaign_duration",
            "label": "Campaign duration",
            "recommendation": "State the campaign duration, flight dates, or launch window.",
        },
        {
            "key": "budget_range",
            "label": "Budget range",
            "recommendation": "Add a media or campaign budget range; exact numbers are not required.",
        },
        {
            "key": "primary_kpi",
            "label": "Primary KPI",
            "recommendation": "Identify the primary KPI, such as awareness, conversion, sentiment, leads, or market share.",
        },
        {
            "key": "channel_mix",
            "label": "Channel mix",
            "recommendation": "List the channel mix, such as Facebook, TikTok, LINE, X, Reddit, search, retail, or creators.",
        },
        {
            "key": "competitor_context",
            "label": "Competitor context",
            "recommendation": "Describe key competitors, likely counter-moves, pricing pressure, or positioning threats.",
        },
        {
            "key": "brand_constraints",
            "label": "Brand constraints",
            "recommendation": "Add brand constraints, claims, tone rules, must-say, or must-not-say guidance.",
        },
        {
            "key": "risk_legal_notes",
            "label": "Risk / legal notes",
            "recommendation": "Add known legal, regulatory, PR, safety, or compliance risks.",
        },
    ]

    def score(self, brief: Dict[str, Any] | None) -> Dict[str, Any]:
        if brief is None:
            brief = {}
        elif not isinstance(brief, dict):
            brief = {"description": _text(brief)}
        normalized = self._normalize(brief)
        checks = [self._check(criterion, normalized) for criterion in self.CRITERIA]
        present_count = sum(1 for item in checks if item["present"])
        score = round(present_count / len(checks) * 100)
        missing = [item for item in checks if not item["present"]]

        return {
            "score": score,
            "level": self._level(score),
            "confidence_impact": self._confidence_impact(score),
            "brief_completeness": {
                "present": present_count,
                "total": len(checks),
                "percent": score,
            },
            "criteria": checks,
            "missing_fields": missing,
            "recommendations": [item["recommendation"] for item in missing[:4]],
            "known_limitations": self._known_limitations(score, missing),
            "method": "deterministic_brief_quality_v1",
        }

    def _normalize(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        raw_target = brief.get("target") or brief.get("audience") or {}
        target = raw_target if isinstance(raw_target, dict) else {}
        raw_sim_config = brief.get("sim_config") or {}
        sim_config = raw_sim_config if isinstance(raw_sim_config, dict) else {}
        raw_metadata = brief.get("metadata") or brief.get("brief_metadata") or {}
        metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
        fields = {
            "name": brief.get("name"),
            "description": brief.get("description"),
            "objective": brief.get("objective"),
            "target": target,
            "regions": target.get("regions") or brief.get("regions") or metadata.get("regions"),
            "channels": (
                target.get("channels")
                or sim_config.get("audience_channels")
                or brief.get("channels")
                or metadata.get("channels")
            ),
            "duration": brief.get("campaign_duration") or brief.get("duration") or metadata.get("campaign_duration"),
            "budget": brief.get("budget_range") or brief.get("budget") or metadata.get("budget_range"),
            "primary_kpi": brief.get("primary_kpi") or metadata.get("primary_kpi"),
            "competitor_context": brief.get("competitor_context") or metadata.get("competitor_context"),
            "brand_constraints": brief.get("brand_constraints") or metadata.get("brand_constraints"),
            "risk_legal_notes": brief.get("risk_legal_notes") or metadata.get("risk_legal_notes"),
        }
        fields["all_text"] = " ".join(_text(value) for value in fields.values())
        return fields

    def _check(self, criterion: Dict[str, str], fields: Dict[str, Any]) -> Dict[str, Any]:
        key = criterion["key"]
        present = getattr(self, f"_has_{key}")(fields)
        return {
            "key": key,
            "label": criterion["label"],
            "present": present,
            "recommendation": criterion["recommendation"],
        }

    def _has_objective(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("objective")) or _has_keywords(
            fields["all_text"], ["objective", "goal", "awareness", "conversion", "launch", "crisis", "retention"]
        )

    def _has_target_audience(self, fields: Dict[str, Any]) -> bool:
        target = fields.get("target") or {}
        return _has_any_text([target.get("segment_name"), target.get("age_range"), target.get("persona_count")]) or _has_keywords(
            fields["all_text"], ["audience", "persona", "segment", "buyer", "customer", "target", "gen z", "family"]
        )

    def _has_market_region(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("regions")) or _has_keywords(
            fields["all_text"], ["bangkok", "thai", "thailand", "sea", "asean", "region", "market", "province", "global"]
        )

    def _has_campaign_duration(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("duration")) or _has_pattern(
            fields["all_text"], r"\b(\d+\s*(day|week|month|quarter|year|วัน|สัปดาห์|เดือน)|q[1-4]|launch window|flight)\b"
        )

    def _has_budget_range(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("budget")) or _has_pattern(
            fields["all_text"], r"(\$|฿|บาท|budget|media spend|spend|cost|งบ|งบประมาณ)\s*[\d,]*"
        )

    def _has_primary_kpi(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("primary_kpi")) or _has_keywords(
            fields["all_text"], ["kpi", "conversion", "sentiment", "awareness", "reach", "leads", "roi", "market share", "brand lift"]
        )

    def _has_channel_mix(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("channels")) or _has_keywords(
            fields["all_text"], ["facebook", "instagram", "tiktok", "line", "x", "twitter", "reddit", "youtube", "creator", "retail"]
        )

    def _has_competitor_context(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("competitor_context"), min_len=8) or _has_keywords(
            fields["all_text"], ["competitor", "rival", "copycat", "price war", "market leader", "คู่แข่ง"]
        )

    def _has_brand_constraints(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("brand_constraints"), min_len=8) or _has_keywords(
            fields["all_text"], ["brand constraint", "tone", "must say", "must not", "claim", "positioning", "ข้อห้าม", "brand"]
        )

    def _has_risk_legal_notes(self, fields: Dict[str, Any]) -> bool:
        return _has_text(fields.get("risk_legal_notes"), min_len=8) or _has_keywords(
            fields["all_text"], ["risk", "legal", "regulatory", "compliance", "pr risk", "crisis", "claim risk", "กฎหมาย", "ความเสี่ยง"]
        )

    def _level(self, score: int) -> str:
        if score >= 80:
            return "strong"
        if score >= 60:
            return "usable"
        if score >= 40:
            return "thin"
        return "weak"

    def _confidence_impact(self, score: int) -> str:
        if score >= 80:
            return "low_negative_impact"
        if score >= 60:
            return "moderate_negative_impact"
        return "high_negative_impact"

    def _known_limitations(self, score: int, missing: List[Dict[str, Any]]) -> List[str]:
        limitations = []
        if score < 80:
            limitations.append("Simulation confidence is limited by incomplete campaign context.")
        for item in missing[:3]:
            limitations.append(f"Missing {item['label']} may reduce interpretability.")
        return limitations
