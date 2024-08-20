"""commit project config."""

from pathlib import Path

import toml

from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def commit_project_config(document: dict, search_path: str = ".") -> None:
    """commit project config"""
    config_path = Path(get_project_root(search_path=search_path)) / "uncross.toml"

    with config_path.open("w", encoding="utf-8") as config_file:
        config: str = toml.dumps(document)
        LOGGER.debug("project config: %s", config)
        config_file.write(config)
