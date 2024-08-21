"""Root cli group"""

import logging
import sys

import click

from uncross.__about__ import __version__
from uncross.cli.uncross.autocompletion.group import autocompletion
from uncross.cli.uncross.build import build
from uncross.cli.uncross.check import check
from uncross.cli.uncross.clean import clean
from uncross.cli.uncross.config.group import config
from uncross.cli.uncross.fmt import fmt
from uncross.cli.uncross.lint import lint
from uncross.cli.uncross.new import new
from uncross.cli.uncross.project.group import project
from uncross.cli.uncross.release import release
from uncross.cli.uncross.toolchain.group import toolchain
from uncross.logger import make_logger

LOGGER = make_logger(__name__)

ASCII_ART = (
    "__   _ _ __   ___ _ __ ___  ___ ___                                         \n"
    "| | | | '_ \\ / __| '__/ _ \\/ __/ __|                                        \n"
    "| |_| | | | | (__| | | (_) \\__ \\__ \\                                        \n"
    "\\___,_|_| |_|\\___|_|  \\___/|___/___/                                        \n"
)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False
)
@click.version_option(version=__version__, prog_name="uncross")
@click.option("log_level", "--level", default="INFO", help="Logging level.")
def uncross(log_level: str):
    """Entrypoint."""

    try:
        log_format = "[%(levelname)s] %(message)s"
        if log_level == "DEBUG":
            log_format = "[%(levelname)s] %(filename)s.%(funcName)s:%(lineno)d %(message)s"
        logging.basicConfig(level=log_level.upper(), format=log_format)
    except ValueError:
        click.echo(f"ERROR: '{log_level}' is not a valid logging level.")
        sys.exit(1)


uncross.help = f"{ASCII_ART}\nAn opinionated meta build system for C cross-compilation."
uncross.add_command(autocompletion)
uncross.add_command(build)
uncross.add_command(check)
uncross.add_command(clean)
uncross.add_command(config)
uncross.add_command(fmt)
uncross.add_command(lint)
uncross.add_command(new)
uncross.add_command(project)
uncross.add_command(release)
uncross.add_command(toolchain)
