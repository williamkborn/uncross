# SPDX-FileCopyrightText: 2024-present William Born <william.born.git@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from uncross.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="uncross")
def uncross():
    click.echo("Hello world!")
