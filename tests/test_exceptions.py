"""Tests for custom exceptions."""

import unittest

from english_accent_classifier.exceptions import (
    AccentClassifierError,
    DependencyError,
    AudioProcessingError,
    DownloadError,
    ClassificationError,
)


class TestExceptions(unittest.TestCase):
    """Test cases for custom exceptions."""

    def test_base_exception(self):
        """Test base AccentClassifierError."""
        error = AccentClassifierError("Test error")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error")

    def test_dependency_error(self):
        """Test DependencyError."""
        error = DependencyError("Missing dependency")
        self.assertIsInstance(error, AccentClassifierError)
        self.assertEqual(str(error), "Missing dependency")

    def test_audio_processing_error(self):
        """Test AudioProcessingError."""
        error = AudioProcessingError("Audio processing failed")
        self.assertIsInstance(error, AccentClassifierError)
        self.assertEqual(str(error), "Audio processing failed")

    def test_download_error(self):
        """Test DownloadError."""
        error = DownloadError("Download failed")
        self.assertIsInstance(error, AccentClassifierError)
        self.assertEqual(str(error), "Download failed")

    def test_classification_error(self):
        """Test ClassificationError."""
        error = ClassificationError("Classification failed")
        self.assertIsInstance(error, AccentClassifierError)
        self.assertEqual(str(error), "Classification failed")

    def test_exception_hierarchy(self):
        """Test that all exceptions inherit from AccentClassifierError."""
        exceptions = [
            DependencyError("test"),
            AudioProcessingError("test"),
            DownloadError("test"),
            ClassificationError("test"),
        ]

        for exc in exceptions:
            with self.subTest(exception=exc):
                self.assertIsInstance(exc, AccentClassifierError)


if __name__ == "__main__":
    unittest.main()
