#!/usr/bin/env python3
"""
Forest Fire Detection System - Main Entry Point

This script serves as the main entry point for the Forest Fire Detection System.
It provides options to train the model, run the backend server, or run tests.

Usage:
    python main.py --train          # Train the model
    python main.py --server         # Run the backend server
    python main.py --test           # Run tests
    python main.py --demo           # Run a demo prediction
"""

import argparse
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    parser = argparse.ArgumentParser(description='Forest Fire Detection System')
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--server', action='store_true', help='Run the backend server')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--demo', action='store_true', help='Run demo prediction')

    args = parser.parse_args()

    if args.train:
        from src.model.train import train_model
        print("Starting model training...")
        train_model()
        print("Training completed!")

    elif args.server:
        from backend.app import app
        print("Starting backend server...")
        app.run(host='0.0.0.0', port=5000, debug=True)

    elif args.test:
        import subprocess
        print("Running tests...")
        result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/'], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

    elif args.demo:
        from src.model.predict import predict_fire
        # For demo, assume an image path
        image_path = 'data/raw/sample_fire.jpg'  # You need to provide a sample image
        if os.path.exists(image_path):
            result = predict_fire(image_path)
            print(f"Prediction: {result['prediction']}, Confidence: {result['confidence']:.2f}")
        else:
            print("Sample image not found. Please provide an image in data/raw/")

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
