"""Create Makefile"""

import os

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def drop_root_makefile(_name: str, path: str) -> None:
    """Create C Source file"""

    root_makefile_content = """
.POSIX:
UNCROSS=uncross

all: debug

build-debug:
\t$(UNCROSS) build --debug

build-release:
\t$(UNCROSS) build --release

check-debug: build-debug
\t$(UNCROSS) check --debug

check-release: build-release
\t$(UNCROSS) check --release

clean:
\t$(UNCROSS) clean

debug: fmt build-debug check-debug

format: fmt
fmt:
\t$(UNCROSS) fmt

lint:
\t$(UNCROSS) lint

release: lint build-release check-release

.PHONY: all build-debug build-release check-debug check-release clean debug format fmt lint release

"""

    with open(path, "w", encoding="utf-8") as root_makefile_file:
        root_makefile_file.write(root_makefile_content)


def create_makefile(name: str, root: str) -> None:
    """Create makefile at project root"""
    LOGGER.debug("creating cmake C project structure at %s ...", root)
    os.makedirs(f"{root}/src", exist_ok=True)
    drop_root_makefile(name, f"{root}/Makefile")
