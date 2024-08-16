"""Build params."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BuildParams:
    """Parameter for building"""

    build_dir: str = "./build"
    source_dir: str = "."
    build_debug: bool = True
    cmake_vars: list[str] = ()
    toolchains: list[str] = ()
    presets: list[str] = ()
