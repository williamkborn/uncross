"""test uncross basic project"""

from __future__ import annotations

import os

from uncross.testing.project import UncrossTestProject, project_vars
from uncross.testing.run import run_uncross_process


def test_repo_basic_check():
    """Test creating a repo and building binaries"""

    _, project_name, test_src_directory = project_vars()
    test_build_directory = f"{test_src_directory}/build"

    test_project = UncrossTestProject(project_name, test_src_directory)

    test_project.build()

    run_uncross_process(
        ["uncross", "check", "-S", test_src_directory, "-B", test_build_directory, "--all"]
    )
    assert os.path.exists(
        f"{test_src_directory}/release/analysis/code_checker/reports/native/index.html"
    )
    assert os.path.exists(
        f"{test_src_directory}/debug/analysis/code_checker/reports/native/index.html"
    )

    test_project.teardown()
