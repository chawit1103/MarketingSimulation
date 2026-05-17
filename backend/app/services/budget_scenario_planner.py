"""Deterministic budget scenario planner.

This service provides assumption-based channel and segment allocation guidance.
It intentionally avoids exact ROI/ROAS prediction language and does not use
live ad-platform cost data.
"""

from __future__ import annotations

from typing import Any, Dict, List


SAFE_SOURCE_MODES = {"demo_mode", "local_estimate", "live_backend", "backend_verified", "unknown_source"}


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _slug(value: str) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("/", "_")


class BudgetScenarioPlanner:
    """Create deterministic budget/channel what-if guidance."""

    DEFAULT_CHANNELS = ["facebook", "instagram", "tiktok", "youtube", "line"]

    OBJECTIVE_WEIGHTS: Dict[str, Dict[str, float]] = {
        "awareness": {
            "tiktok": 0.24,
            "instagram": 0.20,
            "facebook": 0.18,
            "youtube": 0.18,
            "line": 0.08,
            "twitter_x": 0.06,
            "reddit": 0.03,
            "linkedin": 0.03,
        },
        "conversion": {
            "facebook": 0.22,
            "line": 0.20,
            "tiktok": 0.18,
            "instagram": 0.16,
            "youtube": 0.10,
            "linkedin": 0.06,
            "twitter_x": 0.05,
            "reddit": 0.03,
        },
        "retention": {
            "line": 0.30,
            "facebook": 0.22,
            "instagram": 0.14,
            "youtube": 0.12,
            "tiktok": 0.10,
            "linkedin": 0.05,
            "twitter_x": 0.04,
            "reddit": 0.03,
        },
        "crisis_recovery": {
            "facebook": 0.24,
            "line": 0.18,
            "twitter_x": 0.16,
            "youtube": 0.14,
            "tiktok": 0.12,
            "instagram": 0.08,
            "reddit": 0.05,
            "linkedin": 0.03,
        },
    }

    RISK_SPREAD = {
        "low": 0.12,
        "medium": 0.18,
        "high": 0.25,
    }

    def plan(self, inputs: Dict[str, Any] | None) -> Dict[str, Any]:
        inputs = inputs or {}
        total_budget = max(0, _number(inputs.get("total_budget"), 0))
        duration_weeks = max(1, int(_number(inputs.get("duration_weeks"), 6)))
        objective = _slug(inputs.get("objective") or "awareness")
        if objective not in self.OBJECTIVE_WEIGHTS:
            objective = "awareness"

        risk_tolerance = _slug(inputs.get("risk_tolerance") or "medium")
        if risk_tolerance not in self.RISK_SPREAD:
            risk_tolerance = "medium"

        channels = self._channels(inputs.get("channel_mix"))
        segments = self._segments(inputs.get("target_segments"))
        source_mode = "demo_mode" if inputs.get("demo") else "live_backend"

        channel_weights = self._channel_weights(objective, channels, inputs.get("channel_mix"))
        segment_weights = self._segment_weights(segments)
        spread = self.RISK_SPREAD[risk_tolerance]

        allocations = [
            self._allocation(channel, weight, total_budget, duration_weeks, spread, objective)
            for channel, weight in channel_weights.items()
        ]
        segment_allocations = [
            self._segment_allocation(segment, weight, total_budget, spread)
            for segment, weight in segment_weights.items()
        ]

        confidence_score = self._confidence_score(total_budget, duration_weeks, channels, segments, inputs)

        return {
            "version": "budget_scenario_planner_v1",
            "scenario_type": "assumption_based_budget_planning",
            "objective": objective,
            "total_budget": round(total_budget, 2),
            "duration_weeks": duration_weeks,
            "risk_tolerance": risk_tolerance,
            "source": self._source(source_mode),
            "allocation_ranges": allocations,
            "segment_allocation_ranges": segment_allocations,
            "trade_offs": self._tradeoffs(objective, risk_tolerance, channels),
            "confidence_level": self._confidence_label(confidence_score),
            "confidence_score": confidence_score,
            "assumptions": self._assumptions(inputs),
            "limitations": self._limitations(),
            "recommended_validation_step": self._recommended_validation_step(confidence_score, objective),
            "safe_wording": [
                "scenario estimate",
                "assumption-based planning",
                "channel mix what-if",
                "directional budget guidance",
            ],
            "disclaimer": (
                "This budget scenario is directional planning guidance, not an exact ROI, ROAS, "
                "or media-performance prediction."
            ),
        }

    def _channels(self, channel_mix: Any) -> List[str]:
        if isinstance(channel_mix, dict):
            channels = [_slug(key) for key in channel_mix if _slug(key)]
        elif isinstance(channel_mix, list):
            channels = [_slug(item) for item in channel_mix if _slug(item)]
        else:
            channels = self.DEFAULT_CHANNELS
        return list(dict.fromkeys(channels))[:8] or self.DEFAULT_CHANNELS

    def _segments(self, target_segments: Any) -> List[str]:
        if isinstance(target_segments, list):
            segments = [str(item).strip() for item in target_segments if str(item).strip()]
        elif isinstance(target_segments, str):
            segments = [part.strip() for part in target_segments.split(",") if part.strip()]
        else:
            segments = []
        return segments[:6] or ["Primary target segment", "Secondary validation segment"]

    def _channel_weights(self, objective: str, channels: List[str], channel_mix: Any) -> Dict[str, float]:
        base = self.OBJECTIVE_WEIGHTS[objective]
        weights: Dict[str, float] = {}

        if isinstance(channel_mix, dict):
            supplied = {
                _slug(channel): max(0, _number(value, 0))
                for channel, value in channel_mix.items()
                if _slug(channel) in channels
            }
            supplied_total = sum(supplied.values())
            if supplied_total > 0:
                for channel in channels:
                    supplied_weight = supplied.get(channel, 0) / supplied_total
                    objective_weight = base.get(channel, 0.08)
                    weights[channel] = (supplied_weight * 0.58) + (objective_weight * 0.42)
                return self._normalize(weights)

        for channel in channels:
            weights[channel] = base.get(channel, 0.08)
        return self._normalize(weights)

    def _segment_weights(self, segments: List[str]) -> Dict[str, float]:
        if len(segments) == 1:
            return {segments[0]: 1.0}
        weights = {}
        remaining = 1.0
        for index, segment in enumerate(segments):
            if index == 0:
                weights[segment] = 0.46
                remaining -= 0.46
            else:
                weights[segment] = remaining / (len(segments) - 1)
        return self._normalize(weights)

    @staticmethod
    def _normalize(weights: Dict[str, float]) -> Dict[str, float]:
        total = sum(max(0, value) for value in weights.values()) or 1
        return {key: max(0, value) / total for key, value in weights.items()}

    def _allocation(
        self,
        channel: str,
        weight: float,
        total_budget: float,
        duration_weeks: int,
        spread: float,
        objective: str,
    ) -> Dict[str, Any]:
        midpoint = total_budget * weight
        low = midpoint * (1 - spread)
        high = midpoint * (1 + spread)
        return {
            "channel": channel,
            "recommended_pct_midpoint": round(weight * 100, 1),
            "budget_range": {
                "low": round(low, 0),
                "midpoint": round(midpoint, 0),
                "high": round(high, 0),
            },
            "weekly_range": {
                "low": round(low / duration_weeks, 0),
                "high": round(high / duration_weeks, 0),
            },
            "role": self._channel_role(channel, objective),
            "risk_note": self._channel_risk(channel),
        }

    def _segment_allocation(self, segment: str, weight: float, total_budget: float, spread: float) -> Dict[str, Any]:
        midpoint = total_budget * weight
        return {
            "segment": segment,
            "recommended_pct_midpoint": round(weight * 100, 1),
            "budget_range": {
                "low": round(midpoint * (1 - spread), 0),
                "midpoint": round(midpoint, 0),
                "high": round(midpoint * (1 + spread), 0),
            },
            "reason": "Use as directional segment weighting; validate against actual reach, response, and risk signals.",
        }

    @staticmethod
    def _channel_role(channel: str, objective: str) -> str:
        if channel in {"tiktok", "instagram"} and objective == "awareness":
            return "Discovery and creative resonance testing."
        if channel == "line":
            return "Retention, nurture, service recovery, or conversion follow-up."
        if channel == "youtube":
            return "Proof-led education and longer-form explanation."
        if channel in {"twitter_x", "reddit"}:
            return "Narrative monitoring and fast objection discovery."
        if channel == "linkedin":
            return "B2B, stakeholder, or executive credibility support."
        return "Core reach and audience response testing."

    @staticmethod
    def _channel_risk(channel: str) -> str:
        if channel in {"tiktok", "twitter_x", "reddit"}:
            return "Fast amplification can expose weak claims quickly."
        if channel == "line":
            return "Closed-group response may be harder to observe directly."
        return "Validate creative fatigue and audience overlap before scaling."

    @staticmethod
    def _tradeoffs(objective: str, risk_tolerance: str, channels: List[str]) -> List[Dict[str, str]]:
        return [
            {
                "choice": "Concentrate spend in top channels",
                "upside": "Faster read on the strongest channel mix.",
                "risk": "May overfit to one platform's audience behavior.",
            },
            {
                "choice": "Reserve validation budget",
                "upside": "Keeps room for message testing before scale.",
                "risk": "Reduces short-term reach during the first wave.",
            },
            {
                "choice": f"{objective.replace('_', ' ').title()} objective with {risk_tolerance} risk tolerance",
                "upside": f"Allocation is weighted toward the selected objective across {len(channels)} channels.",
                "risk": "Objective weights are deterministic assumptions until calibrated with real outcomes.",
            },
        ]

    @staticmethod
    def _confidence_score(total_budget: float, duration_weeks: int, channels: List[str], segments: List[str], inputs: Dict[str, Any]) -> int:
        score = 40
        if total_budget > 0:
            score += 15
        if duration_weeks >= 2:
            score += 10
        if len(channels) >= 3:
            score += 10
        if len(segments) >= 2:
            score += 10
        if inputs.get("channel_mix"):
            score += 8
        if inputs.get("risk_tolerance"):
            score += 4
        if inputs.get("objective"):
            score += 3
        return int(_clamp(score, 0, 92))

    @staticmethod
    def _confidence_label(score: int) -> str:
        if score >= 78:
            return "medium_high_directional"
        if score >= 60:
            return "medium_directional"
        return "low_directional"

    @staticmethod
    def _assumptions(inputs: Dict[str, Any]) -> List[str]:
        return [
            "Allocation uses deterministic objective weights and any user-supplied channel mix.",
            "No live media cost, auction, CRM, or sales data is used unless the user supplied it in this request.",
            "Budget ranges are planning ranges around a midpoint, not exact spend instructions.",
            f"Currency is treated as {inputs.get('currency') or 'THB'} for display and planning only.",
        ]

    @staticmethod
    def _limitations() -> List[str]:
        return [
            "This is not exact ROI, ROAS, CAC, sales, or market-share prediction.",
            "Channel costs, audience saturation, creative quality, seasonality, and competitor activity require validation.",
            "Use real pilot results or approved media benchmarks before committing major spend.",
        ]

    @staticmethod
    def _recommended_validation_step(confidence_score: int, objective: str) -> str:
        if confidence_score < 60:
            return "Add clearer budget, channel mix, target segments, and duration before using this plan for approval."
        if objective == "crisis_recovery":
            return "Run a small response-cell rehearsal and legal/comms review before increasing spend."
        return "Reserve 10-20% of the budget for a controlled creative/channel test before scaling."

    @staticmethod
    def _source(source_mode: str) -> Dict[str, Any]:
        if source_mode not in SAFE_SOURCE_MODES:
            source_mode = "unknown_source"
        return {
            "type": source_mode,
            "source_mode": source_mode,
            "data_basis": "demo_fixture" if source_mode == "demo_mode" else "deterministic_scenario_estimate",
            "warning": (
                "Demo fixture for budget-planning walkthrough; not live campaign evidence."
                if source_mode == "demo_mode"
                else "Backend deterministic budget scenario estimate; not calibrated media-performance evidence."
            ),
        }
