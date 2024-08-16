"""new command"""

from uncross.logger import make_logger
from uncross.project.create import create_project

LOGGER = make_logger(__name__)


def new_command(name: str, source_dir: str, build_project: bool, git: bool) -> None:
    """new project"""
    LOGGER.debug("Creating new project %s at %s ...", name, source_dir)
    create_project(name, source_dir, build_project, git)
