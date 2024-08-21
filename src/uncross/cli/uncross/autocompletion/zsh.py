"""autocompletion for zsh"""

import click
from auto_click_auto import enable_click_shell_completion
from auto_click_auto.constants import ShellType


@click.command("zsh")
def zsh() -> None:
    """Add zsh autocompletion."""
    enable_click_shell_completion(program_name="uncross", shells=[ShellType.ZSH], verbose=True)
