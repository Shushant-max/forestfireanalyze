"""
Prediction module for Forest Fire Detection
"""

import numpy as np
from src.config.config import MODEL_PATH, CLASSES
from src.preprocessing.preprocess import preprocess_image
from src.model.architecture import load_model

def predict_fire(image_path):
    """
    Predict if an image contains fire

    Args:
        image_path (str): Path to the image file

    Returns:
        dict: Prediction results with 'prediction' and 'confidence'
    """
    # Load model and scaler
    model, scaler = load_model(MODEL_PATH)
    if model is None:
        raise ValueError("Model could not be loaded. Please train the model first.")

    # Preprocess image
    processed_image = preprocess_image(image_path)

    # Flatten the image for the Random Forest model
    flattened_image = processed_image.reshape(1, -1)

    # Scale the features
    scaled_image = scaler.transform(flattened_image)

    # Make prediction
    prediction_prob = model.predict_proba(scaled_image)[0][1]  # Probability of fire (class 1)

    # Determine class
    if prediction_prob > 0.5:
        prediction = CLASSES[1]  # 'fire'
        confidence = prediction_prob
    else:
        prediction = CLASSES[0]  # 'no_fire'
        confidence = 1 - prediction_prob

    # Format prediction text
    prediction_text = "Fire Detected" if prediction == 'fire' else "No Fire"

    return {
        'prediction': prediction_text,
        'confidence': float(confidence)
    }

def predict_with_heatmap(image_path):
    """
    Predict with heatmap visualization (optional advanced feature)

    Args:
        image_path (str): Path to the image file

    Returns:
        dict: Prediction results with heatmap data
    """
    # This is a placeholder for advanced heatmap functionality
    # In a real implementation, you'd use Grad-CAM or similar techniques

    basic_result = predict_fire(image_path)

    # Add dummy heatmap data (in practice, compute actual heatmap)
    basic_result['heatmap'] = None  # Would be a numpy array

    return basic_result

def batch_predict(image_paths):
    """
    Predict for multiple images

    Args:
        image_paths (list): List of image file paths

    Returns:
        list: List of prediction results
    """
    results = []
    for path in image_paths:
        try:
            result = predict_fire(path)
            result['image_path'] = path
            results.append(result)
        except Exception as e:
            results.append({
                'image_path': path,
                'error': str(e)
            })

    return results
