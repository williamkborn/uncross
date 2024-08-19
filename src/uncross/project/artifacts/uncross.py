"""Create uncross.toml"""

import toml

from uncross.logger import make_logger

LOGGER = make_logger(__name__)


def drop_uncross_toml(name, path: str) -> None:
    """Drop uncross.toml file"""
    document = {
        "uncross": {
            "project": {"name": name, "author": "John Doe", "email": "john.doe@example.com"},
            "toolchain": {"native": {}},
        }
    }

    with open(path, "w", encoding="utf-8") as config_file:
        config_file.write(toml.dumps(document))


def create_uncross_toml(name: str, root: str) -> None:
    """Create uncross.toml"""
    LOGGER.debug("creating uncross.toml file at %s ...", root)
    drop_uncross_toml(name, f"{root}/uncross.toml")
