"""Process-related CLI commands."""

import typer

processes_app = typer.Typer(
    help="Manage Camunda processes.",
    epilog="Use `camctl processes COMMAND --help` for command-specific options.",
    no_args_is_help=True,
)

from . import get  # noqa: E402,F401
from . import list  # noqa: E402,F401
from . import cancel  # noqa: E402,F401
from . import variables  # noqa: E402,F401
from . import count  # noqa: E402,F401

__all__ = ["processes_app"]
