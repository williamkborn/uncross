"""invoke a subprocess"""

from __future__ import annotations

import multiprocessing
import subprocess
from typing import Callable

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def invoke_subprocess(args: list[str]) -> int:
    """invoke a subprocess"""
    command = " ".join(args)
    process = subprocess.run(["/bin/sh", "-c", command], shell=False, check=False)
    return process.returncode


def perform_subtask(task: Callable, args: list[str]) -> int:
    """Run a subtask"""
    process = multiprocessing.Process(target=task, args=args)
    process.start()
    process.join()
    return process.exitcode
