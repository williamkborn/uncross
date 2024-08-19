"""Parse project config."""

from pathlib import Path

import toml

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def parse_tool_config() -> dict:
    """Parse project config"""
    config_path = Path.home() / ".config" / "uncross" / "uncross.toml"

    if not config_path.exists():
        return {}

    with config_path.open("r", encoding="utf-8") as config_file:
        config = toml.loads(config_file.read())
        LOGGER.debug("tool config: %s", config)
        return config
