"""
Executive Dashboard Models — KPI calculations, segment breakdowns, action plans.
Provides the data model for the executive-level simulation report.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


# ---------------------------------------------------------------------------
# Sub-models for segment breakdowns, influencers, timeline, action items
# ---------------------------------------------------------------------------

class SegmentSentiment(BaseModel):
    """Sentiment breakdown for one persona archetype or region segment."""
    segment_name: str                                          # e.g. "Bangkok Millennials"
    persona_count: int = 0
    avg_sentiment: float = 0.0                                 # -100 to +100
    conversion_estimate: float = 0.0                           # 0.0-100.0 %


class Influencer(BaseModel):
    """Top influencer: high influence_weight × sentiment impact."""
    agent_name: str
    agent_type: str = "persona"
    influence_score: float = 0.0                               # 0.0-100.0
    sentiment_impact: float = 0.0                              # net shift caused


class TimelinePoint(BaseModel):
    """Sentiment snapshot at a given round / simulated hour."""
    round_num: int = 0
    simulated_hour: int = 0
    avg_sentiment: float = 0.0                                 # -100 to +100
    action_count: int = 0


class ActionItem(BaseModel):
    """Actionable recommendation for the executive team."""
    priority: str = "medium"                                   # critical | high | medium
    action: str = ""                                           # สิ่งที่ต้องทำ
    expected_impact: str = ""                                  # ผลลัพธ์ที่คาดหวัง
    timeline: str = "1 สัปดาห์"                                  # ทันที / 1 สัปดาห์ / 1 เดือน


# ---------------------------------------------------------------------------
# Main Executive Report
# ---------------------------------------------------------------------------

class ExecutiveReport(BaseModel):
    """Full executive dashboard report for a completed campaign simulation."""

    report_id: str = Field(default_factory=lambda: f"rpt_{uuid.uuid4().hex[:12]}")
    campaign_id: str
    org_id: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    simulation_id: Optional[str] = None
    run_id: Optional[str] = None
    source_mode: str = "unknown"
    data_basis: str = "unknown"
    confidence: Optional[float] = None
    limitations: List[str] = Field(default_factory=list)

    # ---- Aggregate KPIs (0-100 scale unless noted) ----
    overall_sentiment: float = 0.0              # -100 to +100 (avg across all agents)
    conversion_probability: float = 0.0         # 0-100 %
    social_influence_index: float = 0.0         # 0-100
    message_resonance: float = 0.0              # 0-100 %
    crisis_risk: float = 0.0                    # 0-100 %
    brand_perception_shift: float = 0.0         # -100 to +100 (delta start→end)
    opinion_polarization: float = 0.0           # 0-100 (std-dev of sentiment)

    # ---- Detailed breakdowns ----
    sentiment_by_segment: List[SegmentSentiment] = Field(default_factory=list)
    top_influencers: List[Influencer] = Field(default_factory=list)
    sentiment_timeline: List[TimelinePoint] = Field(default_factory=list)

    # ---- Executive action plan (Think → Finish) ----
    winning_strategy: str = ""                  # แผนที่ชนะ
    risk_areas: List[str] = Field(default_factory=list)  # จุดเสี่ยง
    action_items: List[ActionItem] = Field(default_factory=list)  # ขั้นตอนปฏิบัติ
    executive_summary: str = ""                 # สรุปผู้บริหาร (ภาษาไทย)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutiveReport":
        return cls(**data)

    @classmethod
    def empty(cls, campaign_id: str, org_id: str) -> "ExecutiveReport":
        """Create an empty report shell (used before calculation completes)."""
        return cls(campaign_id=campaign_id, org_id=org_id)
