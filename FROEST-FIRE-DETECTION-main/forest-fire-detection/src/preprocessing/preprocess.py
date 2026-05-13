"""
Image preprocessing utilities for Forest Fire Detection
"""

import cv2
import numpy as np
from src.config.config import IMG_HEIGHT, IMG_WIDTH

def preprocess_image(image_path):
    """
    Preprocess a single image for prediction

    Args:
        image_path (str): Path to the image file

    Returns:
        numpy.ndarray: Preprocessed image array (flattened for Random Forest)
    """
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from {image_path}")

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize image
    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

    # Normalize pixel values to [0, 1]
    image = image.astype(np.float32) / 255.0

    # Flatten the image for Random Forest model
    flattened_image = image.flatten()

    # Add batch dimension (though Random Forest expects 2D)
    flattened_image = np.expand_dims(flattened_image, axis=0)

    return flattened_image

def create_data_generators(train_dir, val_dir=None, test_dir=None):
    """
    Create data generators for training, validation, and testing
    Note: Simplified for demonstration without TensorFlow
    """
    print("Data generators not implemented for demonstration version.")
    print("Using random data instead.")
    return None, None, None

def load_and_preprocess_dataset(data_dir):
    """
    Load and preprocess the entire dataset

    Args:
        data_dir (str): Path to the data directory

    Returns:
        tuple: (X_train, y_train, X_val, y_val, X_test, y_test)
    """
    # This is a placeholder - in a real scenario, you'd load actual data
    # For demonstration, we'll create dummy data
    import os
    from sklearn.model_selection import train_test_split

    # Check if data exists
    fire_dir = os.path.join(data_dir, 'fire')
    no_fire_dir = os.path.join(data_dir, 'no_fire')

    if not os.path.exists(fire_dir) or not os.path.exists(no_fire_dir):
        print("Warning: Data directories not found. Using dummy data for demonstration.")
        # Create dummy data
        X = np.random.rand(1000, IMG_HEIGHT, IMG_WIDTH, 3)
        y = np.random.randint(0, 2, 1000)
    else:
        # Load actual images
        X = []
        y = []

        # Load fire images
        for img_file in os.listdir(fire_dir)[:500]:  # Limit for demo
            img_path = os.path.join(fire_dir, img_file)
            try:
                img = preprocess_image(img_path).squeeze()
                X.append(img)
                y.append(1)  # Fire
            except:
                continue

        # Load no_fire images
        for img_file in os.listdir(no_fire_dir)[:500]:  # Limit for demo
            img_path = os.path.join(no_fire_dir, img_file)
            try:
                img = preprocess_image(img_path).squeeze()
                X.append(img)
                y.append(0)  # No fire
            except:
                continue

        X = np.array(X)
        y = np.array(y)

    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    return X_train, y_train, X_val, y_val, X_test, y_test
