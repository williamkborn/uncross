"""autocompletion for fish"""

import click
from auto_click_auto import enable_click_shell_completion
from auto_click_auto.constants import ShellType


@click.command("fish")
def fish() -> None:
    """Add fish autocompletion."""
    enable_click_shell_completion(program_name="uncross", shells=[ShellType.FISH], verbose=True)
