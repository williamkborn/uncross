"""lint command"""

from __future__ import annotations

import os
import sys

import click

from uncross.git.repo import get_project_root
from uncross.logger import make_logger
from uncross.programs.clang_format import invoke_clang_format

LOGGER = make_logger(__name__)


def run_over_c_h_files(source_dir: str, args: list[str]) -> bool:
    """run for each c/h file"""
    lint_found = False
    for dirpath, _, filenames in os.walk(source_dir):
        if "build" in dirpath or "__pycache__" in dirpath or "deps" in dirpath:
            continue
        for file in filenames:
            if file.endswith((".c", ".h")):
                LOGGER.debug("running clang-format on %s", file)

                file_args = [
                    os.path.join(dirpath, file),
                ]
                if invoke_clang_format(args + file_args) != 0:
                    lint_found = True

    return lint_found


def lint_command(source_dir: str) -> None:
    """lint code"""
    LOGGER.info("linting .c and .h files in %s", source_dir)
    args = [
        "clang-format",
        "--dry-run",
        "-Werror",
        f"--style=file:{get_project_root()}/.clang-format",
    ]
    lint_found = run_over_c_h_files(source_dir, args)

    if lint_found:
        LOGGER.error("LINT FOUND")
        sys.exit(1)
    else:
        LOGGER.info("NO LINT FOUND")


@click.command("lint")
@click.option("-S", "--source-dir", type=str, help="source directory")
def lint(source_dir: str) -> None:
    """Lint code."""
    if source_dir is None:
        source_dir = get_project_root()
    LOGGER.debug("lint command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    lint_command(source_dir)
