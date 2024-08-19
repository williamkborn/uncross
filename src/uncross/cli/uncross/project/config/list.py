"""config list command"""

import click

from uncross.config.project.parse import parse_project_config
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


@click.command("list")
def config_list() -> None:
    """New project."""
    config = parse_project_config()

    LOGGER.info("config: %s", config)
