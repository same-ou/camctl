"""Update a task variable."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.api.camunda.tasks import TaskVariablePayload
from camctl.console.commands.tasks.variables import variables_app
from camctl.console.commands.tasks.variables.common import parse_value, parse_value_info
from camctl.console.context import require_context
from camctl.console.display import print_summary


@variables_app.command(
    "update",
    help="Update a task variable.",
    short_help="Update a variable.",
)
def update_variable(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task identifier."),
    var_name: str = typer.Argument(..., help="Variable name."),
    value: str = typer.Option(
        ...,
        "--value",
        help="Variable value (JSON is accepted).",
    ),
    var_type: str | None = typer.Option(
        None,
        "--type",
        help="Optional Camunda variable type.",
    ),
    value_info: str | None = typer.Option(
        None,
        "--value-info",
        help="JSON object for valueInfo.",
    ),
    value_info_file: Path | None = typer.Option(
        None,
        "--value-info-file",
        help="Path to a JSON file with valueInfo.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
) -> None:
    """Update a task variable by name."""
    try:
        parsed_value = parse_value(value)
        info_payload = parse_value_info(value_info, value_info_file)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    payload = TaskVariablePayload(
        value=parsed_value,
        type=var_type,
        value_info=info_payload,
    )

    context = require_context(ctx)
    with context.build_engine() as engine:
        engine.tasks.update_variable(task_id, var_name, payload=payload)

    print_summary(f"Updated variable {var_name}.")
