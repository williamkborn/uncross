"""test uncross basic project"""

from __future__ import annotations

import os
import secrets
import shutil
import sys
from multiprocessing import Process

from uncross.cli import uncross


def invoke_uncross(args: list[str]) -> None:
    """invoke uncross"""
    sys.argv = args
    uncross()


def run_uncross_test(args: list[str]):
    """run uncross test"""
    process = Process(target=invoke_uncross, args=[args])
    process.start()
    process.join()
    assert process.exitcode == 0


def test_repo_basic_create_build_check():
    """Test creating a repo and building binaries"""

    test_id = secrets.token_hex(12)
    test_src_directory = f"/tmp/test_uncross/{test_id}"
    test_build_directory = f"/tmp/test_uncross/{test_id}/build"

    run_uncross_test(["uncross", "new", test_src_directory, "--name", "test_project"])

    assert os.path.exists(test_src_directory)
    assert os.path.exists(f"{test_src_directory}/.clang-format")
    assert os.path.exists(f"{test_src_directory}/.clang-tidy")
    assert os.path.exists(f"{test_src_directory}/.gitignore")
    assert os.path.exists(f"{test_src_directory}/CMakeLists.txt")
    assert os.path.exists(f"{test_src_directory}/src/CMakeLists.txt")
    assert os.path.exists(f"{test_src_directory}/src/main.c")
    assert os.path.exists(f"{test_src_directory}/include/test_project.h")
    assert os.path.exists(f"{test_src_directory}/uncross.toml")

    run_uncross_test(
        ["uncross", "build", "-S", test_src_directory, "-B", test_build_directory, "--all"]
    )
    assert os.path.exists(f"{test_src_directory}/build")
    assert os.path.exists(f"{test_src_directory}/release/bin/test_project_Linux_x86_64")
    assert os.path.exists(f"{test_src_directory}/debug/bin/test_project_Linux_x86_64")

    run_uncross_test(
        ["uncross", "check", "-S", test_src_directory, "-B", test_build_directory, "--all"]
    )
    assert os.path.exists(
        f"{test_src_directory}/release/analysis/code_checker/reports/native/index.html"
    )
    assert os.path.exists(
        f"{test_src_directory}/debug/analysis/code_checker/reports/native/index.html"
    )

    shutil.rmtree(test_src_directory, ignore_errors=True)
