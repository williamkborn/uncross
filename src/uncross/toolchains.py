"""Toolchain management"""

from __future__ import annotations

import os
from pathlib import Path

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def enumerate_toolchains() -> dict[str, list]:
    """Get all available toolchains."""
    to_return: dict[str, list] = {}

    search_locations = (Path.home() / ".uncross" / "toolchains", Path("/opt/cross"))

    for location in search_locations:
        if not location.exists():
            continue

        path = Path(location)

        if not path.is_dir():
            continue

        to_return[str(location)] = []

        for toolchain in path.iterdir():
            if not toolchain.is_dir():
                continue
            to_return[str(location)].append(toolchain.name)

    return to_return


def find_toolchain_file(location: str, toolchain: str) -> Path | None:
    """find toolchain file given"""

    possibles = ("toolchainfile.cmake", "toolchain.cmake")

    path = Path(f"{location}/{toolchain}")
    LOGGER.debug("checking %s", path)

    if not path.exists():
        return None

    for loc, _, files in os.walk(str(path)):
        for item in files:
            if item in possibles:
                LOGGER.debug("found: %s", item)
                return path / loc / item

    return None


def get_toolchain_file_by_name(name: str) -> Path | None:
    """Get toolchain file by toolchain name"""
    toolchains = enumerate_toolchains()

    for location, possibles in toolchains.items():
        for toolchain in possibles:
            if toolchain == name:
                possible = find_toolchain_file(location, toolchain)
                if possible is None:
                    continue
                return possible

    return None
