"""Git repo helper functions"""

import os

import git

from uncross.__about__ import __version__
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def get_project_root() -> None:
    """Get the root path of the current project"""
    repo = git.Repo(os.path.curdir, search_parent_directories=True)
    return os.path.realpath(repo.working_dir)


def project_init_commit(base_path: str, project_name: str) -> None:
    """Initialize git repo and make first commit"""
    LOGGER.info("creating bare repo at %s ...", base_path)
    repo = git.Repo.init(base_path)

    LOGGER.info("adding files to repo ...")
    for file in repo.untracked_files:
        repo.index.add(file)

    commit_message = f"Project {project_name} initialized with uncross version {__version__}."

    LOGGER.info("commiting ...")
    repo.index.commit(commit_message)