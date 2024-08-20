"""Run commands from cli perspective."""

from __future__ import annotations

import sys
from multiprocessing import Process

from uncross.cli import uncross
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def invoke_uncross(args: list[str]) -> None:
    """invoke uncross"""
    sys.argv = args
    uncross()  # pylint: disable=no-value-for-parameter


def run_uncross_process(args: list[str]) -> int:
    """run uncross test"""
    LOGGER.info("invoking: %s", args)
    process = Process(target=invoke_uncross, args=[args])
    process.start()
    process.join()
    return process.exitcode
