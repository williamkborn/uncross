"""autocompletion for bash"""

import click
from auto_click_auto import enable_click_shell_completion
from auto_click_auto.constants import ShellType


@click.command("bash")
def bash() -> None:
    """Add bash autocompletion."""
    enable_click_shell_completion(program_name="uncross", shells=[ShellType.BASH], verbose=True)
