#!/usr/bin/env python3
"""Test YouTube download functionality."""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from english_accent_classifier.audio_processor import AudioProcessor
import logging

logging.basicConfig(level=logging.INFO)


def test_download():
    """Test downloading from a known working YouTube video."""
    try:
        print("Initializing audio processor...")
        processor = AudioProcessor()

        # Try a few different URLs
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll - should work
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Another test video
        ]

        for url in test_urls:
            print(f"\nTesting URL: {url}")
            try:
                wav_path = processor.download_and_convert_to_wav(url)
                print(f"Success! WAV file created at: {wav_path}")

                # Check file size
                if os.path.exists(wav_path):
                    size = os.path.getsize(wav_path)
                    print(f"File size: {size} bytes")

                    # Clean up
                    processor.cleanup_temp_file(wav_path)
                    print("File cleaned up")
                    break  # Success, no need to try more URLs

            except Exception as e:
                print(f"Failed for URL {url}: {e}")
                continue

    except Exception as e:
        print(f"Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_download()
