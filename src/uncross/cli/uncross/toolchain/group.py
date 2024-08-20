"""toolchain command group"""

import click

from uncross.cli.uncross.toolchain.download.group import toolchain_download
from uncross.cli.uncross.toolchain.list import toolchain_list
from uncross.cli.uncross.toolchain.register.group import toolchain_register


@click.group("toolchain")
def toolchain() -> None:
    """Toolchain management commands."""


toolchain.add_command(toolchain_download)
toolchain.add_command(toolchain_list)
toolchain.add_command(toolchain_register)
