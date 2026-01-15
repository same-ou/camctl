"""Fetch variables for a process instance."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.processes import processes_app
from camctl.console.context import require_context
from camctl.console.display import print_json, print_raw_json, print_summary
from camctl.utils import write_json


@processes_app.command(
    "variables",
    help="Fetch variables for a process instance.",
    short_help="Get process variables.",
)
def get_variables(
    ctx: typer.Context,
    process_id: str = typer.Argument(..., help="Process instance identifier."),
    deserialize_values: bool | None = typer.Option(
        None,
        "--deserialize-values/--no-deserialize-values",
        help="Control server-side value deserialization.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the variables response to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
    raw: bool = typer.Option(
        False,
        "--raw",
        help="Print raw JSON for piping (no Rich formatting).",
    ),
) -> None:
    """Retrieve variables for a process instance and print the JSON response."""
    context = require_context(ctx)
    with context.build_engine() as engine:
        payload = engine.processes.variables(
            process_id,
            deserialize_values=deserialize_values,
        )

    if payload is None:
        print_summary("Process not found.", style="yellow")
        return

    if output:
        write_json(payload, output)
        print_summary(f"Saved output to {output}", style="blue")

    if raw:
        print_raw_json(payload)
    else:
        print_json(payload, title="Process Variables")
