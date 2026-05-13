"""
API routes for Forest Fire Detection
"""

import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from src.model.predict import predict_fire
from src.utils.helper import log_prediction, validate_image_file

api = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/predict', methods=['POST'])
def predict():
    """
    Predict fire in uploaded image

    Returns:
        JSON response with prediction results
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        # Validate image
        if not validate_image_file(temp_path):
            os.remove(temp_path)
            return jsonify({'error': 'Invalid image file'}), 400

        # Make prediction
        result = predict_fire(temp_path)

        # Log prediction
        log_prediction(temp_path, result['prediction'], result['confidence'])

        # Clean up temp file
        os.remove(temp_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint

    Returns:
        JSON response with service status
    """
    return jsonify({'status': 'healthy', 'service': 'Forest Fire Detection API'})

@api.route('/model-info', methods=['GET'])
def model_info():
    """
    Get model information

    Returns:
        JSON response with model details
    """
    from src.utils.helper import get_model_info
    info = get_model_info()
    return jsonify(info)
