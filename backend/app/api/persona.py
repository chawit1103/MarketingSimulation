"""Persona API — generate, list, and manage synthetic consumer personas.

Supports 11 countries via ?lang= parameter.
"""
import traceback
from flask import Blueprint, request, jsonify, g

from ..services.persona_factory import PersonaFactory
from ..services.persona_context import ContextRegistry
from ..models.campaign import CampaignTarget
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.persona')

persona_bp = Blueprint('persona', __name__)


def _get_org_id():
    return g.get('current_org_id') or (g.current_user.get('org_id') if g.get('current_user') else None)


@persona_bp.route('/generate', methods=['POST'])
def generate_personas():
    """Generate personas for a campaign in any supported language.

    Body: {campaign_id, target: {...}, language: 'th'|'en'|'zh'|...}
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

        target = CampaignTarget(
            segment_name=target_data.get('segment_name', 'Custom'),
            age_range=tuple(target_data.get('age_range', [18, 65])),
            gender=target_data.get('gender', 'all'),
            regions=target_data.get('regions', ['Bangkok']),
            persona_count=target_data.get('persona_count', 100),
            interests=target_data.get('interests', []),
        )

        factory = PersonaFactory()
        personas = factory.generate_batch(
            org_id=org_id, campaign_id=campaign_id,
            target=target, count=target.persona_count, language=language,
        )

        return jsonify({
            'success': True,
            'data': {'count': len(personas), 'personas': [p.to_dict() for p in personas[:50]]}
        })
    except Exception as e:
        logger.error(f"Persona generation failed: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


@persona_bp.route('/archetypes', methods=['GET'])
def list_archetypes():
    """List consumer archetypes for a country. ?lang=en (default: th)."""
    language = request.args.get('lang', 'th')
    ctx = ContextRegistry.get_context(language)

    return jsonify({
        'success': True,
        'country': ctx.COUNTRY_NAME,
        'data': {
            name: {
                'age_range': arch['age_range'],
                'income': arch['income'],
                'regions': arch['regions'],
                'description': arch['narrative'],
            }
            for name, arch in ctx.CONSUMER_ARCHETYPES.items()
        }
    })


@persona_bp.route('/regions', methods=['GET'])
def list_regions():
    """List regions for a country. ?lang=en (default: th)."""
    language = request.args.get('lang', 'th')
    ctx = ContextRegistry.get_context(language)

    return jsonify({
        'success': True,
        'country': ctx.COUNTRY_NAME,
        'data': {
            region: {
                'population_millions': ctx.REGION_POPULATION.get(region, 0),
                'traits': profile['traits'],
                'lifestyle': profile['lifestyle_note'],
            }
            for region, profile in ctx.REGION_PROFILES.items()
        }
    })


@persona_bp.route('/countries', methods=['GET'])
def list_countries():
    """List available countries with persona context."""
    from ..models.persona import Country
    from .persona_context import LANG_TO_MODULE
    return jsonify({
        'success': True,
        'data': [
            {'code': c.value, 'name': c.name}
            for c in Country
            if c.value in LANG_TO_MODULE
        ]
    })
