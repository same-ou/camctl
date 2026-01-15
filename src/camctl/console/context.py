"""Context objects shared across CLI commands."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import typer

from camctl.api.camunda import CamundaEngine


@dataclass
class CLIContext:
    """State container for CLI invocations."""

    authority: str
    scopes: Optional[Sequence[str]] = None

    def build_engine(self) -> CamundaEngine:
        """Instantiate a Camunda engine based on the CLI configuration."""
        return CamundaEngine()


def require_context(ctx: typer.Context) -> CLIContext:
    """Return the CLI context or raise a helpful error."""
    if isinstance(ctx.obj, CLIContext):
        return ctx.obj
    raise typer.BadParameter("Missing CLI context; check global options.")
