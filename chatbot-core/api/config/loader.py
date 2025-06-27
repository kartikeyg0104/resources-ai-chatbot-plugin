"""
YAML-based configuration loader.

Loads config.yml into a dictionary and exposes it as CONFIG.
"""

import os
import yaml
from utils import LoggerFactory

logger = LoggerFactory.instance().get_logger("api")

def load_config():
    """
    Loads and parses the config.yml file located in the same directory.

    Returns:
        dict: Parsed configuration values.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r", encoding='utf-8') as f:
        config = yaml.safe_load(f)

    config["is_test_mode"] = os.getenv("IS_TESTING", "0") == "1"
    if config["is_test_mode"]:
        logger.info("#### Running in Test Mode ####")

    return config

CONFIG = load_config()
