"""lint command"""

from __future__ import annotations

import os
import sys

import click
import git

from uncross.git.repo import get_project_root
from uncross.logger import make_logger
from uncross.programs.clang_format import invoke_clang_format

LOGGER = make_logger(__name__)


def run_over_c_h_files_find(source_dir: str | None, args: list[str]) -> bool:
    """Run over all files using a find-like behavior."""
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


def run_over_c_h_files_git(source_dir: str | None, args: list[str]) -> bool:
    """Run over all files by walking git tree."""
    lint_found = False

    repo = git.Repo(source_dir)

    staged_files = repo.index.diff("HEAD")
    staged_files = [item.a_path for item in staged_files if item.a_path.endswith((".c", ".h"))]

    committed_files = [
        item.abspath
        for item in repo.head.commit.tree.traverse()
        if item.abspath.endswith((".c", ".h"))
    ]

    for file in staged_files + committed_files:
        LOGGER.debug("running clang-format on %s", file)
        file_args = [file]
        if invoke_clang_format(args + file_args) != 0:
            lint_found = True

    return lint_found


def run_over_c_h_files(source_dir: str | None, args: list[str]) -> bool:
    """run for each c/h file"""
    try:
        return run_over_c_h_files_git(source_dir, args)
    except git.exc.InvalidGitRepositoryError:
        return run_over_c_h_files_find(".", args)


def lint_command(source_dir: str | None) -> None:
    """lint code"""
    LOGGER.info("linting .c and .h files ...")
    args = [
        "clang-format",
        "--dry-run",
        "-Werror",
    ]
    if source_dir is None:
        args.append(f"--style=file:{get_project_root()}/.clang-format")
        lint_found = run_over_c_h_files(get_project_root(), args)
    else:
        args.append(f"--style=file:{source_dir}/.clang-format")
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
    LOGGER.debug("lint command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    lint_command(source_dir)
