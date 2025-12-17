"""Accent classification using SpeechBrain models."""

import logging
import os
import warnings
from typing import Tuple, Optional

try:
    import torch
    import torch.nn.functional as F
    from speechbrain.inference import EncoderClassifier
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    MISSING_DEPENDENCY_ERROR = str(e)

from .exceptions import DependencyError, ClassificationError
from .config import get_config

logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)


class AccentClassifier:
    """Handles accent classification using SpeechBrain models."""

    def __init__(self, model_path: Optional[str] = None):
        """Initialize the accent classifier.

        Args:
            model_path: Path to the model. Uses config default if None.
        """
        if not DEPENDENCIES_AVAILABLE:
            raise DependencyError(
                "Required dependencies are not available. Please install "
                "torch, pydub, speechbrain, and yt-dlp."
            )

        config = get_config()
        self.model_path = model_path or config.get('model.path')
        self.cache_dir = config.get('model.cache_dir')

        self.model: Optional[EncoderClassifier] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the SpeechBrain model."""
        try:
            # Set cache directory if specified
            if self.cache_dir:
                os.environ['TORCH_HOME'] = self.cache_dir

            self.model = EncoderClassifier.from_hparams(self.model_path)
        except Exception as e:
            raise ClassificationError(f"Failed to load accent classification model: {str(e)}")

    def classify_accent(self, wav_path: str) -> Tuple[str, str]:
        """Classify the English accent in the given WAV audio file.

        Args:
            wav_path: Path to the WAV audio file to classify.

        Returns:
            tuple: (result_string, best_label) where result_string contains
                   all accent probabilities and best_label is the most probable accent.

        Raises:
            DependencyError: If required dependencies are not available.
            ClassificationError: If classification fails.
        """
        if not DEPENDENCIES_AVAILABLE or self.model is None:
            raise DependencyError(
                "Required dependencies are not available. Please install "
                "torch, pydub, speechbrain, and yt-dlp."
            )

        # Ensure the file exists
        if not os.path.exists(wav_path):
            raise ClassificationError(f"Audio file not found: {wav_path}")

        # Normalize the path to absolute path to avoid Windows path issues
        wav_path = os.path.abspath(wav_path)
        # Convert backslashes to forward slashes to avoid escape character issues
        wav_path = wav_path.replace('\\', '/')
        logger.info(f"Classifying audio file: {wav_path}")

        try:
            # Perform classification
            logits, _, _, _ = self.model.classify_file(wav_path)
            probs = F.softmax(logits, dim=1)
            class_labels = self.model.hparams.label_encoder.decode_ndim(
                torch.arange(probs.shape[1])
            )

            # Build result string
            result = "Accent probabilities:\n\n"
            for i, lbl in enumerate(class_labels):
                probability = probs[0, i].item() * 100
                result += f"{str(lbl):<20}: {probability:>6.2f}%\n"

            # Find the most probable accent
            best_index = torch.argmax(probs, dim=1).item()
            best_label = class_labels[best_index]

            return result, best_label

        except Exception as e:
            raise ClassificationError(f"Accent classification failed: {str(e)}")

    def get_supported_accents(self) -> list[str]:
        """Get the list of supported accent types.

        Returns:
            list: List of supported accent names.

        Raises:
            ClassificationError: If model is not loaded.
        """
        if self.model is None:
            raise ClassificationError("Model not loaded. Cannot retrieve accent list.")

        try:
            return self.model.hparams.label_encoder.decode_ndim(
                torch.arange(self.model.hparams.label_encoder.num_labels)
            ).tolist()
        except Exception as e:
            raise ClassificationError(f"Failed to retrieve accent list: {str(e)}")
