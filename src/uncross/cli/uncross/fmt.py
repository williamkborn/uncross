"""fmt command"""

import click

from uncross.cli.uncross.lint import run_over_c_h_files
from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def fmt_command(source_dir: str) -> None:
    """fmt code"""
    LOGGER.info("formatting .c and .h files in %s", source_dir)
    args = ["clang-format", "-i", f"--style=file:{get_project_root()}/.clang-format"]
    format_failed = run_over_c_h_files(source_dir, args)

    if format_failed:
        raise RuntimeError


@click.command("fmt")
@click.option("-S", "--source-dir", type=str, help="source directory")
def fmt(source_dir: str) -> None:
    """Format project."""
    if source_dir is None:
        source_dir = get_project_root()
    LOGGER.debug("fmt command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    fmt_command(source_dir)
