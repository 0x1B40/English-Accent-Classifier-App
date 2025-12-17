"""Audio processing utilities for downloading and converting audio files."""

import logging
import os
import tempfile
import warnings
from typing import Optional

try:
    from pydub import AudioSegment
    import yt_dlp
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    MISSING_DEPENDENCY_ERROR = str(e)

from .exceptions import DependencyError, DownloadError, AudioProcessingError
from .config import get_config

logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)


class AudioProcessor:
    """Handles audio downloading and processing operations."""

    def __init__(self, temp_dir: Optional[str] = None):
        """Initialize the audio processor.

        Args:
            temp_dir: Directory for temporary files. Uses system temp if None.
        """
        if not DEPENDENCIES_AVAILABLE:
            raise DependencyError(
                "Required dependencies are not available. Please install "
                "torch, pydub, speechbrain, and yt-dlp."
            )

        config = get_config()
        self.temp_dir = temp_dir or config.get('audio.temp_dir') or tempfile.gettempdir()
        self.youtube_format = config.get('youtube.format')
        self.audio_format = config.get('youtube.audio_format')
        self.audio_quality = config.get('youtube.audio_quality')

    def download_and_convert_to_wav(self, youtube_url: str) -> str:
        """Download audio from YouTube URL and convert it to WAV format.

        Args:
            youtube_url: The YouTube video URL to download audio from.

        Returns:
            str: Path to the converted WAV file.

        Raises:
            DependencyError: If required dependencies are not available.
            DownloadError: If download fails.
            AudioProcessingError: If audio conversion fails.
        """
        if not DEPENDENCIES_AVAILABLE:
            raise DependencyError(
                "Required dependencies are not available. Please install "
                "torch, pydub, speechbrain, and yt-dlp."
            )

        # Create temporary filenames
        temp_base = os.path.join(self.temp_dir, f"temp_audio_{os.getpid()}")
        temp_audio_file = f"{temp_base}.{self.audio_format}"
        temp_wav = f"{temp_base}.wav"

        try:
            # Configure yt-dlp options with fallbacks
            ydl_opts = {
                'format': self.youtube_format,
                'outtmpl': f"{temp_base}.%(ext)s",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.audio_format,
                    'preferredquality': self.audio_quality,
                }],
                'quiet': True,
                'no_warnings': True,
                # Add options to handle various YouTube issues
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'player_skip': ['js', 'configs'],
                    }
                },
            }

            logger.info(f"Starting download from URL: {youtube_url}")
            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            logger.info("Download completed")

            # Check if audio file was created and has content
            if not os.path.exists(temp_audio_file):
                raise DownloadError(f"Failed to download audio from YouTube URL.")

            # Check if the file has any content
            if os.path.getsize(temp_audio_file) == 0:
                raise DownloadError(
                    "Downloaded audio file is empty. The video may not be available, "
                    "may not contain audio, or may be restricted. Try a different YouTube URL."
                )

            logger.info(f"Downloaded audio file size: {os.path.getsize(temp_audio_file)} bytes")

            # Convert to WAV
            audio = AudioSegment.from_file(temp_audio_file)
            audio.export(temp_wav, format="wav")

            logger.info(f"Audio processing complete, returning WAV path: {temp_wav}")
            return temp_wav

        except Exception as e:
            raise AudioProcessingError(f"Audio processing failed: {str(e)}")
        finally:
            # Clean up temporary audio file
            if os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)

    def cleanup_temp_file(self, file_path: str) -> None:
        """Clean up temporary audio file.

        Args:
            file_path: Path to the temporary file to remove.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            pass  # Ignore cleanup errors
