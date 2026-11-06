"""
Mini Search Engine Root Launcher
Forwards to mini_search_engine/app.py
"""

import sys
from pathlib import Path

# Add mini_search_engine to sys.path
PROJECT_DIR = Path(__file__).resolve().parent / "mini_search_engine"
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from app import main

if __name__ == "__main__":
    main()
