"""CLI Entrypoint"""

import sys

from uncross.cli.uncross.group import uncross
from uncross.exceptions import FailedSubTaskError
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def main() -> None:
    """Entrypoint for program"""
    try:
        uncross()  # pylint: disable=no-value-for-parameter
    except FailedSubTaskError:
        LOGGER.error("task failed, exiting ...")
        sys.exit(1)
