"""Local task variable CLI commands."""

from __future__ import annotations

import typer

local_app = typer.Typer(
    help="Manage local task variables.",
    epilog="Use `camctl tasks variables local COMMAND --help` for command-specific options.",
    no_args_is_help=True,
)

from . import list  # noqa: E402,F401
from . import get  # noqa: E402,F401
from . import update  # noqa: E402,F401
from . import delete  # noqa: E402,F401
from . import modify  # noqa: E402,F401

__all__ = ["local_app"]
