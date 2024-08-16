"""CLI Entrypoint"""

from __future__ import annotations

import logging
import sys

import click

from uncross.__about__ import __version__
from uncross.build_params import BuildParams
from uncross.commands.build import build_command
from uncross.commands.check import check_command
from uncross.commands.clean import clean_command
from uncross.commands.download import download_command
from uncross.commands.fmt import fmt_command
from uncross.commands.lint import lint_command
from uncross.commands.new import new_command
from uncross.commands.release import release_command
from uncross.git.repo import get_project_root
from uncross.logger import make_logger
from uncross.task.series_pipeline import SeriesPipeline

LOGGER = make_logger(__name__)

ASCII_ART = (
    "__   _ _ __   ___ _ __ ___  ___ ___                                         \n"
    "| | | | '_ \\ / __| '__/ _ \\/ __/ __|                                        \n"
    "| |_| | | | | (__| | | (_) \\__ \\__ \\                                        \n"
    "\\___,_|_| |_|\\___|_|  \\___/|___/___/                                        \n"
)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False
)
@click.version_option(version=__version__, prog_name="uncross")
@click.option("log_level", "--level", default="INFO", help="Logging level.")
def uncross(log_level: str):
    """Entrypoint."""
    try:
        log_format = "[%(levelname)s] %(message)s"
        if log_level == "DEBUG":
            log_format = "[%(levelname)s] %(filename)s.%(funcName)s:%(lineno)d %(message)s"
        logging.basicConfig(level=log_level.upper(), format=log_format)
    except ValueError:
        click.echo(f"ERROR: '{log_level}' is not a valid logging level.")
        sys.exit(1)


uncross.help = f"{ASCII_ART}\nAn opinionated meta build system for C cross-compilation."


@uncross.command("build")
@click.option("-S", "--source-dir", type=str, help="source directory")
@click.option("-B", "--build-dir", type=str, help="build directory")
@click.option("-D", "--define-cmake-var", type=str, multiple=True, help="define cmake variables")
@click.option("-t", "--toolchain", type=str, multiple=True, help="toolchain to invoke")
@click.option("-p", "--preset", type=str, multiple=True, help="cmake presets to build")
@click.option("--debug", is_flag=True, required=False, help="to build in debug")
@click.option("--release", is_flag=True, required=False, help="to build in release")
@click.option(
    "build_all",
    "--all",
    "-a",
    is_flag=True,
    required=False,
    help="to build both release and debug",
)
def build(
    source_dir: str,
    build_dir: str,
    define_cmake_var: list[str],
    toolchain: list[str],
    preset: list[str],
    debug: bool,
    release: bool,
    build_all: bool,
) -> None:
    """Build project."""
    LOGGER.debug("build command invoked with args:")

    if source_dir is None:
        source_dir = get_project_root()

    if build_dir is None:
        build_dir = f"{source_dir}/build"

    LOGGER.debug("source dir: %s", source_dir)
    LOGGER.debug("build dir: %s", build_dir)
    LOGGER.debug("define cmake variables: %s", define_cmake_var)
    LOGGER.debug("presets: %s", preset)

    if len(toolchain) == 0 and len(preset) == 0:
        LOGGER.warning("no toolchains or presets provided, building native ...")
        toolchain = list(toolchain)
        toolchain.append("native")

    LOGGER.debug("toolchains: %s", toolchain)
    LOGGER.debug("debug: %s", debug)
    LOGGER.debug("release: %s", release)

    params = BuildParams(
        build_dir=build_dir,
        source_dir=source_dir,
        build_debug=False,
        toolchains=toolchain,
        presets=preset,
        cmake_vars=define_cmake_var,
    )

    if build_all or debug or (not debug and not release):
        LOGGER.debug("building Debug ...")
        params.build_debug = True
        build_command(SeriesPipeline("build pipeline"), params)

    if build_all or release:
        LOGGER.debug("building Release ...")
        params.build_debug = False
        build_command(SeriesPipeline("build pipeline"), params)


@uncross.command("check")
@click.option("-S", "--source-dir", type=str, help="source directory")
@click.option("-B", "--build-dir", type=str, help="build directory")
@click.option("-t", "--toolchain", type=str, multiple=True, help="toolchain to invoke")
@click.option("-p", "--preset", type=str, multiple=True, help="cmake presets to build")
@click.option("--debug", is_flag=True, required=False, help="to build in debug")
@click.option("--release", is_flag=True, required=False, help="to build in release")
@click.option(
    "check_all",
    "--all",
    "-a",
    is_flag=True,
    required=False,
    help="to check both release and debug",
)
@click.option(
    "open_browser", "--open", is_flag=True, required=False, help="open reports in browser"
)
def check(
    source_dir: str,
    build_dir: str,
    toolchain: list[str],
    preset: list[str],
    debug: bool,
    release: bool,
    check_all: bool,
    open_browser: bool,
) -> None:
    """Check project."""

    if source_dir is None:
        source_dir = get_project_root()

    if build_dir is None:
        build_dir = f"{source_dir}/build"

    LOGGER.debug("check command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    LOGGER.debug("build dir: %s", build_dir)
    LOGGER.debug("presets: %s", preset)

    if len(toolchain) == 0 and len(preset) == 0:
        LOGGER.warning("no toolchains or presets provided, building native ...")
        toolchain = list(toolchain)
        toolchain.append("native")

    LOGGER.debug("toolchains: %s", toolchain)
    LOGGER.debug("debug: %s", debug)
    LOGGER.debug("release: %s", release)

    params = BuildParams(
        build_dir=build_dir,
        source_dir=source_dir,
        build_debug=False,
        toolchains=toolchain,
        presets=preset,
        cmake_vars=[],
    )

    if check_all or debug or (not debug and not release):
        LOGGER.debug("checking Debug ...")
        params.build_debug = True
        check_command(SeriesPipeline("build pipeline"), params, open_browser=open_browser)

    if check_all or release:
        LOGGER.debug("checking Release ...")
        params.build_debug = False
        check_command(SeriesPipeline("build pipeline"), params, open_browser=open_browser)


@uncross.command("clean")
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


@uncross.command("download")
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
def download(arch: str, libc: str, status: str, version: str):
    """Download a toolchain."""
    download_command(arch, libc, status, version)


@uncross.command("fmt")
@click.option("-S", "--source-dir", type=str, help="source directory")
def fmt(source_dir: str) -> None:
    """Format project."""
    if source_dir is None:
        source_dir = get_project_root()
    LOGGER.debug("fmt command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    fmt_command(source_dir)


@uncross.command("lint")
@click.option("-S", "--source-dir", type=str, help="source directory")
def lint(source_dir: str) -> None:
    """Lint code."""
    if source_dir is None:
        source_dir = get_project_root()
    LOGGER.debug("lint command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    lint_command(source_dir)


@uncross.command("new")
@click.argument("source_dir", type=str)
@click.option("-n", "--name", type=str, default="", help="project name")
@click.option("--build", is_flag=True, required=False, help="build project on creation")
@click.option("--no-git", is_flag=True, required=False, help="initialize git repo")
def new(source_dir: str, name: str, build: bool, no_git: bool) -> None:
    """New project."""
    if name == "":
        name = source_dir
    LOGGER.debug("new command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    LOGGER.debug("name: %s", source_dir)
    new_command(name, source_dir, build, not no_git)


@uncross.command("release")
@click.option("-S", "--source-dir", type=str, help="source directory")
def release(source_dir: str) -> None:
    """Release code."""
    if source_dir is None:
        source_dir = get_project_root()

    LOGGER.debug("release command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    release_command(source_dir)
