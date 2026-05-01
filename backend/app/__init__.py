"""
3C Simulator Backend — Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings (from third-party libraries like transformers)
# Must be set before all other imports
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure JSON encoding: ensure Chinese displays directly (not as \uXXXX)
    # Flask >= 2.3 uses app.json.ensure_ascii, older versions use JSON_AS_ASCII config
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # Setup logging
    logger = setup_logger('mirofish')

    # Only print startup info in reloader subprocess (avoid printing twice in debug mode)
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("3C Simulator Backend starting...")
        logger.info("=" * 50)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Initialize Neo4jStorage singleton (DI via app.extensions) ---
    from .storage import Neo4jStorage
    try:
        neo4j_storage = Neo4jStorage()
        app.extensions['neo4j_storage'] = neo4j_storage
        if should_log_startup:
            logger.info("Neo4jStorage initialized (connected to %s)", Config.NEO4J_URI)
    except Exception as e:
        logger.error("Neo4jStorage initialization failed: %s", e)
        # Store None so endpoints can return 503 gracefully
        app.extensions['neo4j_storage'] = None

    # Register simulation process cleanup function (ensure all simulation processes terminate on server shutdown)
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Simulation process cleanup function registered")

    # --- Tenant Middleware (auth + org scoping) ---
    # Must run BEFORE logging and blueprints so g.current_user is available
    from .middleware.tenant_middleware import TenantMiddleware
    TenantMiddleware(app)
    if should_log_startup:
        logger.info("Tenant middleware registered (JWT + API Key auth)")

    # Request logging middleware
    @app.before_request
    def log_request():
        logger = get_logger('mirofish.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")

    @app.after_request
    def log_response(response):
        logger = get_logger('mirofish.request')
        logger.debug(f"Response: {response.status_code}")
        return response

    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp, dashboard_bp
    from .api.settings import settings_bp
    from .api.auth import auth_bp
    from .api.persona import persona_bp
    from .api.campaign import campaign_bp
    from .api.industry import industry_bp
    from .api.comparator import comparator_bp
    from .api.impact import impact_bp
    from .api.competitor import competitor_bp
    from .api.export import export_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(persona_bp, url_prefix='/api/persona')
    app.register_blueprint(campaign_bp, url_prefix='/api/campaign')
    app.register_blueprint(industry_bp, url_prefix='/api/industry')
    app.register_blueprint(comparator_bp, url_prefix='/api/comparator')
    app.register_blueprint(impact_bp, url_prefix='/api/impact')
    app.register_blueprint(competitor_bp, url_prefix='/api/competitor')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': '3C Simulator Backend'}

    if should_log_startup:
        logger.info("3C Simulator Backend startup complete")

    return app
