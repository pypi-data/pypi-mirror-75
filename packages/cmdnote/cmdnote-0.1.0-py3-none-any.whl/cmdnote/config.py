import os
import configparser
from . import const, exception


class Config:
    """
    Manager of cmdnote config
    """

    def __init__(self, config_file=const.CONFIG_FILE):
        if not os.path.isfile(config_file):
            raise exception.ConfigFileNotFoundError('Config file not found', config_file)
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def get_configs(self):
        """Get configs from config file."""
        self.config.read(self.config_file)
        default = self.config[self.config.default_section]
        return dict(default)

    def get_config(self, key, default=None):
        """Get a config by key from config file."""
        configs = self.get_configs()
        return configs.get(key, default)

    def set_configs(self, configs):
        """Set configs in config file."""
        default = self.config[self.config.default_section]
        for key, value in configs.items():
            default[key] = str(value)
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def set_config(self, key, value):
        """Set a config by key in config file."""
        configs = self.get_configs()
        configs[key] = value
        self.set_configs(configs)
