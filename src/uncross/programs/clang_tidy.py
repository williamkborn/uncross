"""Handle clang-tidy invocation"""

from __future__ import annotations

import functools
import os
import sys

from uncross.invoke import invoke_subprocess, perform_subtask
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def run_clang_tidy(args: list[str], stdout_replace: str = "") -> None:
    """Run clang tidy"""
    sys.argv = args

    if stdout_replace != "":
        with open(stdout_replace, "w", encoding="utf-8") as clang_tidy_output_path:
            os.dup2(clang_tidy_output_path.fileno(), 1)
            invoke_subprocess(args)
    else:
        invoke_subprocess(args)


def invoke_clang_tidy(args: list[str], stdout_replace: str = "") -> int:
    """invoke clang tidy"""
    to_run = functools.partial(run_clang_tidy, args, stdout_replace)
    return perform_subtask(to_run, [])
