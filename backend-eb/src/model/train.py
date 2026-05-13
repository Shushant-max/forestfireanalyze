"""
Model training script for Forest Fire Detection
"""

import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from src.config.config import MODEL_PATH
from src.preprocessing.preprocess import load_and_preprocess_dataset
from src.model.architecture import create_model, save_model

def train_model():
    """
    Train the forest fire detection model
    """
    print("Creating demonstration model...")

    # Create model and scaler
    model, scaler = create_model()

    # Save the model
    save_model(model, scaler, MODEL_PATH)

    # Create dummy test data for evaluation
    np.random.seed(123)
    n_test_samples = 200
    n_features = 224 * 224 * 3

    X_test = np.random.rand(n_test_samples, n_features)
    y_test = np.random.randint(0, 2, n_test_samples)

    # Scale test data
    X_test_scaled = scaler.transform(X_test)

    # Make predictions
    y_pred = model.predict(X_test_scaled)

    # Calculate metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("\nModel Evaluation Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Fire', 'Fire']))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    print(f"\nModel saved to {MODEL_PATH}")
    print("Note: This is a demonstration model using random data.")
    print("For production use, replace with actual TensorFlow/Keras model.")

    return model
