#!/usr/bin/env python3
"""Entry point for the English Accent Classifier GUI application.

This script maintains backward compatibility while using the new modular structure.
"""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from english_accent_classifier.gui import run_gui

if __name__ == "__main__":
    run_gui()
