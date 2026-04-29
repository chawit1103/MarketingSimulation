"""TenantMiddleware — Flask before_request handler for multi-tenant auth.

Extracts authentication from:
  - Authorization: Bearer <token>
  - X-Api-Key: <api-key>
  - ?api_key=<api-key> query parameter

Injects g.current_user and g.current_org (Organization dict) on success.
Returns 401/403 JSON on failure.
Skips auth for: /health, /api/auth/*, OPTIONS requests.
"""

from typing import Optional, Dict, Any
from flask import g, request, jsonify

from ..config import Config
from ..models.organization import OrganizationStatus, Organization


def _load_current_org(org_id: str, org_service) -> Optional[Organization]:
    """Load the organization scoped to this request."""
    return org_service.get_org(org_id)


class TenantMiddleware:
    """Installable middleware that enforces tenant authentication.

    Usage (in create_app):
        from app.middleware.tenant_middleware import TenantMiddleware
        TenantMiddleware(app)
    """

    # Paths that bypass authentication entirely
    PUBLIC_PREFIXES = ("/health", "/api/auth/", "/api/persona/archetypes", "/api/persona/regions")
    PUBLIC_METHODS = {"OPTIONS"}

    def __init__(self, app=None, auth_service=None, org_service=None):
        # Deferred imports to avoid circular deps
        if auth_service is None:
            from ..services.auth_service import AuthService
            auth_service = AuthService()
        if org_service is None:
            from ..services.organization_service import OrganizationService
            org_service = OrganizationService()

        self._auth = auth_service
        self._orgs = org_service

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register before_request handler on a Flask app."""
        app.before_request(self._enforce)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _is_public(self) -> bool:
        """Return True if the current request does NOT require auth."""
        if request.method in self.PUBLIC_METHODS:
            return True
        path = request.path
        return any(path.startswith(p) for p in self.PUBLIC_PREFIXES)

    def _extract_token(self) -> Optional[str]:
        """Try to extract a token / API key from the request."""
        # 1) Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()

        # 2) X-Api-Key header
        api_key = request.headers.get("X-Api-Key")
        if api_key:
            return api_key

        # 3) ?api_key= query param
        api_key = request.args.get("api_key")
        if api_key:
            return api_key

        return None

    def _authenticate(self, token: str) -> Optional[Dict[str, Any]]:
        """Try to validate the credential as a JWT first, then as an API key.

        Returns a dict with keys: sub, org, role — or None.
        """
        # Try JWT first
        payload = self._auth.validate_token(token)
        if payload is not None:
            return payload

        # Try API key
        return self._auth.validate_api_key(token)

    # ------------------------------------------------------------------
    # before_request handler
    # ------------------------------------------------------------------
    def _enforce(self):
        """before_request callback — injects g.current_user / g.current_org."""
        # Skip public paths
        if self._is_public():
            return

        # Extract credential
        token = self._extract_token()
        if not token:
            return self._abort(401, "Missing authentication token")

        # Validate
        payload = self._authenticate(token)
        if payload is None:
            return self._abort(401, "Invalid or expired authentication token")

        user_id = payload.get("sub")
        org_id = payload.get("org")
        role = payload.get("role")

        if not user_id or not org_id:
            return self._abort(401, "Malformed authentication token")

        # Load org & check status
        org = _load_current_org(org_id, self._orgs)
        if org is None:
            return self._abort(401, "Organization not found")
        if org.status == OrganizationStatus.SUSPENDED:
            return self._abort(403, "Organization is suspended")
        if org.status == OrganizationStatus.DELETED:
            return self._abort(401, "Organization not found")

        # Inject into Flask g
        g.current_user = {
            "user_id": user_id,
            "org_id": org_id,
            "role": role,
        }
        g.current_org = org.to_dict()

    # ------------------------------------------------------------------
    # Error response
    # ------------------------------------------------------------------
    @staticmethod
    def _abort(status_code: int, message: str):
        """Abort the request with a JSON error body."""
        response = jsonify({"error": message})
        response.status_code = status_code
        # Note: Returning the response from a before_request handler
        # causes Flask to skip the view function and send this response.
        # We need to raise an abort-like pattern. However, before_request
        # can return a Response directly to short-circuit.
        return response
