import os
import sys

# Ensure current directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import application

if __name__ == '__main__':
    # For local testing
    application.run(host='0.0.0.0', port=5000, debug=True)
