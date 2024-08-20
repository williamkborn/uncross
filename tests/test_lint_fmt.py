"""test uncross basic project"""

from __future__ import annotations

from uncross.testing.project import UncrossTestProject, project_vars
from uncross.testing.run import run_uncross_process


def test_repo_basic_create_lint_fmt():
    """Test creating a repo and linting/formatting"""

    _, project_name, test_src_directory = project_vars()

    test_project = UncrossTestProject(project_name, test_src_directory)

    # project starts with lint, this should fail
    return_code = run_uncross_process(
        ["uncross", "--level", "DEBUG", "lint", "-S", test_src_directory]
    )
    assert return_code != 0

    return_code = run_uncross_process(
        ["uncross", "--level", "DEBUG", "fmt", "-S", test_src_directory]
    )
    assert return_code == 0

    return_code = run_uncross_process(
        ["uncross", "--level", "DEBUG", "lint", "-S", test_src_directory]
    )
    assert return_code == 0

    test_project.teardown()
