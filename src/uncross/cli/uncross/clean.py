"""clean command"""

import contextlib
import os
import shutil

import click

from uncross.git.repo import get_project_root
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
    LOGGER.debug("removing release tarball ...")
    with contextlib.suppress(FileNotFoundError):
        os.remove("release.tar.gz")


@click.command("clean")
@click.option("source_dir", "-S", "--source-dir", type=str, help="source directory")
@click.option("build_dir", "-B", "--build-dir", type=str, help="build directory")
def clean(source_dir: str, build_dir: str):
    """Clean build artifacts."""
    if source_dir is None:
        source_dir = get_project_root()

    if build_dir is None:
        build_dir = f"{source_dir}/build"

    LOGGER.debug("clean command invoked")
    clean_command(source_dir, build_dir)
