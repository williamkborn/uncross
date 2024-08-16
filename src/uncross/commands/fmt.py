"""fmt command"""

from uncross.commands.lint import run_over_c_h_files
from uncross.git.repo import get_project_root
from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def fmt_command(source_dir: str) -> None:
    """fmt code"""
    LOGGER.info("formatting .c and .h files in %s", source_dir)
    args = ["clang-format", "-i", f"--style=file:{get_project_root()}/.clang-format"]
    format_failed = run_over_c_h_files(source_dir, args)

    if format_failed:
        raise RuntimeError
