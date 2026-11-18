#!/usr/bin/env python3
"""
Launcher script for the Reversible Data Hiding Web Interface.
Runs Flask server and prints access URL.
Usage:
    .venv/bin/python run_web.py
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from web_gui.app import app

if __name__ == "__main__":
    port = 5000
    print("\n" + "=" * 65)
    print("  REVERSIBLE DATA HIDING - MODERN WEB INTERFACE")
    print("=" * 65)
    print(f"  Access URL : http://127.0.0.1:{port}")
    print("  Open the URL in any browser for live demonstration.")
    print("=" * 65 + "\n")
    app.run(host="127.0.0.1", port=port, debug=False)
