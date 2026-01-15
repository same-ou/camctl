"""Task variable CLI commands."""

from __future__ import annotations

import typer

variables_app = typer.Typer(
    help="Manage task variables.",
    epilog="Use `camctl tasks variables COMMAND --help` for command-specific options.",
    no_args_is_help=True,
)

from .local import local_app  # noqa: E402

variables_app.add_typer(local_app, name="local")

from . import list  # noqa: E402,F401
from . import get  # noqa: E402,F401
from . import update  # noqa: E402,F401
from . import delete  # noqa: E402,F401
from . import modify  # noqa: E402,F401
from .local import list  # noqa: E402,F401
from .local import get  # noqa: E402,F401
from .local import update  # noqa: E402,F401
from .local import delete  # noqa: E402,F401
from .local import modify  # noqa: E402,F401

__all__ = ["variables_app"]
