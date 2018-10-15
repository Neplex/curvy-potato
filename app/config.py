"""
Configuration loader
"""

import os
import uuid


class Config(object):
    """Configuration flask extension."""

    __env_prefix = 'API_'
    __default_config = {
        'DEBUG': False,
        'SECRET_KEY': str(uuid.uuid4()),
        'DATABASE_URI': 'sqlite:///:memory:'
    }

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        """App init."""
        self.app = app
        self.load_config()

    def load_config_from_file(self, local_settings):
        """Load cofiguration from 'local_settings' file."""
        for cfg, default in self.__default_config.items():
            self.app.config[cfg] = local_settings.get(cfg, default)

    def load_config_from_env(self):
        """Load Configuration from environment variables."""
        for cfg, default in self.__default_config.items():
            self.app.config[cfg] = os.getenv(self.__env_prefix + cfg, default)

    def load_config(self):
        """Load configuration."""
        print("Start loading config...")
        try:
            import local_settings
            print("Use local settings.")
            self.load_config_from_file(local_settings.__dict__)
        except ImportError:
            print("No local settings found, use environment variables instead.")
            self.load_config_from_env()
