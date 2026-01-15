"""Fetch a single task from the Camunda API."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.tasks import tasks_app
from camctl.console.context import require_context
from camctl.console.display import print_json, print_summary
from camctl.utils import write_json


@tasks_app.command(
    "get",
    help="Fetch a task by ID and print the JSON response.",
    short_help="Fetch a task by ID.",
)
def get_task(
    ctx: typer.Context,
    task_id: str = typer.Argument(
        ...,
        help="Task identifier (for example, 12345).",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the task response to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
) -> None:
    """
    Retrieve a task by its ID and print the JSON response.

    Use --output to persist the response to a JSON file.
    """
    context = require_context(ctx)
    with context.build_engine() as engine:
        payload = engine.tasks.get(task_id)
    if payload is None:
        print_summary("Task not found.", style="yellow")
        return
    if output:
        write_json(payload, output)
        print_summary(f"Saved output to {output}", style="blue")
    print_json(payload, title="Task")
