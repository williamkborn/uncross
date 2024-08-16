"""Build command."""

import functools
import webbrowser

from uncross.build_params import BuildParams
from uncross.logger import make_logger
from uncross.programs.code_checker import invoke_code_checker
from uncross.task.base_pipeline import BasePipeline
from uncross.task.task import BuildTask

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
        raise RuntimeError


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
