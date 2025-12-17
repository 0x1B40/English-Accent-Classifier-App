"""English Accent Classifier - A tool for identifying English accents from YouTube videos.

This package provides functionality to:
- Download audio from YouTube videos
- Convert audio to WAV format
- Classify English accents using SpeechBrain models
- Provide a GUI interface for easy use

Example:
    >>> from english_accent_classifier import AccentClassifier
    >>> classifier = AccentClassifier()
    >>> result = classifier.classify_from_url("https://www.youtube.com/watch?v=example")
"""

__version__ = "1.0.0"
__author__ = "English Accent Classifier Team"
__license__ = "MIT"

from .accent_classifier import AccentClassifier
from .audio_processor import AudioProcessor
from .gui import run_gui

__all__ = ["AccentClassifier", "AudioProcessor", "run_gui"]
