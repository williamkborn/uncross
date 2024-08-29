"""Create a new project"""

from __future__ import annotations

import os
import pathlib

import rich.tree

from uncross.build_params import BuildParams
from uncross.cli.uncross.build import build_command
from uncross.git.repo import project_init_commit
from uncross.logger import make_logger
from uncross.project.artifacts.c_proj import create_c_project
from uncross.project.artifacts.clang_format import create_dot_clang_format
from uncross.project.artifacts.clang_tidy import create_dot_clang_tidy
from uncross.project.artifacts.cmake import create_cmakelists_txt
from uncross.project.artifacts.gitignore import create_dot_git_ignore
from uncross.project.artifacts.makefile import create_makefile
from uncross.project.artifacts.uncross import create_uncross_toml
from uncross.task.series_pipeline import SeriesPipeline

LOGGER = make_logger(__name__)


def display_project_overview_tree(source_dir: str) -> None:
    """Display project tree"""
    dir_style = "[magenta]"
    guide_style = "red"
    file_style = "[white]"

    def recurse_directory(directory: str, tree: rich.tree.Tree) -> None:
        """Recurse directory to fill project tree display"""

        paths: list[pathlib.Path] = sorted(
            pathlib.Path(directory).iterdir(), key=lambda p: (p.is_file(), p.name)
        )
        for path in paths:
            if path.is_dir():
                if path.name == "Debug":
                    debug_root = tree.add(f"{dir_style}{path.name}")
                    debug_root.add(f"{file_style}<debug build files>")
                elif path.name == "Release":
                    release_root = tree.add(f"{dir_style}{path.name}")
                    release_root.add(f"{file_style}<release build files>")
                elif path.name == ".git":
                    git_root = tree.add(f"{dir_style}{path.name}")
                    git_root.add(f"{file_style}<git files>")
                else:
                    recurse_directory(path, tree.add(f"{dir_style}{path.name}"))
            else:
                tree.add(f"{file_style}{path.name}")

    root = rich.tree.Tree(
        f"{dir_style}{source_dir}",
        guide_style=guide_style,
        hide_root=source_dir == pathlib.Path.cwd(),
    )
    recurse_directory(source_dir, root)
    rich.console.Console().print(root, markup=True)


def create_project(name: str, source_dir: str, build_project: bool, git: bool) -> None:
    """Create a builtool project tree"""

    if " " in name:
        msg = "Cannot have space in name"
        raise RuntimeError(msg)

    LOGGER.info("Creating project %s at %s...", name, source_dir)
    os.makedirs(source_dir, exist_ok=True)
    create_c_project(name, source_dir)
    create_dot_clang_format(name, source_dir)
    create_dot_clang_tidy(name, source_dir)
    create_cmakelists_txt(name, source_dir)
    create_dot_git_ignore(name, source_dir)
    create_makefile(name, source_dir)
    create_uncross_toml(name, source_dir)
    if build_project:
        params = BuildParams(
            build_dir=f"{source_dir}/build",
            source_dir=source_dir,
            build_debug=True,
            toolchains=["native"],
            presets=[],
            cmake_vars=[],
        )

        build_command(SeriesPipeline("build pipeline"), params)
        params.build_debug = False
        build_command(SeriesPipeline("build pipeline"), params)
    if git:
        project_init_commit(source_dir, name)
    display_project_overview_tree(source_dir)
