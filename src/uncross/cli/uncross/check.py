"""Check command."""

from __future__ import annotations

import functools
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

import click

from uncross.build_params import BuildParams
from uncross.config.project.parse import parse_project_config
from uncross.exceptions import FailedSubTaskError
from uncross.git.repo import get_project_root
from uncross.logger import make_logger
from uncross.programs.code_checker import invoke_code_checker
from uncross.task.series_pipeline import SeriesPipeline
from uncross.task.task import BuildTask

if TYPE_CHECKING:
    from uncross.task.base_pipeline import BasePipeline

LOGGER = make_logger(__name__)


def task_check_toolchain(name: str, params: BuildParams) -> None:
    """Command:

    CodeChecker check
      -l <path to compile_commands.json>
      -o results
      --analyzer-config 'clang-tidy:take-config-from-directory=true'
    """
    build_mode = "Debug" if params.build_debug else "Release"
    analysis_path = f"{params.source_dir}/{build_mode.lower()}/analysis/code_checker/"
    build_dir = f"{params.build_dir}/{build_mode}/toolchains/{name}"

    compile_commands = f"{build_dir}/compile_commands.json"

    if not Path(compile_commands).exists():
        LOGGER.error("%s not found.", compile_commands)
        raise FailedSubTaskError

    LOGGER.info("running report on %s", compile_commands)
    args = [
        "CodeChecker",
        "check",
        "-l",
        compile_commands,
        "-o",
        f"{analysis_path}/results/{name}",
        "--analyzer-config",
        "'clang-tidy:take-config-from-directory=true'",
    ]

    result = invoke_code_checker(args)
    if result not in (0, 2):
        LOGGER.error("CodeChecker failed. (return code %s)", result)
        raise FailedSubTaskError


def task_report_toolchain(name: str, params: BuildParams, open_browser: bool) -> None:
    """Command:

    CodeChecker parse
      -e html
      ./results
      -o ./reports_html
    """
    build_mode = "Debug" if params.build_debug else "Release"
    analysis_path = f"{params.source_dir}/{build_mode.lower()}/analysis/code_checker/"

    results_dir = f"{analysis_path}/results/{name}"
    reports_dir = f"{analysis_path}/reports/{name}"

    args = [
        "CodeChecker",
        "parse",
        "-e",
        "html",
        results_dir,
        "-o",
        reports_dir,
    ]

    invoke_code_checker(args)

    if open_browser:
        report_path = f"{reports_dir}/index.html"
        LOGGER.info("opening %s in browser...", report_path)
        webbrowser.open_new_tab(report_path)


def check_toolchain(
    name: str, pipeline: BasePipeline, params: BuildParams, open_browser: bool
) -> None:
    """Add check tasks for a toolchain"""
    check_name = f"toolchain: {name} check task"
    check_work = functools.partial(task_check_toolchain, name, params)
    pipeline.add_task(BuildTask(check_name, check_work))
    report_name = f"toolchain: {name} reports task"
    report_work = functools.partial(task_report_toolchain, name, params, open_browser)
    pipeline.add_task(BuildTask(report_name, report_work))


def check_command(pipeline: BasePipeline, params: BuildParams, open_browser: bool = False) -> None:
    """Perform build."""
    LOGGER.info("checking ...")

    for toolchain in params.toolchains:
        check_toolchain(toolchain, pipeline, params, open_browser)

    for preset in params.presets:
        check_toolchain(preset, pipeline, params, open_browser)

    pipeline.run()

    LOGGER.info("check complete")


@click.command("check")
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
