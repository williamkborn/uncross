"""fmt command"""

from __future__ import annotations

import click

from uncross.cli.uncross.lint import run_over_c_h_files
from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def fmt_command(source_dir: str | None) -> None:
    """fmt code"""
    LOGGER.info("formatting .c and .h files in %s", source_dir)
    args = ["clang-format", "-i"]
    if source_dir is None:
        args.append(f"--style=file:{get_project_root()}/.clang-format")
        format_failed = run_over_c_h_files(get_project_root(), args)
    else:
        args.append(f"--style=file:{source_dir}/.clang-format")
        format_failed = run_over_c_h_files(source_dir, args)

    if format_failed:
        raise RuntimeError


@click.command("fmt")
@click.option("-S", "--source-dir", type=str, help="source directory")
def fmt(source_dir: str) -> None:
    """Format project."""
    LOGGER.debug("fmt command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    fmt_command(source_dir)
