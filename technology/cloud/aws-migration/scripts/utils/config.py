"""
Configuration management for AWS migration
"""
import yaml
import os
from typing import Dict, Any


class Config:
    """Configuration loader and manager"""

    def __init__(self, config_file: str):
        """
        Initialize config from YAML file

        Args:
            config_file: Path to YAML configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default=None):
        """
        Get configuration value

        Args:
            key: Configuration key (supports dot notation, e.g., 'migration.source.databases')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def get_aws_region(self) -> str:
        """Get AWS region from config"""
        return self.get('migration.target.region', 'us-east-1')

    def get_environment(self) -> str:
        """Get environment name"""
        return self.get('migration.target.environment', 'production')
