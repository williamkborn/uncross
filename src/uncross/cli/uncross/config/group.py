"""uncross config command group"""

import click

from uncross.cli.uncross.config.list import config_list


@click.group("config")
def config() -> None:
    """uncross config commands"""


config.add_command(config_list)