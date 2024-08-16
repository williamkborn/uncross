"""Handle clang-format invocation"""

from __future__ import annotations

import functools
import sys

from codechecker_common.cli import main as code_checker

from uncross.invoke import perform_subtask
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def run_code_checker(args: list[str]) -> None:
    """Run code checker"""
    sys.argv = args
    code_checker()


def invoke_code_checker(args: list[str]) -> int:
    """invoke clang format"""
    to_run = functools.partial(run_code_checker, args)
    return perform_subtask(to_run, [])
