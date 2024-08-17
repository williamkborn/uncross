"""release command"""

import click

from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def release_command(source_dir: str) -> None:
    """release code"""
    LOGGER.info("release project at %s", source_dir)


@click.command("release")
@click.option("-S", "--source-dir", type=str, help="source directory")
def release(source_dir: str) -> None:
    """Release code."""
    if source_dir is None:
        source_dir = get_project_root()

    LOGGER.debug("release command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    release_command(source_dir)
