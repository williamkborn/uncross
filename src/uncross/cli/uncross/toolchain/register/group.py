"""toolchain register command group"""

import click

from uncross.cli.uncross.toolchain.register.bootlin import bootlin


@click.group("register")
def toolchain_register() -> None:
    """register toolchain with project"""


toolchain_register.add_command(bootlin)
