"""Persona API — generate, list, and manage synthetic consumer personas."""
import traceback
from flask import Blueprint, request, jsonify, g

from ..services.persona_factory import PersonaFactory
from ..services.organization_service import OrganizationService
from ..models.campaign import Campaign, CampaignTarget
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.persona')

persona_bp = Blueprint('persona', __name__)


def _get_org_id():
    """Get org_id from authenticated request context."""
    return g.get('current_org_id') or (g.current_user.get('org_id') if g.get('current_user') else None)


@persona_bp.route('/generate', methods=['POST'])
def generate_personas():
    """Generate Thai personas for a campaign.

    Body: {
        campaign_id: str,
        target: {segment_name, age_range, gender, regions, interests, persona_count},
        language: str (default 'th')
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body required'}), 400

        org_id = _get_org_id()
        campaign_id = data.get('campaign_id')
        language = data.get('language', 'th')
        target_data = data.get('target', {})

        if not campaign_id:
            return jsonify({'success': False, 'error': 'campaign_id required'}), 400

        # Build target
        target = CampaignTarget(
            segment_name=target_data.get('segment_name', 'Custom'),
            age_range=tuple(target_data.get('age_range', [18, 65])),
            gender=target_data.get('gender', 'all'),
            regions=target_data.get('regions', ['Bangkok']),
            persona_count=target_data.get('persona_count', 100),
            interests=target_data.get('interests', []),
        )

        # Generate
        factory = PersonaFactory()
        personas = factory.generate_batch(
            org_id=org_id,
            campaign_id=campaign_id,
            target=target,
            count=target.persona_count,
            language=language,
        )

        return jsonify({
            'success': True,
            'data': {
                'count': len(personas),
                'personas': [p.to_dict() for p in personas[:50]],  # Limit response
            }
        })

    except Exception as e:
        logger.error(f"Persona generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


@persona_bp.route('/archetypes', methods=['GET'])
def list_archetypes():
    """List available Thai consumer archetypes with descriptions."""
    from ..services.thai_context import CONSUMER_ARCHETYPES

    return jsonify({
        'success': True,
        'data': {
            name: {
                'age_range': arch['age_range'],
                'income': arch['income'],
                'regions': arch['regions'],
                'description': arch['narrative'],
            }
            for name, arch in CONSUMER_ARCHETYPES.items()
        }
    })


@persona_bp.route('/regions', methods=['GET'])
def list_regions():
    """List Thai regions with profiles."""
    from ..services.thai_context import REGION_PROFILES, REGION_POPULATION

    return jsonify({
        'success': True,
        'data': {
            region: {
                'population_millions': REGION_POPULATION.get(region, 0),
                'traits': profile['traits'],
                'lifestyle': profile['lifestyle_note'],
            }
            for region, profile in REGION_PROFILES.items()
        }
    })
