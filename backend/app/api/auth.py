"""
Auth API — registration, login, API key management, and org switching.

All endpoints return {success: bool, data/error: ...} JSON responses.
"""
import traceback
from flask import Blueprint, request, jsonify, g

from ..services.organization_service import OrganizationService
from ..services.user_service import UserService
from ..services.auth_service import AuthService
from ..models.user import User
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


def auth_required(f):
    """
    Decorator: require a valid JWT token.

    Expects Authorization: Bearer <token> header.
    Sets g.current_user_id, g.current_org_id, g.current_user, g.current_org.
    The tenant_middleware also runs as before_request and populates
    g.tenant_org_id, but auth_required ensures the user is authenticated.
    """
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Missing or invalid Authorization header'}), 401

        token = auth_header[7:]  # strip "Bearer "
        auth_svc = _get_auth_service()

        try:
            payload = auth_svc.validate_token(token)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Invalid or expired token: {str(e)}'}), 401

        g.current_user_id = payload.get('sub')
        g.current_org_id = payload.get('org')
        g.current_user_role = payload.get('role', 'analyst')

        # Optionally load full user/org objects for convenience
        try:
            user_svc = UserService()
            g.current_user = user_svc.get_user(g.current_user_id)
            org_svc = OrganizationService()
            g.current_org = org_svc.get_org(g.current_org_id)
        except Exception:
            # Token valid but user/org lookup failed — still allow the request;
            # downstream can check g.current_user / g.current_org
            g.current_user = None
            g.current_org = None

        return f(*args, **kwargs)

    return decorated


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
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


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

        # 3. Check org is active
        org = org_svc.get_org(user.org_id)
        if not org or org.status.value != 'active':
            raise ValueError('Organization is not active')

        # 4. Generate token
        token = auth_svc.create_token(user)

        return jsonify({'success': True, 'data': {
            'user': user.to_dict(),
            'org': org.to_dict(),
            'token': token,
        }})

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ---------------------------------------------------------------------------
# GET /api/auth/me
# ---------------------------------------------------------------------------

@auth_bp.route('/me', methods=['GET'])
@auth_required
def me():
    """
    Return the currently authenticated user and their active organization.

    Requires: Authorization: Bearer <token> header.

    Returns:
        { success: true, data: { user: {...}, org: {...} } }
    """
    try:
        user_dict = g.current_user.to_dict() if hasattr(g.current_user, 'to_dict') else (g.current_user if g.current_user else None)
        org_dict = g.current_org.to_dict() if hasattr(g.current_org, 'to_dict') else (g.current_org if g.current_org else None)

        if not user_dict:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        return jsonify({'success': True, 'data': {
            'user': user_dict,
            'org': org_dict,
        }})

    except Exception as e:
        logger.error(f"GET /me failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ---------------------------------------------------------------------------
# POST /api/auth/api-key
# ---------------------------------------------------------------------------

@auth_bp.route('/api-key', methods=['POST'])
@auth_required
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
        user_svc = UserService()
        raw_key, key_hash, prefix = user_svc.generate_and_store_api_key(g.current_user_id)

        return jsonify({'success': True, 'data': {
            'api_key': raw_key,
            'prefix': prefix,
        }})

    except Exception as e:
        logger.error(f"API key generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ---------------------------------------------------------------------------
# POST /api/auth/switch-org
# ---------------------------------------------------------------------------

@auth_bp.route('/switch-org', methods=['POST'])
@auth_required
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
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400

        target_org_id = data.get('org_id')
        if not target_org_id:
            return jsonify({'success': False, 'error': 'org_id is required'}), 400

        auth_svc = _get_auth_service()
        result = auth_svc.switch_org(
            user_id=g.current_user_id,
            current_org_id=g.current_org_id,
            target_org_id=target_org_id,
        )

        return jsonify({'success': True, 'data': result})

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        logger.error(f"Org switch failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500
