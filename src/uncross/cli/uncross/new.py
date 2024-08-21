"""new command"""

from __future__ import annotations

import sys

import click

from uncross.logger import make_logger
from uncross.project.create import create_project

LOGGER = make_logger(__name__)


def new_command(name: str | None, source_dir: str, build_project: bool, git: bool) -> None:
    """new project"""
    LOGGER.debug("Creating new project %s at %s ...", name, source_dir)
    if name is None:
        name = source_dir
    create_project(name, source_dir, build_project, git)


@click.command("new")
@click.argument("source_dir", type=str)
@click.option("-n", "--name", type=str, help="project name")
@click.option("--build", is_flag=True, required=False, help="build project on creation")
@click.option("--no-git", is_flag=True, required=False, help="initialize git repo")
def new(source_dir: str, name: str | None, build: bool, no_git: bool) -> None:
    """New project."""
    if name == "":
        name = source_dir
    LOGGER.debug("new command invoked with args:")
    LOGGER.debug("source dir: %s", source_dir)
    LOGGER.debug("name: %s", source_dir)
    if (" " in source_dir or "." in source_dir or "/" in source_dir) and name is None:
        LOGGER.error("'.', ' ', or '/' in path and name was not provided")
        sys.exit(1)

    new_command(name, source_dir, build, not no_git)
