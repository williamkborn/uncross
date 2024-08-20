"""Create .git_ignore"""

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def drop_git_ignore(path: str) -> None:
    """Drop git_ignore file"""

    git_ignore_contents = """
.vscode/
build/
release/
release.tar.gz
debug/
__pycache__/
dist/
*.o
*.a
*.so
"""
    with open(path, "w", encoding="utf-8") as git_ignore_file:
        git_ignore_file.write(git_ignore_contents)


def create_dot_git_ignore(_name: str, root: str) -> None:
    """Create .git_ignore"""
    LOGGER.debug("creating git_ignore file at %s ...", root)
    drop_git_ignore(f"{root}/.gitignore")
