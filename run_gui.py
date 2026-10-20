#!/usr/bin/env python3
"""
Main launcher script for the Reversible Data Hiding (RDH) Application.
Usage:
    .venv/bin/python run_gui.py
"""

import os
import sys

# Ensure current directory is on PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from implementation.app_gui import main

if __name__ == "__main__":
    main()
