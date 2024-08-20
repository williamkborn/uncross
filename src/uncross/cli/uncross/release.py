"""release command"""

import os
import sys
import tarfile

import click

from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def compress_directory_to_tar_gz(directory_path, output_file):
    """compress target directory"""
    LOGGER.info("tar %s to %s", directory_path, output_file)
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(directory_path, arcname=os.path.basename(directory_path))


def release_command(source_dir: str) -> None:
    """release code"""
    LOGGER.info("release project at %s", source_dir)
    if not os.path.exists(f"{source_dir}/release"):
        LOGGER.error("release dir does not exist, please run build --release")
        sys.exit(1)
    compress_directory_to_tar_gz(f"{source_dir}/release", f"{source_dir}/release.tar.gz")


@click.command("release")
@click.option("-S", "--source-dir", type=str, help="source directory")
def release(source_dir: str) -> None:
    """Release project."""
    if source_dir is None:
        source_dir = get_project_root()

    LOGGER.debug("release command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    release_command(source_dir)
