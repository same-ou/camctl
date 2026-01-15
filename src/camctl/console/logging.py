"""Logging configuration for the camctl CLI."""

from __future__ import annotations

import logging
from typing import Mapping

import typer

_CAMCTL_FILTER = logging.Filter(name="camctl")

_LEVEL_COLORS: Mapping[int, str] = {
    logging.DEBUG: "magenta",
    logging.INFO: "blue",
    logging.WARNING: "yellow",
    logging.ERROR: "red",
    logging.CRITICAL: "red",
}


class TyperHandler(logging.Handler):
    """Logging handler that writes to the terminal using Typer."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
            color = _LEVEL_COLORS.get(record.levelno)
            styled = typer.style(message, fg=color) if color else message
            err = record.levelno >= logging.WARNING
            typer.echo(styled, err=err)
        except Exception:
            self.handleError(record)


def configure_logging(verbosity: int) -> None:
    """
    Configure logging for CLI runs.

    Args:
        verbosity: 0 = warnings only, 1 = info, 2+ = debug.
    """
    level = logging.WARNING
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO

    handler = TyperHandler()
    if verbosity >= 2:
        formatter = logging.Formatter("%(levelname)s %(name)s: %(message)s")
    else:
        formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    if verbosity < 2:
        handler.addFilter(_CAMCTL_FILTER)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(handler)
    logging.captureWarnings(True)
