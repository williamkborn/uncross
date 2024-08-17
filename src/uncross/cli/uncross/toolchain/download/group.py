"""toolchain download command group"""

import click

from uncross.cli.uncross.toolchain.download.bootlin import bootlin


@click.group("download")
def toolchain_download() -> None:
    """download toolchains"""


toolchain_download.add_command(bootlin)
