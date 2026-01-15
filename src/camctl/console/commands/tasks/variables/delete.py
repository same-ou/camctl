"""Delete a task variable."""

from __future__ import annotations

import typer

from camctl.console.commands.tasks.variables import variables_app
from camctl.console.context import require_context
from camctl.console.display import print_summary


@variables_app.command(
    "delete",
    help="Delete a task variable.",
    short_help="Delete a variable.",
)
def delete_variable(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task identifier."),
    var_name: str = typer.Argument(..., help="Variable name."),
) -> None:
    """Delete a task variable by name."""
    context = require_context(ctx)
    with context.build_engine() as engine:
        engine.tasks.delete_variable(task_id, var_name)

    print_summary(f"Deleted variable {var_name}.")
