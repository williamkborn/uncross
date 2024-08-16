"""Uncross logging."""

import logging


def make_logger(name: str) -> logging.Logger:
    """Get Logger and add handler and formatting.

    Args:
        name (str): Module name.

    Returns:
        logging.Logger: Logger object.
    """
    return logging.getLogger(name)
