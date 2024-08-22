"""Build command."""

from __future__ import annotations

import functools
import os
from multiprocessing import cpu_count
from typing import TYPE_CHECKING

import click

from uncross.build_params import BuildParams
from uncross.config.project.parse import parse_project_config
from uncross.exceptions import FailedSubTaskError, ToolchainMissingError
from uncross.git.repo import get_project_root
from uncross.logger import make_logger
from uncross.programs.cmake import invoke_cmake
from uncross.task.series_pipeline import SeriesPipeline
from uncross.task.task import BuildTask
from uncross.toolchains import get_toolchain_file_by_name

if TYPE_CHECKING:
    from pathlib import Path

    from uncross.task.base_pipeline import BasePipeline


LOGGER = make_logger(__name__)


def add_cmake_var_args(args: list, cmake_vars: list[str]) -> None:
    """Add cmake vars to arg list"""
    for var in cmake_vars:
        if "=" not in var:
            args.append(f"-D{var}=On")
        else:
            args.append(f"-D{var}")
    args.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=On")


def task_configure_preset(name: str, preset: str, params: BuildParams) -> None:
    """Dummy task for testing"""
    LOGGER.debug("task: %s", name)

    build_mode = "Debug" if params.build_debug else "Release"
    build_dir = f"{params.build_dir}/{build_mode}/presets/{preset}"
    check_file = f"{build_dir}/CMakeCache.txt"
    if os.path.exists(check_file):
        LOGGER.debug("Found %s, skipping configure ...", check_file)
        return

    args = [
        "cmake",
        "--preset",
        preset,
        f"-B{params.build_dir}/{build_mode}/presets/{preset}",
        f"-S{params.source_dir}",
        f"-DCMAKE_BUILD_TYPE={build_mode}",
    ]

    add_cmake_var_args(args, params.cmake_vars)

    if invoke_cmake(args) != 0:
        raise FailedSubTaskError


def task_configure_toolchain(
    name: str, toolchain: str, params: BuildParams, toolchain_file: Path | None = None
) -> None:
    """Dummy task for testing"""
    LOGGER.debug("task: %s", name)

    build_mode = "Debug" if params.build_debug else "Release"
    build_dir = f"{params.build_dir}/{build_mode}/toolchains/{toolchain}"

    check_file = f"{build_dir}/CMakeCache.txt"
    if os.path.exists(check_file):
        LOGGER.debug("Found %s, skipping configure ...", check_file)
        return

    args = [
        "cmake",
        f"-B{build_dir}",
        f"-S{params.source_dir}",
        f"-DCMAKE_BUILD_TYPE={build_mode}",
    ]

    if toolchain_file is not None:
        args.append(f"-DCMAKE_TOOLCHAIN_FILE={toolchain_file!s}")

    add_cmake_var_args(args, params.cmake_vars)

    config = parse_project_config()

    if isinstance(
        config.get("uncross", {}).get("toolchain", {}).get(toolchain, {}).get("defines", None),
        dict,
    ):
        toolchain_vars = []
        for key, val in config["uncross"]["toolchain"][toolchain]["defines"].items():
            toolchain_vars.append(f"{key}={val}")
        add_cmake_var_args(args, toolchain_vars)

    if invoke_cmake(args) != 0:
        raise FailedSubTaskError


def task_build(name: str, build_subdir: str, build_name: str, params: BuildParams) -> None:
    """Build task"""
    LOGGER.debug("task: %s", name)

    build_mode = "Debug" if params.build_debug else "Release"
    args = [
        "cmake",
        "--build",
        f"{params.build_dir}/{build_mode}/{build_subdir}/{build_name}",
        "--parallel",
        f"{cpu_count() + 1}",
    ]

    if invoke_cmake(args) != 0:
        raise FailedSubTaskError


def build_preset(name: str, pipeline: BasePipeline, params: BuildParams) -> None:
    """Add build tasks for a preset"""
    configure_name = f"preset: {name} configure task"
    configure_work = functools.partial(task_configure_preset, configure_name, name, params)
    pipeline.add_task(BuildTask(configure_name, configure_work))
    build_name = f"preset: {name} build task"
    build_work = functools.partial(task_build, build_name, "presets", name, params)
    pipeline.add_task(BuildTask(build_name, build_work))


def build_toolchain(name: str, pipeline: BasePipeline, params: BuildParams) -> None:
    """Add build tasks for a toolchain"""
    configure_name = f"toolchain: {name} configure task"
    toolchain_file = None
    if name != "native":
        toolchain_file = get_toolchain_file_by_name(name)

        if toolchain_file is None:
            raise ToolchainMissingError(name)
    configure_work = functools.partial(
        task_configure_toolchain, configure_name, name, params, toolchain_file
    )
    pipeline.add_task(BuildTask(configure_name, configure_work))
    build_name = f"toolchain: {name} build task"
    build_work = functools.partial(task_build, build_name, "toolchains", name, params)
    pipeline.add_task(BuildTask(build_name, build_work))


def build_command(pipeline: BasePipeline, params: BuildParams) -> None:
    """Perform build."""
    LOGGER.info("building ...")

    for toolchain in params.toolchains:
        build_toolchain(toolchain, pipeline, params)

    for preset in params.presets:
        build_preset(preset, pipeline, params)

    pipeline.run()

    LOGGER.info("build complete")


@click.command("build")
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

    config = parse_project_config(search_path=source_dir)

    if len(toolchain) == 0 and "uncross" in config and "toolchain" in config["uncross"]:
        toolchain = list(set(list(toolchain) + list(config["uncross"]["toolchain"].keys())))

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
