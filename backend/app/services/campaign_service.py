"""CampaignService — CRUD for Campaign, stored as JSON files per organization.

Campaigns are stored in:
    Config.UPLOAD_FOLDER/organizations/<org_id>/campaigns/<campaign_id>.json
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from ..config import Config
from ..models.campaign import (
    Campaign, CampaignStatus, CampaignObjective,
    CampaignTarget, SimulationConfig,
)
from ..models.organization import Organization, SubscriptionTier
from ..utils.logger import get_logger

logger = get_logger('mirofish.campaign_service')


class CampaignService:
    """CRUD service for Campaign management with JSON file storage."""

    def __init__(self, upload_folder: Optional[str] = None):
        self.base_dir = upload_folder or Config.UPLOAD_FOLDER
        os.makedirs(self.base_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def _org_campaigns_dir(self, org_id: str) -> str:
        """Directory for a given org's campaigns."""
        path = os.path.join(self.base_dir, "organizations", org_id, "campaigns")
        os.makedirs(path, exist_ok=True)
        return path

    def _campaign_path(self, org_id: str, campaign_id: str) -> str:
        """JSON file path for a campaign."""
        return os.path.join(self._org_campaigns_dir(org_id), f"{campaign_id}.json")

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create_campaign(
        self,
        org_id: str,
        name: str,
        description: str = "",
        objective: str = "message_testing",
        target: Optional[Dict[str, Any]] = None,
        sim_config: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
    ) -> Campaign:
        """Create a new campaign for an organization.

        Enforces tier-based campaign limits via Organization.can_create_campaign().

        Args:
            org_id: Organization ID.
            name: Campaign name.
            description: Optional description.
            objective: One of CampaignObjective values.
            target: Dict matching CampaignTarget fields.
            sim_config: Dict matching SimulationConfig fields.
            created_by: User ID of creator.

        Returns:
            The newly created Campaign instance.

        Raises:
            ValueError: If tier limit exceeded or org not found.
        """
        # --- Validate org exists and tier limit ---
        org = self._load_org(org_id)
        if org is None:
            raise ValueError(f"Organization '{org_id}' not found")

        if not org.can_create_campaign():
            limits = {
                SubscriptionTier.FREE: 1,
                SubscriptionTier.PRO: 10,
                SubscriptionTier.ENTERPRISE: "unlimited",
            }
            raise ValueError(
                f"Campaign limit reached for tier '{org.tier.value}' "
                f"(max: {limits[org.tier]})"
            )

        # --- Build campaign ---
        campaign = Campaign(
            org_id=org_id,
            name=name.strip(),
            description=description,
        )

        # Objective
        try:
            campaign.objective = CampaignObjective(objective)
        except ValueError:
            logger.warning(f"Invalid objective '{objective}', defaulting to MESSAGE_TESTING")

        # Target
        if target:
            campaign.target = CampaignTarget(**target)

        # Simulation config
        if sim_config:
            campaign.sim_config = SimulationConfig(**sim_config)

        if created_by:
            campaign.created_by = created_by

        # --- Persist ---
        self._write_campaign(campaign)

        # --- Increment org campaign_count ---
        org.campaign_count += 1
        self._write_org(org)

        logger.info(
            f"Created campaign '{campaign.campaign_id}' for org '{org_id}' "
            f"(name='{name}', tier={org.tier.value}, count={org.campaign_count})"
        )
        return campaign

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def get_campaign(self, campaign_id: str, org_id: Optional[str] = None) -> Optional[Campaign]:
        """Get a campaign by ID. If org_id is provided, looks only in that org."""
        if org_id:
            return self._read_campaign(self._campaign_path(org_id, campaign_id))
        # Search all orgs
        orgs_base = os.path.join(self.base_dir, "organizations")
        if not os.path.isdir(orgs_base):
            return None
        for org_dir in os.listdir(orgs_base):
            path = self._campaign_path(org_dir, campaign_id)
            if os.path.exists(path):
                return self._read_campaign(path)
        return None

    def list_campaigns(
        self,
        org_id: str,
        status_filter: Optional[str] = None,
        include_archived: bool = False,
    ) -> List[Campaign]:
        """List all campaigns for an organization.

        Args:
            org_id: Organization ID.
            status_filter: Optional status value to filter by.
            include_archived: Include archived campaigns (default False).
        """
        campaigns_dir = self._org_campaigns_dir(org_id)
        campaigns: List[Campaign] = []

        for filename in os.listdir(campaigns_dir):
            if not filename.endswith(".json"):
                continue
            campaign = self._read_campaign(os.path.join(campaigns_dir, filename))
            if campaign is None:
                continue
            if not include_archived and campaign.status == CampaignStatus.ARCHIVED:
                continue
            if status_filter and campaign.status.value != status_filter:
                continue
            campaigns.append(campaign)

        campaigns.sort(key=lambda c: c.created_at, reverse=True)
        return campaigns

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_campaign(
        self,
        campaign_id: str,
        org_id: str,
        data: Dict[str, Any],
    ) -> Optional[Campaign]:
        """Update campaign fields. Returns updated campaign or None if not found."""
        campaign = self.get_campaign(campaign_id, org_id=org_id)
        if campaign is None:
            return None

        allowed_fields = {
            "name", "description", "objective", "status",
            "tags", "results_summary",
        }

        for key, value in data.items():
            if key not in allowed_fields:
                continue
            if key == "objective":
                try:
                    campaign.objective = CampaignObjective(value)
                except ValueError:
                    logger.warning(f"Ignoring invalid objective '{value}'")
                continue
            if key == "status":
                try:
                    campaign.status = CampaignStatus(value)
                except ValueError:
                    logger.warning(f"Ignoring invalid status '{value}'")
                continue
            setattr(campaign, key, value)

        campaign.updated_at = datetime.now(timezone.utc).isoformat()
        self._write_campaign(campaign)
        return campaign

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete_campaign(self, campaign_id: str, org_id: str) -> bool:
        """Delete a campaign (hard delete — removes the JSON file).

        Decrements org.campaign_count.
        """
        path = self._campaign_path(org_id, campaign_id)
        if not os.path.exists(path):
            return False

        os.remove(path)

        # Decrement org count
        org = self._load_org(org_id)
        if org:
            org.campaign_count = max(0, org.campaign_count - 1)
            org.updated_at = datetime.now(timezone.utc).isoformat()
            self._write_org(org)

        logger.info(f"Deleted campaign '{campaign_id}' from org '{org_id}'")
        return True

    # ------------------------------------------------------------------
    # Pipeline helpers (status transitions)
    # ------------------------------------------------------------------

    def update_status(self, campaign: Campaign, new_status: CampaignStatus) -> Campaign:
        """Update campaign status and persist."""
        campaign.status = new_status
        campaign.updated_at = datetime.now(timezone.utc).isoformat()
        if new_status == CampaignStatus.COMPLETED:
            campaign.completed_at = datetime.now(timezone.utc).isoformat()
        self._write_campaign(campaign)
        return campaign

    def update_links(
        self,
        campaign: Campaign,
        project_id: Optional[str] = None,
        graph_id: Optional[str] = None,
        simulation_id: Optional[str] = None,
        report_id: Optional[str] = None,
    ) -> Campaign:
        """Update pipeline entity links on the campaign."""
        if project_id is not None:
            campaign.project_id = project_id
        if graph_id is not None:
            campaign.graph_id = graph_id
        if simulation_id is not None:
            campaign.simulation_id = simulation_id
        if report_id is not None:
            campaign.report_id = report_id
        campaign.updated_at = datetime.now(timezone.utc).isoformat()
        self._write_campaign(campaign)
        return campaign

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_org(self, org_id: str) -> Optional[Organization]:
        """Load organization by ID from JSON file."""
        path = os.path.join(self.base_dir, "organizations", f"{org_id}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Organization.from_dict(data)
        except (json.JSONDecodeError, OSError, TypeError):
            return None

    def _write_org(self, org: Organization) -> None:
        """Persist organization to JSON file."""
        org_dir = os.path.join(self.base_dir, "organizations")
        os.makedirs(org_dir, exist_ok=True)
        path = os.path.join(org_dir, f"{org.org_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(org.to_dict(), f, ensure_ascii=False, indent=2)

    def _read_campaign(self, path: str) -> Optional[Campaign]:
        """Read a Campaign from a JSON file path."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Campaign.from_dict(data)
        except (json.JSONDecodeError, OSError, TypeError):
            return None

    def _write_campaign(self, campaign: Campaign) -> None:
        """Serialize a Campaign to its JSON file."""
        org_dir = self._org_campaigns_dir(campaign.org_id)
        path = os.path.join(org_dir, f"{campaign.campaign_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(campaign.to_dict(), f, ensure_ascii=False, indent=2)
