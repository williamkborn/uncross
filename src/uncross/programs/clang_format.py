"""Handle clang-format invocation"""

from __future__ import annotations

import functools
import os
import sys

from clang_format import clang_format

from uncross.invoke import perform_subtask
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def run_clang_format(args: list[str], stdout_replace: str = "") -> None:
    """Run clang format"""
    sys.argv = args

    if stdout_replace != "":
        with open(stdout_replace, "w", encoding="utf-8") as output_path:
            os.dup2(output_path.fileno(), 1)
            clang_format()
    else:
        clang_format()


def invoke_clang_format(args: list[str], stdout_replace: str = "") -> int:
    """invoke clang format"""
    to_run = functools.partial(run_clang_format, args, stdout_replace)
    return perform_subtask(to_run, [])
