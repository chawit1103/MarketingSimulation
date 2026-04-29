"""Organization (Tenant) domain model — the top-level B2B entity.

An Organization owns: Users, Campaigns, Persona Libraries, and
isolated Neo4j graphs. All data is scoped by org_id.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
import uuid


class SubscriptionTier(str, Enum):
    FREE = "free"               # 1 campaign, 100 agents, no export
    PRO = "pro"                 # 10 campaigns, 500 agents, CSV export
    ENTERPRISE = "enterprise"   # Unlimited, API access, white-label


class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class Organization(BaseModel):
    org_id: str = Field(default_factory=lambda: f"org_{uuid.uuid4().hex[:12]}")
    name: str
    slug: str  # URL-safe identifier, e.g. "brand-x-thailand"
    tier: SubscriptionTier = SubscriptionTier.FREE
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    contact_email: str = ""
    settings: Dict[str, Any] = Field(default_factory=lambda: {
        "language": "th",
        "default_llm_provider": "deepseek",
        "default_llm_model": "deepseek-chat",
        "timezone": "Asia/Bangkok",
    })
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Usage tracking
    campaign_count: int = 0
    simulation_minutes: int = 0
    agent_count_total: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Organization":
        return cls(**data)

    def can_create_campaign(self) -> bool:
        limits = {
            SubscriptionTier.FREE: 1,
            SubscriptionTier.PRO: 10,
            SubscriptionTier.ENTERPRISE: 999,
        }
        return self.campaign_count < limits[self.tier]

    def max_agents(self) -> int:
        limits = {
            SubscriptionTier.FREE: 100,
            SubscriptionTier.PRO: 500,
            SubscriptionTier.ENTERPRISE: 5000,
        }
        return limits[self.tier]
