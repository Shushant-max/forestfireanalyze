import sys
import os

# Add the project directory to sys.path so imports like 'from backend' and 'from src' work
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, 'FROEST-FIRE-DETECTION-main', 'forest-fire-detection')
sys.path.append(project_dir)

# Change working directory to the project folder so it can find 'data', 'models', etc.
try:
    os.chdir(project_dir)
except OSError:
    pass

# Import the actual Flask app
from backend.app import application as app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
