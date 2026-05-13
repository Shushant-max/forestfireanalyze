"""
Helper utilities for Forest Fire Detection System
"""

import os
import logging
from datetime import datetime
from src.config.config import LOGS_DIR, PREDICTIONS_LOG

def setup_logging():
    """
    Setup logging configuration
    """
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
    except OSError:
        pass  # Read-only file system on Vercel

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_prediction(image_path, prediction, confidence):
    """
    Log a prediction result

    Args:
        image_path (str): Path to the processed image
        prediction (str): Prediction result
        confidence (float): Confidence score
    """
    logging.info(f"Prediction: {prediction}, Confidence: {confidence:.4f}, Image: {image_path}")

def create_directories():
    """
    Create necessary directories if they don't exist
    """
    directories = [
        'data/raw/fire',
        'data/raw/no_fire',
        'data/processed',
        'models',
        'logs',
        'tests'
    ]

    for dir_path in directories:
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            pass  # Ignore on read-only file systems

def validate_image_file(file_path):
    """
    Validate if the file is a valid image

    Args:
        file_path (str): Path to the file

    Returns:
        bool: True if valid image, False otherwise
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    if not os.path.exists(file_path):
        return False

    _, ext = os.path.splitext(file_path.lower())
    return ext in valid_extensions

def format_confidence(confidence):
    """
    Format confidence score for display

    Args:
        confidence (float): Confidence score between 0 and 1

    Returns:
        str: Formatted confidence percentage
    """
    return f"{confidence * 100:.1f}%"

def get_model_info():
    """
    Get information about the trained model

    Returns:
        dict: Model information
    """
    model_path = 'models/trained_model.h5'
    if os.path.exists(model_path):
        model_size = os.path.getsize(model_path) / (1024 * 1024)  # Size in MB
        modified_time = datetime.fromtimestamp(os.path.getmtime(model_path))

        return {
            'exists': True,
            'size_mb': round(model_size, 2),
            'last_modified': modified_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        return {
            'exists': False,
            'message': 'Model not found. Please train the model first.'
        }
