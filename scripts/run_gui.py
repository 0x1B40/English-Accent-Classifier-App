#!/usr/bin/env python3
"""Entry point script for running the English Accent Classifier GUI."""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from english_accent_classifier.gui import run_gui

if __name__ == "__main__":
    run_gui()
