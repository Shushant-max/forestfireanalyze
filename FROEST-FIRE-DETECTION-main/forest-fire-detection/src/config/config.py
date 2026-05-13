"""
Configuration file for Forest Fire Detection System
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Model parameters
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

# Model paths
MODEL_PATH = os.path.join(MODELS_DIR, 'trained_model.h5')

# Data paths
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Log paths
PREDICTIONS_LOG = os.path.join(LOGS_DIR, 'predictions.log')

# Classes
CLASSES = ['no_fire', 'fire']
NUM_CLASSES = len(CLASSES)

# API settings
API_HOST = '0.0.0.0'
API_PORT = 5000
API_DEBUG = True
