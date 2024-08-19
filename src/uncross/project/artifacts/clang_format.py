"""Create .clang_format"""

from uncross.logger import make_logger
from uncross.programs.clang_format import invoke_clang_format

LOGGER = make_logger(__name__)


def drop_clang_format(path: str) -> None:
    """Drop clang format file"""
    args = [
        "clang-format",
        "--style",
        "{ BasedOnStyle: Microsoft, ColumnLimit: 80, SortIncludes: false }",
        "--dump-config",
    ]

    if invoke_clang_format(args, stdout_replace=path) != 0:
        raise RuntimeError


def create_dot_clang_format(_name: str, root: str) -> None:
    """Create .clang_format"""
    LOGGER.debug("creating clang format file at %s ...", root)
    drop_clang_format(f"{root}/.clang-format")
