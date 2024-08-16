"""new command"""

from uncross.project.create import create_project
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def new_command(name: str, source_dir: str, build_project: bool, git: bool) -> None:
    """new project"""
    LOGGER.info("Creating new project %s at %s ...", name, source_dir)
    create_project(name, source_dir, build_project, git)
