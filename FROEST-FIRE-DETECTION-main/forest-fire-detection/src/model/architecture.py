"""
Model architecture for Forest Fire Detection
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
from src.config.config import MODEL_PATH

def create_model():
    """
    Create a Random Forest classifier for demonstration
    (Since TensorFlow may not be available for Python 3.14)

    Returns:
        tuple: (model, scaler) - trained model and scaler
    """
    # Create dummy training data for demonstration
    np.random.seed(42)
    n_samples = 1000
    n_features = 224 * 224 * 3  # Flattened image size

    # Generate random features
    X = np.random.rand(n_samples, n_features)
    y = np.random.randint(0, 2, n_samples)

    # Create and train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Create scaler
    scaler = StandardScaler()
    scaler.fit(X)

    return model, scaler

def save_model(model, scaler, model_path=MODEL_PATH):
    """
    Save the model and scaler

    Args:
        model: Trained model
        scaler: Fitted scaler
        model_path: Path to save the model
    """
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    with open(model_path, 'wb') as f:
        pickle.dump({'model': model, 'scaler': scaler}, f)

    print(f"Model saved to {model_path}")

def load_model(model_path=MODEL_PATH):
    """
    Load a saved model

    Args:
        model_path (str): Path to the saved model

    Returns:
        tuple: (model, scaler) or None if not found
    """
    try:
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
        print(f"Model loaded successfully from {model_path}")
        return data['model'], data['scaler']
    except FileNotFoundError:
        print(f"Model not found at {model_path}. Creating new model...")
        model, scaler = create_model()
        save_model(model, scaler, model_path)
        return model, scaler
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None
