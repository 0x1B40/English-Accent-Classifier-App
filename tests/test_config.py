"""Tests for configuration management."""

import tempfile
import unittest
from pathlib import Path

from english_accent_classifier.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    def test_default_config(self):
        """Test loading default configuration."""
        config = Config()

        # Test app config
        self.assertEqual(config.get("app.name"), "English Accent Classifier")
        self.assertEqual(config.get("app.version"), "1.0.0")

        # Test audio config
        self.assertIsNone(config.get("audio.temp_dir"))
        self.assertEqual(config.get("audio.sample_rate"), 16000)

        # Test model config
        self.assertEqual(
            config.get("model.path"), "Jzuluaga/accent-id-commonaccent_ecapa"
        )

    def test_config_get_set(self):
        """Test getting and setting configuration values."""
        config = Config()

        # Test setting a value
        config.set("test.key", "test_value")
        self.assertEqual(config.get("test.key"), "test_value")

        # Test getting with default
        self.assertEqual(config.get("nonexistent.key", "default"), "default")

    def test_config_file_loading(self):
        """Test loading configuration from file."""
        # Create a temporary config file
        config_data = """
app:
  name: "Test App"
  version: "2.0.0"
audio:
  temp_dir: "/tmp/test"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(config_data)
            temp_file = f.name

        try:
            config = Config(temp_file)

            # Test loaded values
            self.assertEqual(config.get("app.name"), "Test App")
            self.assertEqual(config.get("app.version"), "2.0.0")
            self.assertEqual(config.get("audio.temp_dir"), "/tmp/test")

            # Test default values still work
            self.assertEqual(config.get("audio.sample_rate"), 16000)

        finally:
            Path(temp_file).unlink()

    def test_config_merge(self):
        """Test configuration merging."""
        config = Config()

        # Original value
        self.assertEqual(config.get("audio.sample_rate"), 16000)

        # Set a custom value
        config.set("audio.sample_rate", 44100)
        self.assertEqual(config.get("audio.sample_rate"), 44100)


if __name__ == "__main__":
    unittest.main()
