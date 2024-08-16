"""Create .clang_tidy"""

from uncross.logger import make_logger
from uncross.programs.clang_tidy import invoke_clang_tidy

LOGGER = make_logger(__name__)


def drop_clang_tidy(path: str) -> None:
    """Drop clang tidy file"""
    args = [
        "clang-tidy",
        '--checks="*,-altera*,-llvm-libc*,-android*"',
        "--dump-config",
    ]

    if invoke_clang_tidy(args, stdout_replace=path) != 0:
        raise RuntimeError


def create_dot_clang_tidy(_name: str, root: str) -> None:
    """Create .clang_tidy"""
    LOGGER.debug("creating clang tidy file at %s ...", root)
    drop_clang_tidy(f"{root}/.clang-tidy")
