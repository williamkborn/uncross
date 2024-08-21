"""autocompletion command group"""

import click

from uncross.cli.uncross.autocompletion.bash import bash
from uncross.cli.uncross.autocompletion.fish import fish
from uncross.cli.uncross.autocompletion.zsh import zsh


@click.group("autocompletion")
def autocompletion() -> None:
    """Autocompletion commands."""


autocompletion.add_command(bash)
autocompletion.add_command(fish)
autocompletion.add_command(zsh)
