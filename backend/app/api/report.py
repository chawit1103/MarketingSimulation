"""
Report API Routes
Provides interfaces for simulation report generation, retrieval, and conversation
"""

import os
import traceback
import threading
from flask import request, jsonify, send_file, current_app, g

from . import report_bp
from ..config import Config
from ..services.report_agent import ReportAgent, ReportManager, ReportStatus
from ..services.simulation_manager import SimulationManager
from ..services.audit_log_service import record_audit_event
from ..models.project import ProjectManager
from ..models.task import TaskManager, TaskStatus
from ..services.graph_tools import GraphToolsService
from ..authz import ADMIN_ROLES, ANALYST_ROLES, role_required
from ..utils.logger import get_logger

logger = get_logger('mirofish.api.report')


def _get_org_id() -> str:
    org_id = g.get("current_org_id")
    if not org_id and g.get("current_user"):
        org_id = g.current_user.get("org_id")
    if not org_id:
        raise ValueError("Authentication required")
    return org_id


def _resource_not_found():
    return jsonify({"success": False, "error": "Resource not found"}), 404


def _get_owned_simulation(manager: SimulationManager, simulation_id: str):
    return manager.get_simulation(simulation_id, org_id=_get_org_id())


def _get_owned_report(report_id: str):
    return ReportManager.get_report(report_id, org_id=_get_org_id())


# ============== Report Generation Interface ==============

@report_bp.route('/generate', methods=['POST'])
@role_required(*ANALYST_ROLES)
def generate_report():
    try:
        data = request.get_json() or {}
        simulation_id = data.get('simulation_id')
        if not simulation_id:
            return jsonify({"success": False, "error": "Please provide simulation_id"}), 400

        force_regenerate = data.get('force_regenerate', False)
        language = data.get('language', 'en')
        org_id = _get_org_id()
        manager = SimulationManager()
        state = manager.get_simulation(simulation_id, org_id=org_id)
        if not state:
            return _resource_not_found()

        if not force_regenerate:
            existing_report = ReportManager.get_report_by_simulation(simulation_id, org_id=org_id)
            if existing_report and existing_report.status == ReportStatus.COMPLETED:
                return jsonify({"success": True, "data": {
                    "simulation_id": simulation_id,
                    "report_id": existing_report.report_id,
                    "status": "completed",
                    "message": "Report already exists",
                    "already_generated": True
                }})

        project = ProjectManager.get_project(state.project_id, org_id=org_id)
        if not project:
            return _resource_not_found()

        graph_id = state.graph_id or project.graph_id
        if not graph_id:
            return jsonify({"success": False, "error": "Missing graph ID, please ensure graph is built"}), 400

        simulation_requirement = project.simulation_requirement
        if not simulation_requirement:
            return jsonify({"success": False, "error": "Missing simulation requirement description"}), 400

        import uuid
        report_id = f"report_{uuid.uuid4().hex[:12]}"

        task_manager = TaskManager()
        task_id = task_manager.create_task(
            task_type="report_generate",
            metadata={"simulation_id": simulation_id, "graph_id": graph_id, "report_id": report_id, "org_id": org_id}
        )

        # Initialize graph_tools in Flask context BEFORE spawning thread
        # (current_app is not available inside background threads)
        storage = current_app.extensions.get('neo4j_storage')
        if not storage:
            return jsonify({"success": False, "error": "GraphStorage not initialized — check Neo4j connection"}), 500
        graph_tools = GraphToolsService(storage=storage)

        def run_generate():
            try:
                task_manager.update_task(task_id, status=TaskStatus.PROCESSING, progress=0, message="Initializing Report Agent...")
                agent = ReportAgent(
                    graph_id=graph_id,
                    simulation_id=simulation_id,
                    simulation_requirement=simulation_requirement,
                    graph_tools=graph_tools,
                    language=language,
                    org_id=org_id,
                    campaign_id=state.campaign_id,
                )
                def progress_callback(stage, progress, message):
                    task_manager.update_task(task_id, progress=progress, message=f"[{stage}] {message}")
                report = agent.generate_report(progress_callback=progress_callback, report_id=report_id)
                ReportManager.save_report(report)
                if report.status == ReportStatus.COMPLETED:
                    task_manager.complete_task(task_id, result={"report_id": report.report_id, "simulation_id": simulation_id, "status": "completed"})
                else:
                    task_manager.fail_task(task_id, report.error or "Report generation failed")
            except Exception as e:
                logger.error(f"Report generation failed: {str(e)}")
                task_manager.fail_task(task_id, str(e))

        thread = threading.Thread(target=run_generate, daemon=True)
        thread.start()
        record_audit_event(
            org_id=org_id,
            event_type="report_generation_started",
            resource_type="report",
            resource_id=report_id,
            metadata={
                "simulation_id": simulation_id,
                "campaign_id": state.campaign_id,
                "force_regenerate": bool(force_regenerate),
                "language": language,
            },
        )

        return jsonify({"success": True, "data": {
            "simulation_id": simulation_id,
            "report_id": report_id,
            "task_id": task_id,
            "status": "generating",
            "message": "Report generation task started. Query progress via /api/report/generate/status",
            "already_generated": False
        }})

    except Exception as e:
        logger.error(f"Failed to start report generation task: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/generate/status', methods=['POST'])
def get_generate_status():
    try:
        data = request.get_json() or {}
        task_id = data.get('task_id')
        simulation_id = data.get('simulation_id')
        org_id = _get_org_id()

        if simulation_id:
            if not _get_owned_simulation(SimulationManager(), simulation_id):
                return _resource_not_found()
            existing_report = ReportManager.get_report_by_simulation(simulation_id, org_id=org_id)
            if existing_report and existing_report.status == ReportStatus.COMPLETED:
                return jsonify({"success": True, "data": {
                    "simulation_id": simulation_id,
                    "report_id": existing_report.report_id,
                    "status": "completed",
                    "progress": 100,
                    "message": "Report generated",
                    "already_completed": True
                }})

        if not task_id:
            return jsonify({"success": False, "error": "Please provide task_id or simulation_id"}), 400

        task_manager = TaskManager()
        task = task_manager.get_task(task_id)
        if not task or task.metadata.get("org_id") != org_id:
            return _resource_not_found()

        task_dict = task.to_dict()
        if isinstance(task_dict.get("metadata"), dict):
            task_dict["metadata"].pop("org_id", None)
        return jsonify({"success": True, "data": task_dict})

    except Exception as e:
        logger.error(f"Failed to query task status: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============== Report Retrieval Interface ==============

@report_bp.route('/<report_id>', methods=['GET'])
def get_report(report_id: str):
    try:
        report = _get_owned_report(report_id)
        if not report:
            return _resource_not_found()
        return jsonify({"success": True, "data": report.to_dict()})
    except Exception as e:
        logger.error(f"Failed to get report: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/by-simulation/<simulation_id>', methods=['GET'])
def get_report_by_simulation(simulation_id: str):
    try:
        org_id = _get_org_id()
        if not _get_owned_simulation(SimulationManager(), simulation_id):
            return _resource_not_found()
        report = ReportManager.get_report_by_simulation(simulation_id, org_id=org_id)
        if not report:
            return jsonify({"success": False, "error": "Resource not found", "has_report": False}), 404
        return jsonify({"success": True, "data": report.to_dict()})
    except Exception as e:
        logger.error(f"Failed to get report: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/list', methods=['GET'])
def list_reports():
    try:
        simulation_id = request.args.get('simulation_id')
        limit = request.args.get('limit', 50, type=int)
        org_id = _get_org_id()
        if simulation_id and not _get_owned_simulation(SimulationManager(), simulation_id):
            return _resource_not_found()
        reports = ReportManager.list_reports(simulation_id=simulation_id, limit=limit, org_id=org_id)
        return jsonify({"success": True, "data": [r.to_dict() for r in reports], "count": len(reports)})
    except Exception as e:
        logger.error(f"Failed to list reports: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>/download', methods=['GET'])
def download_report(report_id: str):
    try:
        report = _get_owned_report(report_id)
        if not report:
            return _resource_not_found()
        record_audit_event(
            org_id=_get_org_id(),
            event_type="report_downloaded",
            resource_type="report",
            resource_id=report_id,
            metadata={
                "simulation_id": report.simulation_id,
                "campaign_id": report.campaign_id,
                "format": "markdown",
            },
        )

        md_path = ReportManager._get_report_markdown_path(report_id)
        if not os.path.exists(md_path):
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write(report.markdown_content)
                temp_path = f.name
            return send_file(temp_path, as_attachment=True, download_name=f"{report_id}.md")

        return send_file(md_path, as_attachment=True, download_name=f"{report_id}.md")

    except Exception as e:
        logger.error(f"Failed to download report: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>', methods=['DELETE'])
@role_required(*ADMIN_ROLES)
def delete_report(report_id: str):
    try:
        success = ReportManager.delete_report(report_id, org_id=_get_org_id())
        if not success:
            return _resource_not_found()
        return jsonify({"success": True, "message": "Report deleted"})
    except Exception as e:
        logger.error(f"Failed to delete report: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Report Agent Chat Interface ==============

@report_bp.route('/chat', methods=['POST'])
@role_required(*ANALYST_ROLES)
def chat_with_report_agent():
    try:
        data = request.get_json() or {}
        simulation_id = data.get('simulation_id')
        message = data.get('message')
        chat_history = data.get('chat_history', [])
        language = data.get('language', 'en')

        if not simulation_id:
            return jsonify({"success": False, "error": "Please provide simulation_id"}), 400
        if not message:
            return jsonify({"success": False, "error": "Please provide message"}), 400

        manager = SimulationManager()
        state = manager.get_simulation(simulation_id, org_id=_get_org_id())
        if not state:
            return _resource_not_found()

        project = ProjectManager.get_project(state.project_id, org_id=_get_org_id())
        if not project:
            return _resource_not_found()

        graph_id = state.graph_id or project.graph_id
        if not graph_id:
            return jsonify({"success": False, "error": "Missing graph ID"}), 400

        simulation_requirement = project.simulation_requirement or ""

        storage = current_app.extensions.get('neo4j_storage')
        if not storage:
            raise ValueError("GraphStorage not initialized — check Neo4j connection")
        graph_tools = GraphToolsService(storage=storage)

        agent = ReportAgent(
            graph_id=graph_id,
            simulation_id=simulation_id,
            simulation_requirement=simulation_requirement,
            graph_tools=graph_tools,
            language=language,
            org_id=_get_org_id(),
            campaign_id=state.campaign_id,
        )

        result = agent.chat(message=message, chat_history=chat_history)
        return jsonify({"success": True, "data": {"response": result, "simulation_id": simulation_id}})

    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Report Progress and Section Retrieval Interface ==============

@report_bp.route('/<report_id>/progress', methods=['GET'])
def get_report_progress(report_id: str):
    try:
        if not _get_owned_report(report_id):
            return _resource_not_found()
        progress = ReportManager.get_progress(report_id)
        if not progress:
            return _resource_not_found()
        return jsonify({"success": True, "data": progress})
    except Exception as e:
        logger.error(f"Failed to get report progress: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>/sections', methods=['GET'])
def get_report_sections(report_id: str):
    try:
        report = _get_owned_report(report_id)
        if not report:
            return _resource_not_found()
        sections = ReportManager.get_generated_sections(report_id)
        is_complete = report is not None and report.status == ReportStatus.COMPLETED
        return jsonify({"success": True, "data": {
            "report_id": report_id,
            "sections": sections,
            "total": len(sections),
            "is_complete": is_complete
        }})
    except Exception as e:
        logger.error(f"Failed to get section list: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>/section/<int:section_index>', methods=['GET'])
def get_single_section(report_id: str, section_index: int):
    try:
        section_path = ReportManager._get_section_path(report_id, section_index)
        if not _get_owned_report(report_id):
            return _resource_not_found()
        if not os.path.exists(section_path):
            return _resource_not_found()
        with open(section_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({"success": True, "data": {"filename": f"section_{section_index:02d}.md", "content": content}})
    except Exception as e:
        logger.error(f"Failed to get section content: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Report Status Check Interface ==============

@report_bp.route('/check/<simulation_id>', methods=['GET'])
def check_report_status(simulation_id: str):
    try:
        org_id = _get_org_id()
        if not _get_owned_simulation(SimulationManager(), simulation_id):
            return _resource_not_found()
        report = ReportManager.get_report_by_simulation(simulation_id, org_id=org_id)
        has_report = report is not None
        report_status = report.status.value if report and hasattr(report.status, 'value') else (report.status if report else None)
        report_id = report.report_id if report else None
        interview_unlocked = has_report and report.status == ReportStatus.COMPLETED
        return jsonify({"success": True, "data": {
            "simulation_id": simulation_id,
            "has_report": has_report,
            "report_id": report_id,
            "report_status": report_status,
            "interview_unlocked": interview_unlocked
        }})
    except Exception as e:
        logger.error(f"Failed to check report status: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Agent Log Interface ==============

@report_bp.route('/<report_id>/agent-log', methods=['GET'])
def get_agent_log(report_id: str):
    try:
        from_line = request.args.get('from_line', 0, type=int)
        if not _get_owned_report(report_id):
            return _resource_not_found()
        log_data = ReportManager.get_agent_log(report_id, from_line=from_line)
        return jsonify({"success": True, "data": log_data})
    except Exception as e:
        logger.error(f"Failed to get agent log: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>/agent-log/stream', methods=['GET'])
def stream_agent_log(report_id: str):
    try:
        if not _get_owned_report(report_id):
            return _resource_not_found()
        logs = ReportManager.get_agent_log_stream(report_id)
        return jsonify({"success": True, "data": {"logs": logs, "count": len(logs)}})
    except Exception as e:
        logger.error(f"Failed to get agent log: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Console Log Interface ==============

@report_bp.route('/<report_id>/console-log', methods=['GET'])
def get_console_log(report_id: str):
    try:
        from_line = request.args.get('from_line', 0, type=int)
        if not _get_owned_report(report_id):
            return _resource_not_found()
        log_data = ReportManager.get_console_log(report_id, from_line=from_line)
        return jsonify({"success": True, "data": log_data})
    except Exception as e:
        logger.error(f"Failed to get console log: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/<report_id>/console-log/stream', methods=['GET'])
def stream_console_log(report_id: str):
    try:
        if not _get_owned_report(report_id):
            return _resource_not_found()
        logs = ReportManager.get_console_log_stream(report_id)
        return jsonify({"success": True, "data": {"logs": logs, "count": len(logs)}})
    except Exception as e:
        logger.error(f"Failed to get console log: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


# ============== Tool Call Interface (For Debugging) ==============

@report_bp.route('/tools/search', methods=['POST'])
@role_required(*ANALYST_ROLES)
def search_graph_tool():
    try:
        data = request.get_json() or {}
        graph_id = data.get('graph_id')
        query = data.get('query')
        limit = data.get('limit', 10)
        if not graph_id or not query:
            return jsonify({"success": False, "error": "Please provide graph_id and query"}), 400
        storage = current_app.extensions.get('neo4j_storage')
        if not storage:
            raise ValueError("GraphStorage not initialized — check Neo4j connection")
        tools = GraphToolsService(storage=storage)
        result = tools.search_graph(graph_id=graph_id, query=query, limit=limit)
        return jsonify({"success": True, "data": result.to_dict()})
    except Exception as e:
        logger.error(f"Graph search failed: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500


@report_bp.route('/tools/statistics', methods=['POST'])
@role_required(*ANALYST_ROLES)
def get_graph_statistics_tool():
    try:
        data = request.get_json() or {}
        graph_id = data.get('graph_id')
        if not graph_id:
            return jsonify({"success": False, "error": "Please provide graph_id"}), 400
        storage = current_app.extensions.get('neo4j_storage')
        if not storage:
            raise ValueError("GraphStorage not initialized — check Neo4j connection")
        tools = GraphToolsService(storage=storage)
        result = tools.get_graph_statistics(graph_id)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        logger.error(f"Failed to get graph statistics: {str(e)}")
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()}), 500
