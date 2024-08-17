"""toolchain command group"""

import click

from uncross.cli.uncross.toolchain.download.group import toolchain_download
from uncross.cli.uncross.toolchain.list import toolchain_list


@click.group("toolchain")
def toolchain() -> None:
    """toolchain commands"""


toolchain.add_command(toolchain_list)
toolchain.add_command(toolchain_download)
