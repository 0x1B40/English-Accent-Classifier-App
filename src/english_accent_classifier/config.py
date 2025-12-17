"""Configuration management for the English Accent Classifier."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class Config:
    """Configuration manager for the application."""

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file. If None, uses default.
        """
        self.config_file = config_file or self._get_default_config_path()
        self._config: Dict[str, Any] = {}

        self._load_config()

    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        # Try to find config relative to the package
        package_dir = Path(__file__).parent.parent.parent
        config_path = package_dir / "config" / "default.yaml"
        return str(config_path)

    def _load_config(self) -> None:
        """Load configuration from file."""
        if not YAML_AVAILABLE:
            # Use default configuration if yaml is not available
            self._config = self._get_default_config()
            return

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = yaml.safe_load(f) or {}
                # Merge with defaults
                defaults = self._get_default_config()
                self._config = self._merge_configs(defaults, loaded_config)
            else:
                self._config = self._get_default_config()
        except Exception:
            # Fall back to defaults on any error
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "app": {
                "name": "English Accent Classifier",
                "version": "1.0.0",
                "description": "A tool for identifying English accents from YouTube videos"
            },
            "audio": {
                "temp_dir": None,
                "sample_rate": 16000,
                "channels": 1
            },
            "model": {
                "path": "Jzuluaga/accent-id-commonaccent_ecapa",
                "cache_dir": None
            },
            "youtube": {
                "format": "bestaudio/best",
                "audio_format": "mp3",
                "audio_quality": "192"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": None
            },
            "gui": {
                "title": "English Accent Classifier",
                "width": 600,
                "height": 500,
                "font_family": "Arial",
                "font_size": 10
            }
        }

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two configuration dictionaries."""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.

        Args:
            key: Dot-separated configuration key (e.g., 'audio.temp_dir')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Dot-separated configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the final value
        config[keys[-1]] = value

    def save(self, file_path: Optional[str] = None) -> None:
        """Save current configuration to file.

        Args:
            file_path: Path to save to. If None, uses current config file.
        """
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML is required to save configuration files")

        save_path = file_path or self.config_file

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self._config, f, default_flow_style=False, indent=2)


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
