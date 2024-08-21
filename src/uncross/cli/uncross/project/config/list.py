"""config list command"""

import click
import toml
from rich.console import Console
from rich.pretty import pprint
from rich.syntax import Syntax

from uncross.config.project.parse import parse_project_config


@click.command("list")
@click.option("as_json", "--json", is_flag=True, help="display as json")
def config_list(as_json: bool) -> None:
    """New project."""
    config = parse_project_config()

    if as_json is False:
        Console().print(Syntax(toml.dumps(config), "toml", line_numbers=True))
    else:
        pprint(config)
