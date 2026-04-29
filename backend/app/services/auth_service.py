"""AuthService — JWT-style token creation and validation.

Uses PyJWT if available; falls back to HMAC+SHA256+Base64 simple tokens.
Secret comes from env AUTH_SECRET_KEY, or a hard-coded fallback.
"""

import os
import json
import time
import hmac
import hashlib
import base64
from typing import Optional, Dict, Any

from ..config import Config
from ..models.user import User


# ---------------------------------------------------------------------------
# Attempt to use PyJWT; if unavailable, use the home-grown simple token
# ---------------------------------------------------------------------------
try:
    import jwt as _pyjwt  # type: ignore[import-untyped]

    _HAS_PYJWT = True
except ImportError:
    _HAS_PYJWT = False


def _get_secret() -> str:
    """Return the auth secret, preferring AUTH_SECRET_KEY env var."""
    return os.environ.get("AUTH_SECRET_KEY", Config.SECRET_KEY or "mirofish-auth-fallback")


# ---------------------------------------------------------------------------
# Simple token helpers (fallback when PyJWT is absent)
# ---------------------------------------------------------------------------
def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64_decode(s: str) -> bytes:
    # Add padding back
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def _simple_create_token(payload: Dict[str, Any], secret: str) -> str:
    """Create a token: base64(payload_json) + '.' + base64(hmac_signature)."""
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_b64 = _b64_encode(payload_bytes)

    sig = hmac.new(secret.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).digest()
    sig_b64 = _b64_encode(sig)

    return f"{payload_b64}.{sig_b64}"


def _simple_validate_token(token: str, secret: str) -> Optional[Dict[str, Any]]:
    """Validate a simple token; returns payload dict or None."""
    try:
        parts = token.split(".", 1)
        if len(parts) != 2:
            return None
        payload_b64, sig_b64 = parts

        # Verify signature
        expected_sig = hmac.new(
            secret.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256
        ).digest()
        actual_sig = _b64_decode(sig_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = _b64_decode(payload_b64)
        payload = json.loads(payload_bytes)

        # Check expiry
        exp = payload.get("exp", 0)
        if exp and time.time() > exp:
            return None  # expired

        return payload
    except Exception:
        return None


# ---------------------------------------------------------------------------
# AuthService
# ---------------------------------------------------------------------------
class AuthService:
    """Authentication and token management service."""

    TOKEN_EXPIRY_SECONDS = 24 * 60 * 60  # 24 hours

    def __init__(self, secret: Optional[str] = None):
        self.secret = secret or _get_secret()

    # ------------------------------------------------------------------
    # JWT / Token creation & validation
    # ------------------------------------------------------------------
    def create_token(self, user: User) -> str:
        """Create an auth token for a user.

        Payload: {sub: user_id, org: org_id, role: role, exp: timestamp}
        """
        now = int(time.time())
        payload: Dict[str, Any] = {
            "sub": user.user_id,
            "org": user.org_id,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
            "iat": now,
            "exp": now + self.TOKEN_EXPIRY_SECONDS,
        }

        if _HAS_PYJWT:
            return _pyjwt.encode(payload, self.secret, algorithm="HS256")
        else:
            return _simple_create_token(payload, self.secret)

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate a token and return its payload dict, or None."""
        try:
            if _HAS_PYJWT:
                payload = _pyjwt.decode(
                    token, self.secret, algorithms=["HS256"],
                    options={"require": ["exp", "sub"]},
                )
                return {
                    "sub": payload.get("sub"),
                    "org": payload.get("org"),
                    "role": payload.get("role"),
                }
            else:
                payload = _simple_validate_token(token, self.secret)
                if payload is None:
                    return None
                return {
                    "sub": payload.get("sub"),
                    "org": payload.get("org"),
                    "role": payload.get("role"),
                }
        except Exception:
            return None

    # ------------------------------------------------------------------
    # API key creation & validation
    # ------------------------------------------------------------------
    def create_api_key(self, user: User) -> Dict[str, str]:
        """Generate a raw API key and return it along with its prefix.

        NOTE: This only generates the key material. Storing the hash on
        the user record must be done by UserService.generate_api_key().
        """
        raw_key, api_key_hash, api_key_prefix = User.generate_api_key()
        return {
            "raw_key": raw_key,
            "hash": api_key_hash,
            "prefix": api_key_prefix,
        }

    def validate_api_key(self, raw_key: str, user_service=None) -> Optional[Dict[str, Any]]:
        """Validate a raw API key by looking up the user who owns it.

        Args:
            raw_key: The raw API key string (e.g. "ms_abcd...")
            user_service: UserService instance. If not provided, one is created.

        Returns:
            User-like dict with keys: sub, org, role — or None if invalid.
        """
        if user_service is None:
            from .user_service import UserService
            user_service = UserService()

        user = user_service.find_user_by_api_key(raw_key)
        if user is None:
            return None

        return {
            "sub": user.user_id,
            "org": user.org_id,
            "role": user.role.value if hasattr(user.role, "value") else str(user.role),
        }
