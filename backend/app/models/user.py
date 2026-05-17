"""User domain model — belongs to an Organization with role-based access."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, timezone
import uuid
import hashlib
import secrets
import hmac

from werkzeug.security import check_password_hash, generate_password_hash


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
        """Hash password with Werkzeug's adaptive password hasher."""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against stored hash."""
        if User.is_legacy_password_hash(password_hash):
            return User._verify_legacy_password(password, password_hash)
        try:
            return check_password_hash(password_hash, password)
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def is_legacy_password_hash(password_hash: str) -> bool:
        """Return True for the historical salt:sha256 password format."""
        if not isinstance(password_hash, str) or ":" not in password_hash:
            return False
        salt, digest = password_hash.split(":", 1)
        return (
            len(salt) == 32
            and len(digest) == 64
            and all(ch in "0123456789abcdef" for ch in salt.lower())
            and all(ch in "0123456789abcdef" for ch in digest.lower())
        )

    @staticmethod
    def _verify_legacy_password(password: str, password_hash: str) -> bool:
        try:
            salt, digest = password_hash.split(":", 1)
            candidate = hashlib.sha256((salt + password).encode()).hexdigest()
            return hmac.compare_digest(candidate, digest)
        except (ValueError, AttributeError, TypeError):
            return False

    @staticmethod
    def password_needs_rehash(password_hash: str) -> bool:
        """Return True when a password hash should be upgraded after login."""
        return User.is_legacy_password_hash(password_hash)

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
