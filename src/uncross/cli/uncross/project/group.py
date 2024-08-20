"""project command group"""

import click

from uncross.cli.uncross.project.config.group import config


@click.group("project")
def project() -> None:
    """Project commands."""


project.add_command(config)
