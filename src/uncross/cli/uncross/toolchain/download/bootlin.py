"""download command"""

import tarfile
from pathlib import Path

import click

from uncross.logger import make_logger
from uncross.network.download import download_file

LOGGER = make_logger(__name__)


def download_bootlin_command(arch: str, libc: str, status: str, version: str) -> None:
    """download bootlin toolchain"""
    toolchain_base = f"{arch}--{libc}--{status}-{version}"
    tarball = f"{toolchain_base}.tar.bz2"
    disk_path = f"{Path.home()!s}/.uncross/cache/{tarball}"
    output_path = f"{Path.home()!s}/.uncross/toolchains/{toolchain_base}"
    LOGGER.debug("downloading %s to %s ...", tarball, disk_path)
    url = f"https://toolchains.bootlin.com/downloads/releases/toolchains/{arch}/tarballs/{tarball}"

    try:
        download_file(url, disk_path)
        with tarfile.open(disk_path, mode="r:bz2") as tar:
            LOGGER.info("extracting ...")
            tar.extractall(path=output_path, filter=None)  # noqa: S202
    except FileNotFoundError:
        LOGGER.error("toolchain %s not found.", tarball)
    except ConnectionError:
        LOGGER.error("Could not connect to toolchains.bootlin.com.")


@click.command("bootlin")
@click.option("arch", "--arch", type=str, default="x86-64", help="Target architecture.")
@click.option("libc", "--libc", type=str, default="glibc", help="Target libc.")
@click.option(
    "status",
    "--status",
    type=str,
    default="stable",
    help="Target status ('stable', 'bleeding-edge').",
)
@click.option("version", "--version", type=str, default="2024.02-1", help="Target version.")
def bootlin(arch: str, libc: str, status: str, version: str):
    """Download from toolchains.bootlin.com."""
    download_bootlin_command(arch, libc, status, version)
