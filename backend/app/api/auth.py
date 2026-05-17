"""
Auth API — registration, login, API key management, and org switching.

All endpoints return {success: bool, data/error: ...} JSON responses.
"""
from flask import Blueprint, request, jsonify, g

from ..services.organization_service import OrganizationService
from ..services.user_service import UserService
from ..services.auth_service import AuthService
from ..services.audit_log_service import record_audit_event
from ..models.user import User, UserRole
from ..authz import ADMIN_ROLES, ANY_AUTHENTICATED_ROLES, role_required
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.auth')

auth_bp = Blueprint('auth', __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_auth_service() -> AuthService:
    """Factory for AuthService (token handling only)."""
    return AuthService()


def _get_org_service() -> OrganizationService:
    return OrganizationService()


def _get_user_service() -> UserService:
    return UserService()


# ---------------------------------------------------------------------------
# POST /api/auth/register
# ---------------------------------------------------------------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Create a new Organization and its first admin user.

    Body (JSON):
        org_name : str     — Display name for the organization
        org_slug : str     — URL-safe unique slug, e.g. "brand-x-thailand"
        email    : str     — Admin user email
        password : str     — Admin user password (plain text, hashed on server)
        name     : str     — Admin user display name

    Returns:
        { success: true, data: { org: {...}, user: {...}, token: "..." } }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400

        required_fields = ['org_name', 'org_slug', 'email', 'password', 'name']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return jsonify({'success': False, 'error': f'Missing fields: {", ".join(missing)}'}), 400

        org_svc = _get_org_service()
        user_svc = _get_user_service()
        auth_svc = _get_auth_service()

        # 1. Create organization
        org = org_svc.create_org(
            name=data['org_name'],
            slug=data['org_slug'],
            email=data['email'],
        )

        # 2. Create admin user
        user = user_svc.create_user(
            org_id=org.org_id,
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role='admin',
        )

        # 3. Generate token
        token = auth_svc.create_token(user)

        return jsonify({'success': True, 'data': {
            'org': org.to_dict(),
            'user': user.to_dict(),
            'token': token,
        }}), 201

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 409
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return jsonify({'success': False, 'error': 'Registration failed'}), 500


# ---------------------------------------------------------------------------
# POST /api/auth/login
# ---------------------------------------------------------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate with email + password and return a JWT token.

    Body (JSON):
        email    : str
        password : str

    Returns:
        { success: true, data: { user: {...}, token: "...", org: {...} } }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400

        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400

        auth_svc = _get_auth_service()
        user_svc = _get_user_service()
        org_svc = _get_org_service()

        # 1. Find user by email (scan all orgs)
        user = user_svc.get_user_by_email_global(email)
        if not user:
            raise ValueError('Invalid email or password')

        # 2. Verify password
        if not User.verify_password(password, user.password_hash):
            raise ValueError('Invalid email or password')

        if User.password_needs_rehash(user.password_hash):
            logger.info("Rehashing legacy password hash for user %s", user.user_id)
            refreshed = user_svc.update_user(user.org_id, user.user_id, {'password': password})
            if refreshed is not None:
                user = refreshed

        # 3. Check org is active
        org = org_svc.get_org(user.org_id)
        if not org or org.status.value != 'active':
            raise ValueError('Organization is not active')

        # 4. Generate token
        token = auth_svc.create_token(user)
        record_audit_event(
            org_id=user.org_id,
            event_type="login",
            actor_user_id=user.user_id,
            resource_type="user",
            resource_id=user.user_id,
            metadata={"auth_method": "password"},
        )

        return jsonify({'success': True, 'data': {
            'user': user.to_dict(),
            'org': org.to_dict(),
            'token': token,
        }})

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


# ---------------------------------------------------------------------------
# GET /api/auth/me
# ---------------------------------------------------------------------------

@auth_bp.route('/me', methods=['GET'])
@role_required(*ANY_AUTHENTICATED_ROLES)
def me():
    """
    Return the currently authenticated user and their active organization.

    Requires: Authorization: Bearer <token> header.

    Returns:
        { success: true, data: { user: {...}, org: {...} } }
    """
    try:
        user_svc = _get_user_service()
        org_svc = _get_org_service()
        user = user_svc.get_user(g.current_user_id, org_id=g.current_org_id)
        org = org_svc.get_org(g.current_org_id)

        user_dict = user.to_dict() if user else None
        org_dict = org.to_dict() if org else None

        if not user_dict:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({'success': True, 'data': {
            'user': user_dict,
            'org': org_dict,
        }})

    except Exception as e:
        logger.error(f"GET /me failed: {str(e)}")
        return jsonify({'success': False, 'error': 'Unable to load current user'}), 500


# ---------------------------------------------------------------------------
# POST /api/auth/api-key
# ---------------------------------------------------------------------------

@auth_bp.route('/api-key', methods=['POST'])
@role_required(*ADMIN_ROLES)
def generate_api_key():
    """
    Generate a new API key for the current user.

    The raw key is returned ONCE — it cannot be retrieved again.
    Only the SHA-256 hash and a display prefix are stored server-side.

    Requires: Authorization: Bearer <token> header.

    Returns:
        { success: true, data: { api_key: "ms_...", prefix: "ms_abcd1234..." } }
    """
    try:
        user_svc = _get_user_service()
        generated = user_svc.generate_api_key(g.current_org_id, g.current_user_id)
        if generated is None:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({'success': True, 'data': {
            'api_key': generated["raw_key"],
            'prefix': generated["prefix"],
        }})

    except Exception as e:
        logger.error(f"API key generation failed: {str(e)}")
        return jsonify({'success': False, 'error': 'API key generation failed'}), 500


# ---------------------------------------------------------------------------
# POST /api/auth/switch-org
# ---------------------------------------------------------------------------

@auth_bp.route('/switch-org', methods=['POST'])
@role_required(UserRole.ADMIN)
def switch_org():
    """
    Switch the active organization for the current user.

    The user must belong to the target organization.
    A new JWT token scoped to the target org is issued.

    Body (JSON):
        org_id : str  — Target organization ID

    Returns:
        { success: true, data: { user: {...}, token: "...", org: {...} } }
    """
    try:
        data = request.get_json(silent=True) or {}
        target_org_id = str(data.get('org_id') or '').strip()
        if not target_org_id:
            return jsonify({'success': False, 'error': 'Target organization is required'}), 400

        # The current local JSON user model supports exactly one organization
        # per user. Until a real membership model exists, never issue a token
        # for any other org and use one generic denial message so callers
        # cannot probe organization existence.
        if target_org_id != g.current_org_id:
            return jsonify({
                'success': False,
                'error': 'Organization switch is not available for this user',
            }), 403

        return jsonify({
            'success': False,
            'error': 'Organization switching is disabled until multi-org membership is implemented',
        }), 501

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        logger.error(f"Org switch failed: {str(e)}")
        return jsonify({'success': False, 'error': 'Organization switch failed'}), 500
