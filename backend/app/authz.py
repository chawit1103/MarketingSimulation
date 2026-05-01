"""Route authorization helpers for role-based access control."""

from functools import wraps
from typing import Iterable

from flask import g, jsonify

from .models.user import UserRole


ADMIN_ROLES = (UserRole.ADMIN,)
ANALYST_ROLES = (UserRole.ADMIN, UserRole.ANALYST)
ANY_AUTHENTICATED_ROLES = (UserRole.ADMIN, UserRole.ANALYST, UserRole.VIEWER)


def _role_value(role) -> str:
    if hasattr(role, "value"):
        return str(role.value)
    return str(role or "").strip().lower()


def current_role() -> str:
    """Return the role attached by TenantMiddleware, if any."""
    current_user = g.get("current_user") or {}
    if isinstance(current_user, dict) and current_user.get("role"):
        return _role_value(current_user.get("role"))
    return _role_value(g.get("current_user_role"))


def role_required(*roles: UserRole | str):
    """Require an authenticated user with one of the given roles."""
    allowed = {_role_value(role) for role in roles}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not g.get("current_user"):
                return jsonify({"success": False, "error": "Authentication required"}), 401

            role = current_role()
            if role not in allowed:
                return jsonify({
                    "success": False,
                    "error": "Insufficient role for this operation",
                    "required_roles": sorted(allowed),
                }), 403

            return view(*args, **kwargs)

        return wrapped

    return decorator


def require_roles(roles: Iterable[UserRole | str]):
    """Convenience wrapper for dynamic role lists."""
    return role_required(*roles)
