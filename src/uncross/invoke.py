"""invoke a subprocess"""

from __future__ import annotations

import multiprocessing
import os
import shutil
import subprocess
import sys
from typing import Callable

from uncross.exceptions import ProgramMissingError
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def check_program(program: str) -> None:
    """Check if a program exists"""
    if shutil.which(program) is None:
        raise ProgramMissingError(program)


def subtask_redirect_stdout(args: list[str], task: Callable, stdout_replace: str = "") -> None:
    """Run clang format"""
    sys.argv = args

    if stdout_replace != "":
        with open(stdout_replace, "w", encoding="utf-8") as output_path:
            os.dup2(output_path.fileno(), 1)
            return task()
    else:
        return task()


def invoke_subprocess(args: list[str]) -> int:
    """invoke a subprocess"""
    check_program(args[0])
    args[0] = shutil.which(args[0])
    LOGGER.debug("running command: %s", args)
    process = subprocess.run(args, shell=False, check=False)
    return process.returncode


def perform_subtask(task: Callable, args: list[str]) -> int:
    """Run a subtask"""
    process = multiprocessing.Process(target=task, args=args)
    process.start()
    process.join()
    return process.exitcode
