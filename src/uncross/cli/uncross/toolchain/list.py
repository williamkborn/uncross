"""List toolchains"""

from pathlib import Path

import click
import rich
import rich.style

from uncross.toolchains import enumerate_toolchains, find_toolchain_file


def toolchain_list_command(show_toolchain_file: bool = False) -> None:
    """List all toolchains"""
    console = rich.console.Console(highlighter=None)
    toolchains = enumerate_toolchains()

    for location in toolchains:
        console.print(f"{location}:", style="purple")

        for toolchain in Path(location).iterdir():
            if not toolchain.is_dir():
                continue
            console.print(f" - {toolchain.name}", markup=False, style="magenta")
            if show_toolchain_file:
                toolchain_file = find_toolchain_file(location, toolchain.name)
                path = str(toolchain_file).replace(
                    f"{location}/{toolchain.name}/{toolchain.name}", ""
                )
                console.print(f"   - {path}", markup=False, style="green")

        console.print("")


@click.command("list")
@click.option(
    "show_toolchain_file",
    "--show-toolchain-files",
    is_flag=True,
    required=False,
    help="initialize git repo",
)
def toolchain_list(show_toolchain_file: bool) -> None:
    """list toolchains"""
    toolchain_list_command(show_toolchain_file=show_toolchain_file)
