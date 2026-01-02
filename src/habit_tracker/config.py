from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Data directory
DATA_DIR = BASE_DIR/"data"

# Habits file
DATA_PATH = BASE_DIR/"data"/"habits.json"