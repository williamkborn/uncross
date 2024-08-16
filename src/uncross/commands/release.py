"""release command"""

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def release_command(source_dir: str) -> None:
    """release code"""
    LOGGER.info("release project at %s", source_dir)
