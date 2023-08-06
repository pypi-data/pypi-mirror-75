"""
Handles config management

TODO: define a config schema
"""
import yaml


def load_config(file_path):
    with open(file_path, "rb") as config_file:
        return yaml.safe_load(config_file)
