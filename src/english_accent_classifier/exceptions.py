"""Custom exceptions for the English Accent Classifier."""


class AccentClassifierError(Exception):
    """Base exception for accent classifier errors."""
    pass


class DependencyError(AccentClassifierError):
    """Raised when required dependencies are not available."""
    pass


class AudioProcessingError(AccentClassifierError):
    """Raised when audio processing fails."""
    pass


class DownloadError(AccentClassifierError):
    """Raised when video/audio download fails."""
    pass


class ClassificationError(AccentClassifierError):
    """Raised when accent classification fails."""
    pass
