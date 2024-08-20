"""test uncross basic project"""

from __future__ import annotations

import os

from uncross.testing.project import UncrossTestProject, project_vars
from uncross.testing.run import run_uncross_process


def test_repo_bootlin_toolchain():
    """Test creating a repo and building binaries"""
    _, project_name, test_src_directory = project_vars()
    test_project = UncrossTestProject(project_name, test_src_directory)
    return_code = run_uncross_process(
        [
            "uncross",
            "--level",
            "DEBUG",
            "toolchain",
            "register",
            "bootlin",
            "-S",
            test_src_directory,
            "--arch",
            "armv5-eabi",
        ]
    )
    assert return_code == 0
    test_project.build()
    assert os.path.exists(f"{test_src_directory}/release/bin/{project_name}_Linux_armv5l")
    assert os.path.exists(f"{test_src_directory}/debug/bin/{project_name}_Linux_armv5l")

    test_project.teardown()
