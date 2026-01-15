"""Typer application entrypoint for camctl."""

from __future__ import annotations

import httpx
import typer
from rich.console import Console

from camctl.console.logging import configure_logging
from camctl.console.context import CLIContext
from camctl.console.commands.processes import processes_app
from camctl.console.commands.tasks import tasks_app


class CamctlApp(typer.Typer):
    """Typer app with friendly network error handling."""

    def __call__(self, *args, **kwargs):
        try:
            return super().__call__(*args, **kwargs)
        except (httpx.ConnectError, httpx.ConnectTimeout):
            console = Console(stderr=True)
            console.print(
                "[red][!][/red] Camunda server is not reachable. "
                "Check the server URL and that it is running."
            )
            return 1


app = CamctlApp(
    help="Camunda CLI for interacting with task and process services.",
    epilog="Env vars: CAMCTL_AUTHORITY.",
    no_args_is_help=True,
)

_BANNER = "\n".join(
    [
        "█▀▀ ▄▀█ █▀▄▀█ █▀▀ ▀█▀ █░░",
        "█▄▄ █▀█ █░▀░█ █▄▄ ░█░ █▄▄",
    ]
)


@app.callback()
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help="Increase logging verbosity (-v for info, -vv for debug).",
    ),
    authority: str = typer.Option(
        "uat",
        envvar="CAMCTL_AUTHORITY",
        help="Target authority (uat or prod).",
    ),
    scope: list[str] | None = typer.Option(
        None,
        "--scope",
        "-s",
        help="Optional OAuth scopes (repeat flag for multiple).",
    ),
) -> None:
    """Configure shared CLI state used by all commands."""
    configure_logging(verbose)
    if ctx.invoked_subcommand is None:
        Console().print(f"[bold cyan]{_BANNER}[/bold cyan]")
    ctx.obj = CLIContext(
        authority=authority,
        scopes=scope,
    )


app.add_typer(tasks_app, name="tasks")
app.add_typer(processes_app, name="processes")
