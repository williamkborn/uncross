"""Parse project config."""

from pathlib import Path

import toml

from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def parse_project_config(search_path: str = ".") -> dict:
    """Parse project config"""
    config_path = Path(get_project_root(search_path=search_path)) / "uncross.toml"

    if not config_path.exists():
        return {}

    with config_path.open("r", encoding="utf-8") as config_file:
        config = toml.loads(config_file.read())
        LOGGER.debug("project config: %s", config)
        return config
