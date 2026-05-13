from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.routes import api
from backend.auth import auth as auth_bp
from src.utils.helper import setup_logging
import os


def create_app():
    """
    Create and configure the Flask application
    """

    # Base directory
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Frontend directory
    frontend_dir = os.path.join(base_dir, 'frontend')

    # Flask app
    application = Flask(
        __name__,
        static_folder=frontend_dir,
        template_folder=frontend_dir
    )

    application.config['SECRET_KEY'] = os.environ.get(
        'FLASK_SECRET_KEY',
        'forest-fire-secret'
    )

    # Enable CORS
    CORS(application)

    # Setup logging
    setup_logging()

    # Register blueprints
    application.register_blueprint(api, url_prefix='/api')
    application.register_blueprint(auth_bp, url_prefix='/auth')

    print("Blueprints registered successfully")

    # Root route
    @application.route("/")
    def home():
        return jsonify({
            "message": "Forest Fire Backend Running Successfully"
        })

    # Serve frontend files
    @application.route('/<path:path>')
    def serve_frontend(path):

        file_path = os.path.join(frontend_dir, path)

        if os.path.exists(file_path):
            return send_from_directory(frontend_dir, path)

        return jsonify({
            "error": "Route not found"
        }), 404

    return application


# Elastic Beanstalk looks for 'application'
application = create_app()


if __name__ == '__main__':
    application.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )