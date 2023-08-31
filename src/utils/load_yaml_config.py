from pathlib import Path
from typing import Dict
from yaml import dump, safe_load


def load_yaml_config(path: Path) -> Dict:
    """
    Load YAML config file and return a parsed, ready to consume dictionary
    :param path: path to the config file
    :return: configuration dictionary
    """
    with open(file=path, mode='r') as stream:
        config = safe_load(stream)
        return config