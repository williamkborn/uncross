"""Build command."""

from __future__ import annotations

import functools
import os
from multiprocessing import cpu_count
from typing import TYPE_CHECKING

from uncross.invoke import invoke_subprocess
from uncross.logger import make_logger
from uncross.task.task import BuildTask

if TYPE_CHECKING:
    from uncross.build_params import BuildParams
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

    if invoke_subprocess(args) != 0:
        raise RuntimeError


def task_configure_toolchain(name: str, toolchain: str, params: BuildParams) -> None:
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

    if toolchain != "native":
        toolchainfile_path = f"/opt/cross/{toolchain}/toolchain.cmake"
        args.append(f"-DCMAKE_TOOLCHAIN_FILE={toolchainfile_path}")

    add_cmake_var_args(args, params.cmake_vars)

    if invoke_subprocess(args) != 0:
        raise RuntimeError


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

    if invoke_subprocess(args) != 0:
        raise RuntimeError


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
    configure_work = functools.partial(task_configure_toolchain, configure_name, name, params)
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
