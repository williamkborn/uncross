"""project config command group"""

import click

from uncross.cli.uncross.project.config.list import config_list


@click.group("config")
def config() -> None:
    """project config commands"""


config.add_command(config_list)
