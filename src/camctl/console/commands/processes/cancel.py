"""Cancel process instances in batch using concurrent requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import threading

import typer

from camctl.console.commands.processes import processes_app
from camctl.console.context import require_context
from camctl.console.display import print_batch_results, print_json, print_summary
from camctl.utils import gather, load_id_file, parse_id_list, write_json
from rich.progress import Progress, SpinnerColumn, TextColumn


@processes_app.command(
    "cancel",
    help="Cancel process instances by ID using concurrent requests.",
    short_help="Cancel multiple process instances.",
)
def cancel_processes(
    ctx: typer.Context,
    ids: str | None = typer.Option(
        None,
        "--ids",
        help="Comma-separated process instance IDs (for example, id1,id2).",
    ),
    file: Path | None = typer.Option(
        None,
        "--file",
        "-f",
        help="File containing process IDs (newline, comma, or JSON list).",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    max_workers: int = typer.Option(
        5,
        "--max-workers",
        "-w",
        help="Maximum number of concurrent cancel requests.",
        min=1,
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the batch cancel results to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
) -> None:
    """
    Cancel multiple process instances by ID.

    Provide IDs via --ids or load them from --file (supports JSON, comma, or newline).
    """
    if bool(ids) == bool(file):
        raise typer.BadParameter("Provide either --ids or --file.")

    try:
        if file:
            process_ids = load_id_file(file)
            print_summary(f"Loaded {len(process_ids)} process IDs from {file}", style="blue")
        else:
            process_ids = parse_id_list(ids or "")
            print_summary(f"Parsed {len(process_ids)} process IDs from --ids", style="blue")
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    if not process_ids:
        raise typer.BadParameter("No process IDs provided.")

    context = require_context(ctx)
    with context.build_engine() as engine:
        def _cancel(process_id: str) -> dict[str, Any]:
            try:
                response = engine.processes.cancel(process_id)
                return {
                    "process_id": process_id,
                    "status": "cancelled",
                    "response": response,
                }
            except Exception as exc:
                return {
                    "process_id": process_id,
                    "status": "error",
                    "error": str(exc),
                }

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[dim]{task.completed}/{task.total}[/dim]"),
        ) as progress:
            task_id = progress.add_task("Preparing cancellations...", total=len(process_ids))
            lock = threading.Lock()

            def _on_start(process_id: str) -> None:
                with lock:
                    progress.update(task_id, description=f"Cancelling {process_id}...")

            def _on_complete(process_id: str, result: Any) -> None:
                with lock:
                    progress.advance(task_id, 1)
                    status = "cancelled"
                    if isinstance(result, dict) and result.get("status") == "error":
                        status = "failed"
                    progress.update(task_id, description=f"{status.title()} {process_id}")

            results = gather(
                _cancel,
                process_ids,
                max_workers=max_workers,
                on_start=_on_start,
                on_complete=_on_complete,
            )

    success_count = sum(
        1 for result in results if isinstance(result, dict) and result.get("status") == "cancelled"
    )
    failure_count = len(results) - success_count

    payload = {
        "total": len(process_ids),
        "cancelled": success_count,
        "failed": failure_count,
        "results": results,
    }

    if output:
        write_json(payload, output)
        print_summary(f"Saved output to {output}", style="blue")

    summary_style = "green" if failure_count == 0 else "yellow"
    print_summary(
        f"Cancelled {success_count} process(es), {failure_count} failed.",
        style=summary_style,
    )
    print_batch_results("Cancel Results", payload["results"], id_key="process_id")
    print_json(payload, title="Cancel Summary")
