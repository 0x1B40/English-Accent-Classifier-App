#!/usr/bin/env python3
"""Test accent classification with a known file."""

import sys
import os
import tempfile

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from english_accent_classifier.accent_classifier import AccentClassifier
from english_accent_classifier.audio_processor import AudioProcessor
import logging

logging.basicConfig(level=logging.INFO)

def test_classification():
    """Test classification with a mock file."""
    try:
        print("Initializing classifier...")
        classifier = AccentClassifier()

        print("Creating a dummy WAV file...")
        # Create a temporary WAV file (even if it's empty, just to test path handling)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(b'dummy wav data')
            temp_path = temp_file.name

        print(f"Testing classification with file: {temp_path}")

        try:
            result, best_accent = classifier.classify_accent(temp_path)
            print(f"Classification successful: {best_accent}")
            print(f"Result: {result[:100]}...")
        except Exception as e:
            print(f"Classification failed: {e}")
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_classification()
