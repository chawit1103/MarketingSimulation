"""UserService — CRUD for User, stored as JSON files under an Organization.

Users are stored as individual JSON files:
    Config.UPLOAD_FOLDER/organizations/<org_id>/users/<user_id>.json
"""

import os
import json
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from ..config import Config
from ..models.user import User, UserRole, UserStatus


class UserService:
    """Service for managing User CRUD with JSON file storage per organization."""

    def __init__(self, org_service=None, upload_folder: Optional[str] = None):
        # Deferred import to avoid circular dependency at module level
        if org_service is None:
            from .organization_service import OrganizationService
            org_service = OrganizationService()
        self.org_service = org_service
        self.base_orgs_dir = upload_folder or os.path.join(Config.UPLOAD_FOLDER, "organizations")

    def _users_dir(self, org_id: str) -> str:
        """Return the directory where users of a given org are stored."""
        d = os.path.join(self.base_orgs_dir, org_id, "users")
        os.makedirs(d, exist_ok=True)
        return d

    def _user_path(self, org_id: str, user_id: str) -> str:
        return os.path.join(self._users_dir(org_id), f"{user_id}.json")

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create_user(self, org_id: str, email: str, password: str,
                    name: str = "", role: UserRole = UserRole.ANALYST) -> User:
        """Create a new user in the given organization.

        Args:
            org_id: Organization the user belongs to.
            email: Unique email (per org).
            password: Plain-text password – hashed before storage.
            name: Display name.
            role: UserRole (default ANALYST).

        Returns:
            The newly created User.

        Raises:
            ValueError: If the org does not exist or the email is already taken.
        """
        # Ensure org exists
        if self.org_service.get_org(org_id) is None:
            raise ValueError(f"Organization '{org_id}' not found")

        # Check duplicate email in the same org
        if self.get_user_by_email(org_id, email) is not None:
            raise ValueError(f"Email '{email}' already registered in organization '{org_id}'")

        password_hash = User.hash_password(password)

        user = User(
            org_id=org_id,
            email=email.strip().lower(),
            name=name.strip(),
            role=role,
            password_hash=password_hash,
        )
        self._write_user(user)
        return user

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def get_user(self, user_id: str, org_id: Optional[str] = None) -> Optional[User]:
        """Get a user by ID. If org_id is provided, search only that org.

        Without org_id, scans all orgs (slower) — use get_user_by_id_global().
        """
        if org_id is not None:
            return self._read_user(self._user_path(org_id, user_id))
        return self.get_user_by_id_global(user_id)

    def get_user_by_id_global(self, user_id: str) -> Optional[User]:
        """Find a user by ID across all organizations."""
        if not os.path.isdir(self.base_orgs_dir):
            return None
        for org_dir in os.listdir(self.base_orgs_dir):
            users_dir = os.path.join(self.base_orgs_dir, org_dir, "users")
            user_path = os.path.join(users_dir, f"{user_id}.json")
            if os.path.exists(user_path):
                return self._read_user(user_path)
        return None

    def get_user_by_email(self, org_id: str, email: str) -> Optional[User]:
        """Find a user by email within a specific organization."""
        users_dir = self._users_dir(org_id)
        email_lower = email.strip().lower()
        for filename in os.listdir(users_dir):
            if not filename.endswith(".json"):
                continue
            user = self._read_user(os.path.join(users_dir, filename))
            if user is not None and user.email.lower() == email_lower:
                return user
        return None

    def get_user_by_email_global(self, email: str) -> Optional[User]:
        """Find a user by email across ALL organizations (for login)."""
        orgs_dir = self.base_orgs_dir
        if not os.path.isdir(orgs_dir):
            return None
        email_lower = email.strip().lower()
        for org_entry in os.listdir(orgs_dir):
            org_path = os.path.join(orgs_dir, org_entry)
            users_dir = os.path.join(org_path, 'users')
            if not os.path.isdir(users_dir):
                continue
            for filename in os.listdir(users_dir):
                if not filename.endswith('.json'):
                    continue
                user = self._read_user(os.path.join(users_dir, filename))
                if user is not None and user.email.lower() == email_lower:
                    return user
        return None

    def list_users(self, org_id: str, include_inactive: bool = False) -> List[User]:
        """List all users in an organization."""
        users_dir = self._users_dir(org_id)
        users: List[User] = []
        for filename in os.listdir(users_dir):
            if not filename.endswith(".json"):
                continue
            user = self._read_user(os.path.join(users_dir, filename))
            if user is None:
                continue
            if not include_inactive and user.status == UserStatus.INACTIVE:
                continue
            users.append(user)
        users.sort(key=lambda u: u.created_at, reverse=True)
        return users

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update_user(self, org_id: str, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        """Update user fields. Returns updated User or None if not found."""
        user = self.get_user(user_id, org_id=org_id)
        if user is None:
            return None

        allowed_fields = {"name", "email", "role", "status", "last_login_at"}

        # Handle email uniqueness
        new_email = data.get("email")
        if new_email is not None:
            new_email = new_email.strip().lower()
            if new_email != user.email.lower():
                if self.get_user_by_email(org_id, new_email) is not None:
                    raise ValueError(f"Email '{new_email}' already in use")
            data["email"] = new_email

        # Handle password change
        if "password" in data:
            user.password_hash = User.hash_password(data["password"])
            del data["password"]

        for key, value in data.items():
            if key in allowed_fields:
                setattr(user, key, value)

        self._write_user(user)
        return user

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete_user(self, org_id: str, user_id: str) -> bool:
        """Delete a user's JSON file entirely."""
        path = self._user_path(org_id, user_id)
        if not os.path.exists(path):
            return False
        os.remove(path)
        return True

    # ------------------------------------------------------------------
    # API key management
    # ------------------------------------------------------------------
    def generate_api_key(self, org_id: str, user_id: str) -> Optional[Dict[str, str]]:
        """Generate an API key for a user. Returns dict with raw_key and prefix.

        The raw_key is ONLY returned here — it cannot be retrieved later.
        """
        user = self.get_user(user_id, org_id=org_id)
        if user is None:
            return None

        raw_key, api_key_hash, api_key_prefix = User.generate_api_key()
        user.api_key_hash = api_key_hash
        user.api_key_prefix = api_key_prefix
        self._write_user(user)

        return {"raw_key": raw_key, "prefix": api_key_prefix}

    def revoke_api_key(self, org_id: str, user_id: str) -> bool:
        """Revoke a user's API key by clearing its hash."""
        user = self.get_user(user_id, org_id=org_id)
        if user is None:
            return False
        user.api_key_hash = ""
        user.api_key_prefix = ""
        self._write_user(user)
        return True

    def find_user_by_api_key(self, raw_key: str) -> Optional[User]:
        """Find a user by matching a raw API key across all orgs."""
        if not os.path.isdir(self.base_orgs_dir):
            return None
        for org_dir in os.listdir(self.base_orgs_dir):
            users_dir = os.path.join(self.base_orgs_dir, org_dir, "users")
            if not os.path.isdir(users_dir):
                continue
            for filename in os.listdir(users_dir):
                if not filename.endswith(".json"):
                    continue
                user = self._read_user(os.path.join(users_dir, filename))
                if user is None or not user.api_key_hash:
                    continue
                if User.verify_api_key(raw_key, user.api_key_hash):
                    return user
        return None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _read_user(self, path: str) -> Optional[User]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return User(**data)
        except (json.JSONDecodeError, OSError, TypeError):
            return None

    def _write_user(self, user: User) -> None:
        path = self._user_path(user.org_id, user.user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(user.to_dict(safe=False), f, ensure_ascii=False, indent=2)
