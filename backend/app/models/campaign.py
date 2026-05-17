"""Campaign domain model — a marketing simulation run owned by an Organization."""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
import uuid


class CampaignStatus(str, Enum):
    DRAFT = "draft"               # Configuring, not yet ready
    PERSONA_BUILDING = "persona_building"  # Generating synthetic personas
    SIMULATING = "simulating"     # OASIS simulation running
    COMPLETED = "completed"       # Simulation finished, report ready
    ARCHIVED = "archived"         # Read-only, saved for reference
    FAILED = "failed"


class CampaignObjective(str, Enum):
    MESSAGE_TESTING = "message_testing"        # Test marketing message effectiveness
    CRISIS_SIMULATION = "crisis_simulation"    # PR crisis scenario
    PRODUCT_LAUNCH = "product_launch"          # New product market reaction
    COMPETITOR_RESPONSE = "competitor_response" # Competitor move simulation
    BRAND_PERCEPTION = "brand_perception"      # Brand sentiment analysis


class CampaignTarget(BaseModel):
    """Target audience segment definition."""
    segment_name: str = "General"
    age_range: tuple[int, int] = (18, 65)
    gender: str = "all"  # male, female, all
    regions: List[str] = Field(default_factory=lambda: ["Bangkok"])
    channels: List[str] = Field(
        default_factory=lambda: ["twitter_x", "reddit", "facebook", "instagram", "tiktok"]
    )
    income_level: str = "all"
    interests: List[str] = Field(default_factory=list)
    persona_count: int = 100


class SimulationConfig(BaseModel):
    """Simulation parameters for a campaign."""
    platform: str = "twitter"               # twitter, reddit, both
    audience_channels: List[str] = Field(default_factory=list)  # Context channels; native engine remains twitter/reddit
    platform_mode: str = "auto"             # auto, microblog, community_forum, group_chat, creator_feed, commerce_intent
    oasis_preset: Dict[str, Any] = Field(default_factory=dict)
    max_rounds: int = 20                    # Simulation hours
    language: str = "th"                    # Agent communication language
    injection_event: Optional[str] = None   # Crisis/event injected at round N
    injection_text: Optional[str] = None    # The event/message text
    realtime_updates: bool = True           # WebSocket/SSE for live view


class Campaign(BaseModel):
    campaign_id: str = Field(default_factory=lambda: f"cmp_{uuid.uuid4().hex[:12]}")
    org_id: str
    name: str
    description: str = ""
    objective: CampaignObjective = CampaignObjective.MESSAGE_TESTING
    status: CampaignStatus = CampaignStatus.DRAFT
    target: CampaignTarget = Field(default_factory=CampaignTarget)
    sim_config: SimulationConfig = Field(default_factory=SimulationConfig)

    # Links to existing MiroFish pipeline
    project_id: Optional[str] = None   # Maps to graph_builder project
    graph_id: Optional[str] = None     # Neo4j graph UUID
    simulation_id: Optional[str] = None # SimulationRunState ID
    report_id: Optional[str] = None

    # File uploads
    uploaded_files: List[Dict[str, str]] = Field(default_factory=list)
    
    # Results (populated after simulation)
    results_summary: Optional[Dict[str, Any]] = None
    brief_quality: Optional[Dict[str, Any]] = None
    brief_metadata: Dict[str, Any] = Field(default_factory=dict)

    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    # Metadata
    created_by: Optional[str] = None  # user_id
    tags: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Campaign":
        return cls(**data)

    def can_start_simulation(self) -> bool:
        return self.status in (CampaignStatus.DRAFT, CampaignStatus.PERSONA_BUILDING)
