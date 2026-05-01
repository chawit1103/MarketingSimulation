"""Campaign API — CRUD endpoints + pipeline orchestration trigger.

All endpoints are tenant-scoped (auth required, org_id from g.current_org_id).
"""

import traceback
from flask import Blueprint, request, jsonify, g

from ..services.campaign_service import CampaignService
from ..services.pipeline_orchestrator import PipelineOrchestrator
from ..services.oasis_platform_presets import resolve_preset
from ..models.campaign import CampaignStatus
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.campaign')

campaign_bp = Blueprint('campaign', __name__)

# Singleton service instances (lazy init)
_campaign_service = None
_pipeline_orchestrator = None


def _get_campaign_service() -> CampaignService:
    global _campaign_service
    if _campaign_service is None:
        _campaign_service = CampaignService()
    return _campaign_service


def _get_pipeline_orchestrator() -> PipelineOrchestrator:
    global _pipeline_orchestrator
    if _pipeline_orchestrator is None:
        _pipeline_orchestrator = PipelineOrchestrator()
    return _pipeline_orchestrator


def _get_org_id() -> str:
    """Extract org_id from authenticated request context."""
    org_id = g.get('current_org_id')
    if not org_id and g.get('current_user'):
        org_id = g.current_user.get('org_id')
    if not org_id:
        raise ValueError("Authentication required — no org_id in request context")
    return org_id


def _get_user_id() -> str:
    """Extract user_id from authenticated request context."""
    if g.get('current_user'):
        return g.current_user.get('user_id', '')
    return ''


# ──────────────────────────────────────────────────────────────────────
# POST /api/campaign — Create campaign
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('', methods=['POST'])
def create_campaign():
    """Create a new campaign for the current org.

    Body: {
        name: str (required),
        description: str,
        objective: str (default 'message_testing'),
        target|audience: {segment_name, age_range|age_min/age_max, gender, regions, channels, interests, persona_count},
        sim_config: {platform, platform_mode, audience_channels, oasis_preset, max_rounds, language}
    }
    """
    try:
        org_id = _get_org_id()
        data = request.get_json() or {}

        name = data.get('name', '').strip()
        if not name:
            return jsonify({'success': False, 'error': 'Campaign name is required'}), 400

        target = _normalize_target_payload(data)
        sim_config = _normalize_sim_config_payload(data, target)

        svc = _get_campaign_service()
        campaign = svc.create_campaign(
            org_id=org_id,
            name=name,
            description=data.get('description', ''),
            objective=data.get('objective', 'message_testing'),
            target=target,
            sim_config=sim_config,
            brief_quality=data.get('brief_quality') if isinstance(data.get('brief_quality'), dict) else None,
            brief_metadata=data.get('brief_metadata') if isinstance(data.get('brief_metadata'), dict) else None,
            created_by=_get_user_id(),
        )

        return jsonify({
            'success': True,
            'data': campaign.to_dict(),
        }), 201

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Create campaign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


def _normalize_target_payload(data: dict) -> dict | None:
    """Accept legacy frontend `audience` payloads and canonical `target` payloads."""
    raw = data.get('target') or data.get('audience')
    if not isinstance(raw, dict):
        return None

    target = dict(raw)
    if 'age_range' not in target:
        age_min = target.pop('age_min', None)
        age_max = target.pop('age_max', None)
        if age_min is not None and age_max is not None:
            target['age_range'] = (int(age_min), int(age_max))

    channels = target.get('channels') or data.get('audience_channels')
    if channels:
        target['channels'] = channels

    return target


def _normalize_sim_config_payload(data: dict, target: dict | None) -> dict | None:
    """Keep the native simulation platform separate from audience channel context."""
    raw = data.get('sim_config') or {}
    sim_config = dict(raw) if isinstance(raw, dict) else {}

    if data.get('platform') and 'platform' not in sim_config:
        sim_config['platform'] = data.get('platform')
    if data.get('platform_mode') and 'platform_mode' not in sim_config:
        sim_config['platform_mode'] = data.get('platform_mode')
    if data.get('max_rounds') is not None and 'max_rounds' not in sim_config:
        sim_config['max_rounds'] = data.get('max_rounds')

    channels = []
    if 'audience_channels' not in sim_config:
        if isinstance(target, dict):
            channels = target.get('channels') or []
        if channels:
            sim_config['audience_channels'] = channels
    else:
        channels = sim_config.get('audience_channels') or []

    sim_config['oasis_preset'] = resolve_preset(
        mode=sim_config.get('platform_mode', 'auto'),
        channels=channels,
        engine_platform=sim_config.get('platform', 'twitter'),
    )

    return sim_config or None


# ──────────────────────────────────────────────────────────────────────
# GET /api/campaign — List campaigns
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('', methods=['GET'])
def list_campaigns():
    """List all campaigns for the current org.

    Query params:
        status: filter by status value
        include_archived: 'true' to include archived
    """
    try:
        org_id = _get_org_id()
        status_filter = request.args.get('status')
        include_archived = request.args.get('include_archived', '').lower() == 'true'

        svc = _get_campaign_service()
        campaigns = svc.list_campaigns(
            org_id=org_id,
            status_filter=status_filter,
            include_archived=include_archived,
        )

        return jsonify({
            'success': True,
            'data': [c.to_dict() for c in campaigns],
            'meta': {'count': len(campaigns), 'org_id': org_id},
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"List campaigns error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ──────────────────────────────────────────────────────────────────────
# GET /api/campaign/<campaign_id> — Get campaign details
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id: str):
    """Get a single campaign by ID."""
    try:
        org_id = _get_org_id()
        svc = _get_campaign_service()
        campaign = svc.get_campaign(campaign_id, org_id=org_id)

        if campaign is None:
            return jsonify({'success': False, 'error': f'Campaign not found: {campaign_id}'}), 404

        return jsonify({
            'success': True,
            'data': campaign.to_dict(),
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Get campaign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ──────────────────────────────────────────────────────────────────────
# PUT /api/campaign/<campaign_id> — Update campaign
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('/<campaign_id>', methods=['PUT'])
def update_campaign(campaign_id: str):
    """Update campaign fields.

    Body: {name, description, objective, status, tags, results_summary}
    """
    try:
        org_id = _get_org_id()
        data = request.get_json() or {}

        svc = _get_campaign_service()
        campaign = svc.update_campaign(campaign_id, org_id, data)

        if campaign is None:
            return jsonify({'success': False, 'error': f'Campaign not found: {campaign_id}'}), 404

        return jsonify({
            'success': True,
            'data': campaign.to_dict(),
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Update campaign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ──────────────────────────────────────────────────────────────────────
# DELETE /api/campaign/<campaign_id> — Delete campaign
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id: str):
    """Delete a campaign (hard delete)."""
    try:
        org_id = _get_org_id()
        svc = _get_campaign_service()

        deleted = svc.delete_campaign(campaign_id, org_id)
        if not deleted:
            return jsonify({'success': False, 'error': f'Campaign not found: {campaign_id}'}), 404

        return jsonify({
            'success': True,
            'message': f'Campaign {campaign_id} deleted',
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Delete campaign error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ──────────────────────────────────────────────────────────────────────
# POST /api/campaign/<campaign_id>/pipeline/start — Start pipeline
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('/<campaign_id>/pipeline/start', methods=['POST'])
def start_pipeline(campaign_id: str):
    """Start the full simulation pipeline for a campaign.

    Runs all 5 steps sequentially:
      1. Validate draft
      2. Generate personas
      3. Build graph
      4. Run simulation
      5. Generate KPI report

    Returns pipeline progress on success.
    """
    try:
        org_id = _get_org_id()

        orch = _get_pipeline_orchestrator()
        progress = orch.run_pipeline(campaign_id, org_id)

        success = progress.error is None

        return jsonify({
            'success': success,
            'data': progress.to_dict(),
            'message': 'Pipeline completed' if success else f'Pipeline failed: {progress.error}',
        }), 200 if success else 500

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Pipeline start error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500


# ──────────────────────────────────────────────────────────────────────
# GET /api/campaign/<campaign_id>/pipeline/status — Get pipeline status
# ──────────────────────────────────────────────────────────────────────
@campaign_bp.route('/<campaign_id>/pipeline/status', methods=['GET'])
def get_pipeline_status(campaign_id: str):
    """Get current pipeline progress for a campaign.

    Returns progress dict with current_step, step_status, persona_count, etc.
    """
    try:
        _get_org_id()  # Auth check

        orch = _get_pipeline_orchestrator()
        status = orch.get_pipeline_status(campaign_id)

        if status is None:
            return jsonify({'success': False, 'error': f'Campaign not found: {campaign_id}'}), 404

        return jsonify({
            'success': True,
            'data': status,
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Pipeline status error: {str(e)}")
        return jsonify({'success': False, 'error': str(e), 'traceback': traceback.format_exc()}), 500
