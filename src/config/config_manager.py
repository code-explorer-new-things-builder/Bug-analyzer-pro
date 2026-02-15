"""Configuration manager for loading and managing analysis settings."""

import json
import os
from pathlib import Path
from typing import Optional
from src.models.config import AnalysisConfig


class ConfigManager:
    """Manages configuration loading and validation."""
    
    DEFAULT_CONFIG_PATHS = [
        '.reviewrc',
        '.reviewrc.json',
        'review.config.json',
        os.path.expanduser('~/.reviewrc')
    ]
    
    def __init__(self):
        """Initialize config manager."""
        self._config: Optional[AnalysisConfig] = None
    
    def load_config(self, config_path: Optional[str] = None) -> AnalysisConfig:
        """Load configuration from file or use defaults.
        
        Args:
            config_path: Optional path to config file
            
        Returns:
            AnalysisConfig instance
        """
        if config_path and os.path.exists(config_path):
            return self._load_from_file(config_path)
        
        # Try default paths
        for path in self.DEFAULT_CONFIG_PATHS:
            if os.path.exists(path):
                return self._load_from_file(path)
        
        # Return default config
        return AnalysisConfig()
    
    def _load_from_file(self, file_path: str) -> AnalysisConfig:
        """Load config from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return AnalysisConfig.from_dict(data)
        except Exception as e:
            raise ValueError(f"Failed to load config from {file_path}: {e}")
    
    def save_config(self, config: AnalysisConfig, file_path: str) -> None:
        """Save configuration to file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(config.to_dict(), f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to save config to {file_path}: {e}")
    
    def create_default_config(self, file_path: str = '.reviewrc.json') -> None:
        """Create a default configuration file."""
        config = AnalysisConfig()
        self.save_config(config, file_path)
