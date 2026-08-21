"""
Prospect Intelligence OS Configuration Settings
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "prospect_intelligence.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

DEFAULT_DAILY_CAP_PER_MAILBOX = 40
MAX_PARALLEL_WORKERS = 20

# Create required directories
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
