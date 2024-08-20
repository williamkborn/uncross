"""Handle clang-format invocation"""

from __future__ import annotations

import functools

from uncross.invoke import (
    check_program,
    invoke_subprocess,
    perform_subtask,
    subtask_redirect_stdout,
)
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def invoke_clang_format(args: list[str], stdout_replace: str = "") -> int:
    """invoke clang format"""
    try:
        from clang_format import clang_format  # pylint: disable=import-outside-toplevel

        to_run = functools.partial(subtask_redirect_stdout, args, clang_format, stdout_replace)
    except ImportError:
        check_program("clang-format")
        task = functools.partial(invoke_subprocess, args)
        to_run = functools.partial(subtask_redirect_stdout, args, task, stdout_replace)

    return perform_subtask(to_run, [])
