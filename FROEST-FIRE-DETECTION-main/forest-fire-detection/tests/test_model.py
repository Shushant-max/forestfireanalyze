"""
Unit tests for Forest Fire Detection Model
"""

import unittest
import numpy as np
import os
import tempfile
from PIL import Image
from src.preprocessing.preprocess import preprocess_image
from src.model.architecture import create_model
from src.model.predict import predict_fire
from src.utils.helper import validate_image_file

class TestModel(unittest.TestCase):
    """Test cases for the model functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_image_path = None

    def tearDown(self):
        """Clean up test fixtures"""
        if self.test_image_path and os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)

    def create_test_image(self, width=224, height=224, color=(255, 0, 0)):
        """Create a test image for testing"""
        image = Image.new('RGB', (width, height), color=color)
        self.test_image_path = tempfile.mktemp(suffix='.jpg')
        image.save(self.test_image_path)
        return self.test_image_path

    def test_preprocess_image(self):
        """Test image preprocessing"""
        # Create test image
        image_path = self.create_test_image()

        # Test preprocessing
        processed = preprocess_image(image_path)

        # Check shape (flattened for Random Forest)
        expected_size = 224 * 224 * 3  # 150528
        self.assertEqual(processed.shape, (1, expected_size))

        # Check value range
        self.assertTrue(np.all(processed >= 0))
        self.assertTrue(np.all(processed <= 1))

    def test_validate_image_file(self):
        """Test image file validation"""
        # Test valid image
        image_path = self.create_test_image()
        self.assertTrue(validate_image_file(image_path))

        # Test invalid file
        invalid_path = tempfile.mktemp(suffix='.txt')
        with open(invalid_path, 'w') as f:
            f.write('not an image')
        self.assertFalse(validate_image_file(invalid_path))
        os.remove(invalid_path)

        # Test non-existent file
        self.assertFalse(validate_image_file('non_existent.jpg'))

    def test_model_creation(self):
        """Test model creation"""
        model, scaler = create_model()

        # Check model is not None
        self.assertIsNotNone(model)
        self.assertIsNotNone(scaler)

        # Check model type
        self.assertEqual(str(type(model)), "<class 'sklearn.ensemble._forest.RandomForestClassifier'>")

    def test_model_prediction_shape(self):
        """Test model prediction output shape"""
        model, scaler = create_model()
        image_path = self.create_test_image()
        processed = preprocess_image(image_path)

        # Scale the features
        scaled_image = scaler.transform(processed)

        prediction = model.predict_proba(scaled_image)

        # Check prediction shape (probability for both classes)
        self.assertEqual(prediction.shape, (1, 2))

        # Check prediction value range
        self.assertTrue(np.all(prediction >= 0))
        self.assertTrue(np.all(prediction <= 1))

    def test_predict_fire_without_model(self):
        """Test prediction when model doesn't exist"""
        # This should raise an error
        with self.assertRaises(ValueError):
            predict_fire('non_existent.jpg')

    def test_image_validation(self):
        """Test various image validation scenarios"""
        # Test with different image formats
        formats = ['.jpg', '.jpeg', '.png']

        for ext in formats:
            with self.subTest(ext=ext):
                image_path = tempfile.mktemp(suffix=ext)
                image = Image.new('RGB', (100, 100), color=(255, 255, 255))
                image.save(image_path)

                self.assertTrue(validate_image_file(image_path))
                os.remove(image_path)

class TestPreprocessing(unittest.TestCase):
    """Test cases for preprocessing functions"""

    def test_preprocessing_normalization(self):
        """Test that preprocessing normalizes values to [0,1]"""
        # Create image with values > 1 (if any)
        image = Image.new('RGB', (224, 224), color=(255, 255, 255))
        temp_path = tempfile.mktemp(suffix='.jpg')
        image.save(temp_path)

        try:
            processed = preprocess_image(temp_path)
            # Check all values are between 0 and 1
            self.assertTrue(np.all(processed >= 0))
            self.assertTrue(np.all(processed <= 1))
        finally:
            os.remove(temp_path)

    def test_preprocessing_resize(self):
        """Test that preprocessing resizes images correctly"""
        # Create image with different size
        image = Image.new('RGB', (100, 100), color=(255, 0, 0))
        temp_path = tempfile.mktemp(suffix='.jpg')
        image.save(temp_path)

        try:
            processed = preprocess_image(temp_path)
            # Check dimensions (flattened size should be 224*224*3 = 150528)
            expected_size = 224 * 224 * 3
            self.assertEqual(processed.shape, (1, expected_size))
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    unittest.main()
