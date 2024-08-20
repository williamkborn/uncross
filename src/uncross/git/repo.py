"""Git repo helper functions"""

import os

import git

from uncross.__about__ import __version__
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def get_project_root(search_path: str = ".") -> str:
    """Get the root path of the current project"""
    try:
        repo = git.Repo(search_path, search_parent_directories=True)
        return os.path.realpath(repo.working_dir)
    except git.exc.InvalidGitRepositoryError:
        LOGGER.warning(
            "current directory is not in a git repo,"
            "uncross works best when the project is "
            "committed at the root of a git repo."
        )
        return os.path.realpath(os.curdir)


def project_init_commit(base_path: str, project_name: str) -> None:
    """Initialize git repo and make first commit"""
    LOGGER.debug("creating bare repo at %s ...", base_path)
    repo = git.Repo.init(base_path)

    LOGGER.debug("adding files to repo ...")
    for file in repo.untracked_files:
        LOGGER.debug("adding %s to repo ...", file)
        repo.index.add(file)

    commit_message = f"Project {project_name} initialized with uncross version {__version__}."

    LOGGER.debug("committing ...")
    repo.index.commit(commit_message)
