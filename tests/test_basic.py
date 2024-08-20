"""test uncross basic project"""

from __future__ import annotations

from uncross.testing.project import UncrossTestProject, project_vars


def test_repo_basic_create_build():
    """Test creating a repo and building binaries"""
    _, project_name, test_src_directory = project_vars()
    test_project = UncrossTestProject(project_name, test_src_directory)
    test_project.build()
    test_project.teardown()
