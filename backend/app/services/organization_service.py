"""OrganizationService — CRUD for Organization, stored as JSON files.

Organizations are stored as individual JSON files in:
    Config.UPLOAD_FOLDER/organizations/<org_id>.json
"""

import os
import json
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from ..config import Config
from ..models.organization import Organization, OrganizationStatus


class OrganizationService:
    """Service for managing Organization CRUD with JSON file storage."""

    def __init__(self, upload_folder: Optional[str] = None):
        self.base_dir = upload_folder or os.path.join(Config.UPLOAD_FOLDER, "organizations")
        os.makedirs(self.base_dir, exist_ok=True)

    def _org_path(self, org_id: str) -> str:
        """Get the JSON file path for an organization."""
        return os.path.join(self.base_dir, f"{org_id}.json")

    def _slug_exists(self, slug: str, exclude_org_id: Optional[str] = None) -> bool:
        """Check whether a slug is already taken by another organization."""
        for filename in os.listdir(self.base_dir):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.base_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
            if data.get("slug") == slug:
                org_id = filename[:-5]  # strip ".json"
                if exclude_org_id is None or org_id != exclude_org_id:
                    return True
        return False

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create_org(self, name: str, slug: str, email: str = "",
                   tier: Optional[str] = None) -> Organization:
        """Create a new Organization.

        Args:
            name: Display name.
            slug: URL-safe unique identifier.
            email: Contact email.
            tier: Subscription tier (defaults to FREE).

        Returns:
            The newly created Organization instance.

        Raises:
            ValueError: If the slug is already in use.
        """
        slug = slug.lower().strip()
        if self._slug_exists(slug):
            raise ValueError(f"Organization slug '{slug}' already exists")

        org = Organization(
            name=name.strip(),
            slug=slug,
            contact_email=email.strip(),
        )
        if tier is not None:
            org.tier = tier  # type: ignore[assignment]

        self._write_org(org)
        return org

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def get_org(self, org_id: str) -> Optional[Organization]:
        """Get an organization by ID. Returns None if not found."""
        path = self._org_path(org_id)
        if not os.path.exists(path):
            return None
        return self._read_org(path)

    def get_org_by_slug(self, slug: str) -> Optional[Organization]:
        """Look up an organization by its unique slug."""
        slug = slug.lower().strip()
        for filename in os.listdir(self.base_dir):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.base_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
            if data.get("slug") == slug:
                return Organization.from_dict(data)
        return None

    def list_orgs(self, include_deleted: bool = False) -> List[Organization]:
        """List all organizations.

        Args:
            include_deleted: If False, skip orgs with status DELETED.
        """
        orgs: List[Organization] = []
        for filename in os.listdir(self.base_dir):
            if not filename.endswith(".json"):
                continue
            org = self._read_org(os.path.join(self.base_dir, filename))
            if org is None:
                continue
            if not include_deleted and org.status == OrganizationStatus.DELETED:
                continue
            orgs.append(org)
        orgs.sort(key=lambda o: o.created_at, reverse=True)
        return orgs

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update_org(self, org_id: str, data: Dict[str, Any]) -> Optional[Organization]:
        """Update organization fields. Returns updated org or None if not found."""
        org = self.get_org(org_id)
        if org is None:
            return None

        # Slug uniqueness check
        new_slug = data.get("slug")
        if new_slug is not None:
            new_slug = new_slug.lower().strip()
            if new_slug != org.slug and self._slug_exists(new_slug, exclude_org_id=org_id):
                raise ValueError(f"Organization slug '{new_slug}' already exists")
            data["slug"] = new_slug

        # Merge allowed fields
        allowed_fields = {
            "name", "slug", "tier", "status", "contact_email",
            "settings", "campaign_count", "simulation_minutes", "agent_count_total",
        }
        for key, value in data.items():
            if key in allowed_fields:
                setattr(org, key, value)

        org.updated_at = datetime.now(timezone.utc).isoformat()
        self._write_org(org)
        return org

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete_org(self, org_id: str, hard_delete: bool = False) -> bool:
        """Delete (or soft-delete) an organization.

        Args:
            org_id: Organization ID.
            hard_delete: If True, remove the JSON file entirely.

        Returns:
            True if the organization existed, False otherwise.
        """
        path = self._org_path(org_id)
        if not os.path.exists(path):
            return False

        if hard_delete:
            os.remove(path)
        else:
            org = self._read_org(path)
            if org is not None:
                org.status = OrganizationStatus.DELETED
                org.updated_at = datetime.now(timezone.utc).isoformat()
                self._write_org(org)
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _read_org(self, path: str) -> Optional[Organization]:
        """Read an Organization from a JSON file path."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Organization.from_dict(data)
        except (json.JSONDecodeError, OSError, TypeError):
            return None

    def _write_org(self, org: Organization) -> None:
        """Serialize an Organization to its JSON file."""
        path = self._org_path(org.org_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(org.to_dict(), f, ensure_ascii=False, indent=2)
