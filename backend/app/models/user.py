"""User domain model — belongs to an Organization with role-based access."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
import uuid
import hashlib
import secrets


class UserRole(str, Enum):
    ADMIN = "admin"           # Full org control, billing, member management
    ANALYST = "analyst"       # Create/run campaigns, view reports
    VIEWER = "viewer"         # Read-only access to dashboards


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    INVITED = "invited"


class User(BaseModel):
    user_id: str = Field(default_factory=lambda: f"usr_{uuid.uuid4().hex[:12]}")
    org_id: str
    email: str
    name: str = ""
    role: UserRole = UserRole.ANALYST
    status: UserStatus = UserStatus.ACTIVE
    password_hash: str = ""
    api_key_hash: str = ""   # SHA256 of generated API key (stored, not raw)
    api_key_prefix: str = ""  # First 8 chars for display: "ms_abcd1234..."
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_login_at: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with SHA256 + salt."""
        salt = secrets.token_hex(16)
        return salt + ":" + hashlib.sha256((salt + password).encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            salt, h = password_hash.split(":", 1)
            return h == hashlib.sha256((salt + password).encode()).hexdigest()
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def generate_api_key() -> tuple[str, str, str]:
        """Generate API key. Returns (raw_key, hash, prefix)."""
        raw = "ms_" + secrets.token_hex(24)  # ms_ + 48 hex chars
        h = hashlib.sha256(raw.encode()).hexdigest()
        prefix = raw[:11] + "..."  # ms_abcd1234...
        return raw, h, prefix

    @staticmethod
    def verify_api_key(raw_key: str, api_key_hash: str) -> bool:
        """Verify raw API key against stored hash."""
        return hashlib.sha256(raw_key.encode()).hexdigest() == api_key_hash

    def to_dict(self, safe: bool = True) -> Dict[str, Any]:
        """Convert to dict. safe=True removes sensitive fields."""
        d = self.model_dump()
        if safe:
            d.pop("password_hash", None)
            d.pop("api_key_hash", None)
        return d
