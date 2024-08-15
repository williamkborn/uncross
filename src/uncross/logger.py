"""Uncross logging."""

import logging
import sys

LOG_LEVEL = "DEBUG"

def make_logger(name: str) -> logging.Logger:
    """Get Logger and add handler and formatting.

    Args:
        name (str): Module name.

    Returns:
        logging.Logger: Logger object.
    """
    logger = logging.getLogger(name)

    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    formatter = logging.Formatter(
        "[%(levelname)s] %(filename)s.%(funcName)s:%(lineno)d %(message)s"
    )
    handler.setFormatter(formatter)

    return logger
