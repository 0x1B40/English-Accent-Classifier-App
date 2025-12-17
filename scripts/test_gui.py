#!/usr/bin/env python3
"""Test script for GUI functionality."""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from english_accent_classifier.gui import AccentClassifierGUI
import logging

# Set up basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_gui_creation():
    """Test GUI creation without mainloop."""
    try:
        print("Creating GUI instance...")
        gui = AccentClassifierGUI()

        print("Creating GUI widgets...")
        root = gui.create_gui()

        print("GUI created successfully!")
        print(f"Window title: {root.title()}")
        print(f"Window geometry: {root.geometry()}")

        # Clean up
        root.destroy()
        print("GUI test completed successfully")
        return True

    except Exception as e:
        print(f"Error during GUI test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gui_creation()
    sys.exit(0 if success else 1)
