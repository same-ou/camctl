"""Fetch a single process from the Camunda API."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.processes import processes_app
from camctl.console.context import require_context
from camctl.console.display import print_json, print_summary
from camctl.utils import write_json


@processes_app.command(
    "get",
    help="Fetch a process instance by ID and print the JSON response.",
    short_help="Fetch a process instance by ID.",
)
def get_process(
    ctx: typer.Context,
    process_id: str = typer.Argument(
        ...,
        help="Process instance identifier (for example, 98765).",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the process response to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
) -> None:
    """
    Retrieve a process instance by its ID and print the JSON response.

    Use --output to persist the response to a JSON file.
    """
    context = require_context(ctx)
    with context.build_engine() as engine:
        payload = engine.processes.get(process_id)
    if payload is None:
        print_summary("Process not found.", style="yellow")
        return
    if output:
        write_json(payload, output)
        print_summary(f"Saved output to {output}", style="blue")
    print_json(payload, title="Process")
