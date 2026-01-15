"""List task variables."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.tasks.variables import variables_app
from camctl.console.context import require_context
from camctl.console.display import print_json, print_raw_json, print_summary
from camctl.utils import write_json


@variables_app.command(
    "list",
    help="List variables for a task.",
    short_help="List variables.",
)
def list_variables(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task identifier."),
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
    """Retrieve variables for a task and print the JSON response."""
    context = require_context(ctx)
    with context.build_engine() as engine:
        payload = engine.tasks.list_variables(
            task_id,
            deserialize_values=deserialize_values,
        )

    if output:
        write_json(payload, output)
        print_summary(f"Saved output to {output}", style="blue")

    if raw:
        print_raw_json(payload)
    else:
        print_json(payload, title="Task Variables")
