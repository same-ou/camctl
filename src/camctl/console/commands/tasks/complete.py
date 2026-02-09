"""Complete a task using variables and optional comments."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.api.camunda.resources.tasks import TaskCompletionRequest
from camctl.console.commands.tasks import tasks_app
from camctl.console.context import require_context
from camctl.console.display import print_json, print_summary
from camctl.console.inputs import merge_mappings, parse_json_mapping, parse_key_value_pairs
from camctl.utils import write_json


@tasks_app.command(
    "complete",
    help="Complete a task with variables and an optional comment.",
    short_help="Complete a task.",
)
def complete_task(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task identifier."),
    variables: str | None = typer.Option(
        None,
        "--variables",
        help="JSON object with task variables.",
    ),
    variables_file: Path | None = typer.Option(
        None,
        "--variables-file",
        help="Path to a JSON file with task variables.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    var: list[str] = typer.Option(
        None,
        "--var",
        help="Variables as key=value (repeatable).",
    ),
    comment: str | None = typer.Option(
        None,
        "--comment",
        help="Optional completion comment.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the completion response to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
) -> None:
    """Complete a task and print the response."""
    try:
        file_vars = parse_json_mapping(None, variables_file)
        json_vars = parse_json_mapping(variables, None)
        kv_vars = parse_key_value_pairs(var or [])
        merged = merge_mappings(file_vars, json_vars, kv_vars)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    payload = TaskCompletionRequest(variables=merged, comment=comment)

    context = require_context(ctx)
    with context.build_engine() as engine:
        response = engine.tasks.complete(task_id, payload=payload)

    if response is None:
        print_summary("Task not found or no content returned.", style="yellow")
        return

    if output:
        write_json(response, output)

    print_json(response, title="Task Completion")
