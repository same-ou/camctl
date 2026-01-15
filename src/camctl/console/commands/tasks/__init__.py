"""Task-related CLI commands."""

import typer

tasks_app = typer.Typer(
    help="Manage Camunda tasks.",
    epilog="Use `camctl tasks COMMAND --help` for command-specific options.",
    no_args_is_help=True,
)

from .variables import variables_app  # noqa: E402
tasks_app.add_typer(variables_app, name="variables")

from . import get  # noqa: E402,F401
from . import list  # noqa: E402,F401
from . import complete  # noqa: E402,F401
from . import count  # noqa: E402,F401

__all__ = ["tasks_app"]
