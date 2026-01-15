"""Modify local task variables."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.api.camunda.tasks import TaskVariableModificationRequest
from camctl.console.commands.tasks.variables.common import load_modifications
from camctl.console.commands.tasks.variables.local import local_app
from camctl.console.context import require_context
from camctl.console.display import print_summary


@local_app.command(
    "modify",
    help="Update and delete local task variables in a single request.",
    short_help="Modify local variables.",
)
def modify_local_variables(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task identifier."),
    modifications: str | None = typer.Option(
        None,
        "--modifications",
        help="JSON object of variable modifications.",
    ),
    modifications_file: Path | None = typer.Option(
        None,
        "--modifications-file",
        help="Path to a JSON file with variable modifications.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    delete: list[str] | None = typer.Option(
        None,
        "--delete",
        help="Variable names to delete (repeatable).",
    ),
) -> None:
    """Modify local task variables with a bulk request."""
    try:
        modifications_payload = load_modifications(modifications, modifications_file)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    deletions = delete or None
    if not modifications_payload and not deletions:
        raise typer.BadParameter("Provide modifications or delete at least one variable.")

    payload = TaskVariableModificationRequest(
        modifications=modifications_payload,
        deletions=deletions,
    )

    context = require_context(ctx)
    with context.build_engine() as engine:
        engine.tasks.modify_local_variables(task_id, payload=payload)

    print_summary("Local variable updates applied.")
