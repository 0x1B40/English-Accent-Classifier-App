"""Tests for audio processor."""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from english_accent_classifier.audio_processor import AudioProcessor
from english_accent_classifier.exceptions import DependencyError, DownloadError, AudioProcessingError


class TestAudioProcessor(unittest.TestCase):
    """Test cases for AudioProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('english_accent_classifier.audio_processor.DEPENDENCIES_AVAILABLE', False)
    def test_missing_dependencies(self):
        """Test behavior when dependencies are not available."""
        with self.assertRaises(DependencyError):
            AudioProcessor()

    @patch('english_accent_classifier.audio_processor.DEPENDENCIES_AVAILABLE', True)
    def test_initialization(self):
        """Test AudioProcessor initialization."""
        processor = AudioProcessor(temp_dir=self.temp_dir)
        self.assertEqual(processor.temp_dir, self.temp_dir)

    @patch('english_accent_classifier.audio_processor.DEPENDENCIES_AVAILABLE', True)
    def test_cleanup_temp_file(self):
        """Test temporary file cleanup."""
        processor = AudioProcessor()

        # Create a temporary file
        temp_file = os.path.join(self.temp_dir, 'test.wav')
        with open(temp_file, 'w') as f:
            f.write('test')

        self.assertTrue(os.path.exists(temp_file))

        # Clean it up
        processor.cleanup_temp_file(temp_file)
        self.assertFalse(os.path.exists(temp_file))

    @patch('english_accent_classifier.audio_processor.DEPENDENCIES_AVAILABLE', True)
    @patch('english_accent_classifier.audio_processor.yt_dlp')
    @patch('english_accent_classifier.audio_processor.AudioSegment')
    def test_download_and_convert_success(self, mock_audio_segment, mock_yt_dlp):
        """Test successful audio download and conversion."""
        # Mock the YouTube downloader
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

        # Mock AudioSegment
        mock_audio = MagicMock()
        mock_audio_segment.from_file.return_value = mock_audio

        processor = AudioProcessor(temp_dir=self.temp_dir)

        # Create the expected audio file that the mock should "download"
        temp_audio_file = os.path.join(self.temp_dir, f"temp_audio_{os.getpid()}.{processor.audio_format}")
        with open(temp_audio_file, 'w') as f:
            f.write('mock audio data')

        try:
            result = processor.download_and_convert_to_wav("https://youtube.com/watch?v=test")

            # Check that the result is a WAV file path
            self.assertTrue(result.endswith('.wav'))
            self.assertTrue(os.path.basename(result).startswith('temp_audio_'))

            # Verify mocks were called
            mock_ydl_instance.download.assert_called_once_with(["https://youtube.com/watch?v=test"])
            mock_audio.export.assert_called_once()
        finally:
            # Clean up
            if os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)

    @patch('english_accent_classifier.audio_processor.DEPENDENCIES_AVAILABLE', True)
    @patch('english_accent_classifier.audio_processor.yt_dlp')
    def test_download_failure(self, mock_yt_dlp):
        """Test download failure handling."""
        # Mock the YouTube downloader
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

        processor = AudioProcessor(temp_dir=self.temp_dir)

        with self.assertRaises(AudioProcessingError):
            processor.download_and_convert_to_wav("https://youtube.com/watch?v=test")


if __name__ == '__main__':
    unittest.main()
