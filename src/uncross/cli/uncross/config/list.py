"""config list command"""

import click

from uncross.config.tool.parse import parse_tool_config
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


@click.command("list")
def config_list() -> None:
    """New project."""
    config = parse_tool_config()

    LOGGER.info("config: %s", config)
