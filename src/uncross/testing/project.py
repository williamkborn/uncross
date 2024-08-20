"""Testing project"""

from __future__ import annotations

import os
import secrets
import shutil
from pathlib import Path

from uncross.testing.run import run_uncross_process


class UncrossTestProject:
    """Project for testing."""

    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = Path(path)
        self._setup()

    def _setup(self) -> None:
        """Setup test project."""
        run_uncross_process(["uncross", "new", str(self.path), "--name", self.name])
        assert os.path.exists(str(self.path))
        assert os.path.exists(f"{self.path!s}/.clang-format")
        assert os.path.exists(f"{self.path!s}/.clang-tidy")
        assert os.path.exists(f"{self.path!s}/.gitignore")
        assert os.path.exists(f"{self.path!s}/CMakeLists.txt")
        assert os.path.exists(f"{self.path!s}/src/CMakeLists.txt")
        assert os.path.exists(f"{self.path!s}/src/main.c")
        assert os.path.exists(f"{self.path!s}/include/{self.name}.h")
        assert os.path.exists(f"{self.path!s}/uncross.toml")

    def build(self) -> None:
        """Build project"""
        run_uncross_process(
            ["uncross", "build", "-S", str(self.path), "-B", f"{self.path!s}/build", "--all"]
        )
        assert os.path.exists(f"{self.path}/build")
        assert os.path.exists(f"{self.path}/release/bin/{self.name}_Linux_x86_64")
        assert os.path.exists(f"{self.path}/debug/bin/{self.name}_Linux_x86_64")

    def teardown(self) -> None:
        """Teardown project."""
        shutil.rmtree(self.path, ignore_errors=True)


def project_vars() -> tuple[str, str, str]:
    """Vars to seed test project"""
    test_id = secrets.token_hex(12)
    project_name = "testproject"
    test_src_directory = f"/tmp/test_uncross/{test_id}"  # noqa: S108

    return test_id, project_name, test_src_directory
