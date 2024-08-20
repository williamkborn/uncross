"""register command"""

import click

from uncross.cli.uncross.toolchain.download.bootlin import download_bootlin_command
from uncross.config.project.commit import commit_project_config
from uncross.config.project.parse import parse_project_config
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def register_bootlin_command(
    arch: str, libc: str, status: str, version: str, search_path: str = "."
) -> None:
    """register bootlin toolchain"""
    toolchain_base = f"{arch}--{libc}--{status}-{version}"
    config = parse_project_config(search_path=search_path)

    if "uncross" not in config:
        config["uncross"] = {}

    if "toolchain" not in config["uncross"]:
        config["uncross"]["toolchain"] = {}

    toolchain = {
        "source": "bootlin",
        "arch": arch,
        "libc": libc,
        "status": status,
        "version": version,
    }

    config["uncross"]["toolchain"][toolchain_base] = toolchain

    download_bootlin_command(arch, libc, status, version)
    commit_project_config(config, search_path=search_path)

    LOGGER.info("registered toolchain %s", toolchain_base)


@click.command("bootlin")
@click.option("-S", "--source-dir", type=str, help="source directory")
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
def bootlin(source_dir: str, arch: str, libc: str, status: str, version: str):
    """register from toolchains.bootlin.com."""
    register_bootlin_command(arch, libc, status, version, source_dir if source_dir else ".")
