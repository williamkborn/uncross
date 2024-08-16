"""download command"""

import tarfile
from pathlib import Path

from uncross.logger import make_logger
from uncross.network.download import download_file

LOGGER = make_logger(__name__)


def download_bootlin(arch: str, libc: str, status: str, version: str) -> None:
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
            tar.extractall(path=output_path, filter="data")
    except FileNotFoundError:
        LOGGER.error("toolchain %s not found.", tarball)


def download_command(arch: str, libc: str, status: str, version: str) -> None:
    """Clean project"""
    download_bootlin(arch, libc, status, version)
