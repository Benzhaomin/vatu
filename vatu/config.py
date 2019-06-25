import logging
import os

import yaml


class Config:
    config = {}

    @classmethod
    def update(cls, config_dict):
        """ Update the current config only overwriting new values
        """
        cls.config = cls.deep_merge(cls.config, config_dict)

    @classmethod
    def deep_merge(cls, old, new):
        if not isinstance(old, dict):
            if not isinstance(new, dict):
                return new
            else:
                return old
        else:
            if isinstance(new, dict):
                for key in old:
                    if key in new:
                        old[key] = cls.deep_merge(old[key], new[key])
                return old
            else:
                return old

    @classmethod
    def load(cls, path):
        """ Loads config value from a yaml file at *path*
        """
        logging.debug("loading config from %s", path)

        with open(path, 'r') as yaml_file:
            yaml_config = yaml.load(yaml_file)

        # merge this config with the default one
        cls.update(yaml_config)

    @classmethod
    def defaults(cls, path=None):
        """ Loads default config values, optionnally from a given *path*
        """
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "config.default.yml")
        with open(path, 'r') as yaml_file:
            cls.config = yaml.load(yaml_file)

    @classmethod
    def get(cls, key):
        """ Return a config value from a n-level key
        """
        config = cls.config
        for level in key.split('.'):
            config = config.get(level, {})
        return config


Config.defaults()

specific_config = os.getenv('VATU_CONFIGFILE')
if specific_config:
    Config.load(specific_config)
