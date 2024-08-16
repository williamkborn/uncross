"""clean command"""

import shutil

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def clean_command(project_root: str, build_dir: str) -> None:
    """Clean project"""
    debug_dir = f"{project_root}/debug"
    release_dir = f"{project_root}/release"
    LOGGER.info("Cleaning project ...")
    LOGGER.debug("removing build dir: %s ...", build_dir)
    shutil.rmtree(build_dir, ignore_errors=True)
    LOGGER.debug("removing debug dir: %s ...", debug_dir)
    shutil.rmtree(debug_dir, ignore_errors=True)
    LOGGER.debug("removing release dir: %s ...", release_dir)
    shutil.rmtree(release_dir, ignore_errors=True)
