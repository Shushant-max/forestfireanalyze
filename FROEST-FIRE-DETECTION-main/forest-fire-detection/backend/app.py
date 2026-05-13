"""
Flask application for Forest Fire Detection API
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes import api
from backend.auth import auth as auth_bp
from src.utils.helper import setup_logging
import os


def create_app():
    """
    Create and configure the Flask application

    Returns:
        Flask app instance
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    frontend_dir = os.path.join(base_dir, 'frontend')

    app = Flask(__name__, static_folder=frontend_dir, template_folder=frontend_dir)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'forest-fire-secret')

    # Enable CORS
    CORS(app)

    # Setup logging
    setup_logging()

    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != '' and os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        return send_from_directory(frontend_dir, 'index.html')

    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
