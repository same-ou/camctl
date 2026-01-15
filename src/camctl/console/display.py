"""Rich-powered display helpers for CLI output."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Callable, Iterable, Mapping, Sequence

import typer

from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table

from camctl.api.http import Page, Resource
from camctl.api.camunda.processes.models import ProcessInstance
from camctl.api.camunda.tasks.models import Task
from camctl.utils import dumps_json

_console = Console()


class OutputFormat(str, Enum):
    """Output formats supported by list commands."""

    TABLE = "table"
    JSON = "json"


TaskColumnSpec = tuple[str, Callable[[Task], Any], dict[str, Any]]
ProcessColumnSpec = tuple[str, Callable[[ProcessInstance], Any], dict[str, Any]]

_TASK_COLUMN_SPECS: dict[str, TaskColumnSpec] = {
    "id": ("ID", lambda task: task.id, {"style": "dim"}),
    "name": ("Name", lambda task: task.name, {}),
    "status": ("Status", lambda task: task.task_state or task.status, {}),
    "assignee": ("Assignee", lambda task: task.assignee, {}),
    "priority": ("Priority", lambda task: task.priority, {"justify": "right"}),
    "created": ("Created", lambda task: task.created, {}),
    "due": ("Due", lambda task: task.due, {}),
    "follow_up": ("Follow Up", lambda task: task.follow_up, {}),
    "last_updated": ("Last Updated", lambda task: task.last_updated, {}),
    "delegation_state": ("Delegation State", lambda task: task.delegation_state, {}),
    "description": ("Description", lambda task: task.description, {"overflow": "fold"}),
    "execution_id": ("Execution ID", lambda task: task.execution_id, {}),
    "owner": ("Owner", lambda task: task.owner, {}),
    "parent_task_id": ("Parent Task ID", lambda task: task.parent_task_id, {}),
    "process_definition_id": ("Process Definition ID", lambda task: task.process_definition_id, {}),
    "process_instance_id": ("Process Instance ID", lambda task: task.process_instance_id, {}),
    "case_definition_id": ("Case Definition ID", lambda task: task.case_definition_id, {}),
    "case_instance_id": ("Case Instance ID", lambda task: task.case_instance_id, {}),
    "case_execution_id": ("Case Execution ID", lambda task: task.case_execution_id, {}),
    "task_definition_key": ("Task Definition Key", lambda task: task.task_definition_key, {}),
    "suspended": ("Suspended", lambda task: task.suspended, {}),
    "form_key": ("Form Key", lambda task: task.form_key, {}),
    "camunda_form_ref": ("Camunda Form Ref", lambda task: task.camunda_form_ref, {}),
    "tenant_id": ("Tenant ID", lambda task: task.tenant_id, {}),
    "task_state": ("Task State", lambda task: task.task_state, {}),
}

_PROCESS_COLUMN_SPECS: dict[str, ProcessColumnSpec] = {
    "id": ("ID", lambda proc: proc.id, {"style": "dim"}),
    "definition_key": ("Definition Key", lambda proc: proc.definition_key, {}),
    "definition_id": ("Definition ID", lambda proc: proc.definition_id, {"overflow": "fold"}),
    "business_key": ("Business Key", lambda proc: proc.business_key, {}),
    "case_instance_id": ("Case Instance ID", lambda proc: proc.case_instance_id, {}),
    "ended": ("Ended", lambda proc: proc.ended, {}),
    "suspended": ("Suspended", lambda proc: proc.suspended, {}),
    "tenant_id": ("Tenant ID", lambda proc: proc.tenant_id, {}),
    "links": ("Links", lambda proc: proc.links, {"overflow": "fold"}),
}

_TASK_DEFAULT_COLUMNS = ("id", "name", "status", "assignee", "priority")
_PROCESS_DEFAULT_COLUMNS = (
    "id",
    "definition_key",
    "definition_id",
    "business_key",
    "ended",
    "suspended",
)


def task_column_names() -> tuple[str, ...]:
    """Return available task table columns."""
    return tuple(_TASK_COLUMN_SPECS.keys())


def process_column_names() -> tuple[str, ...]:
    """Return available process table columns."""
    return tuple(_PROCESS_COLUMN_SPECS.keys())


def _resolve_columns(
    requested: Sequence[str] | None,
    available: Mapping[str, tuple[str, Callable[..., Any], Mapping[str, Any]]],
    default: Sequence[str],
) -> list[str]:
    if not requested:
        return list(default)
    unknown = [column for column in requested if column not in available]
    if unknown:
        available_list = ", ".join(sorted(available))
        missing = ", ".join(unknown)
        raise ValueError(f"Unknown columns: {missing}. Available: {available_list}.")
    return list(requested)


def print_json(payload: Any, *, title: str | None = None) -> None:
    """Render a payload as pretty JSON using Rich."""
    if payload is None:
        _console.print("[yellow]No data returned.[/yellow]")
        return
    normalized = _normalize(payload)
    pretty = Pretty(normalized, expand_all=True)
    if title:
        _console.print(Panel(pretty, title=title))
    else:
        _console.print(pretty)


def print_raw_json(payload: Any) -> None:
    """Print a JSON payload without Rich formatting for piping tools like jq."""
    typer.echo(dumps_json(payload))


def print_tasks(page: Page[Task], *, columns: Sequence[str] | None = None) -> None:
    """Render a task page as a Rich table."""
    column_keys = _resolve_columns(columns, _TASK_COLUMN_SPECS, _TASK_DEFAULT_COLUMNS)
    table = Table(title="Tasks", header_style="bold cyan")
    for key in column_keys:
        label, _getter, column_kwargs = _TASK_COLUMN_SPECS[key]
        table.add_column(label, **column_kwargs)

    for task in page.items:
        row = []
        for key in column_keys:
            _label, getter, _column_kwargs = _TASK_COLUMN_SPECS[key]
            row.append(_string(getter(task)))
        table.add_row(*row)

    _console.print(table)
    _print_page_meta(page)


def print_processes(
    page: Page[ProcessInstance],
    *,
    columns: Sequence[str] | None = None,
) -> None:
    """Render a process page as a Rich table."""
    column_keys = _resolve_columns(columns, _PROCESS_COLUMN_SPECS, _PROCESS_DEFAULT_COLUMNS)
    table = Table(title="Processes", header_style="bold green")
    for key in column_keys:
        label, _getter, column_kwargs = _PROCESS_COLUMN_SPECS[key]
        table.add_column(label, **column_kwargs)

    for proc in page.items:
        row = []
        for key in column_keys:
            _label, getter, _column_kwargs = _PROCESS_COLUMN_SPECS[key]
            row.append(_string(getter(proc)))
        table.add_row(*row)

    _console.print(table)
    _print_page_meta(page)


def print_batch_results(
    title: str,
    results: Iterable[Mapping[str, Any]],
    *,
    id_key: str,
) -> None:
    """Render batch operation results as a table."""
    table = Table(title=title, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Status")
    table.add_column("Error", overflow="fold")

    for result in results:
        table.add_row(
            _string(result.get(id_key)),
            _string(result.get("status")),
            _string(result.get("error")),
        )

    _console.print(table)


def print_summary(message: str, *, style: str = "green") -> None:
    """Print a highlighted summary line."""
    _console.print(f"[{style}]{message}[/{style}]")


def _print_page_meta(page: Page[Any]) -> None:
    """Render pagination and sort metadata for a page."""
    meta: dict[str, Any] = {}
    if page.pagination:
        meta["pagination"] = asdict(page.pagination)
    if page.sort:
        meta["sort"] = asdict(page.sort)
    if meta:
        _console.print(Panel(Pretty(meta), title="Page Info"))


def _normalize(payload: Any) -> Any:
    """Normalize payloads into JSON-serializable structures."""
    if isinstance(payload, Resource):
        return _normalize(payload.to_dict())
    if is_dataclass(payload):
        return _normalize(asdict(payload))
    if isinstance(payload, dict):
        return {key: _normalize(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_normalize(item) for item in payload]
    if isinstance(payload, tuple):
        return [_normalize(item) for item in payload]
    return payload


def _string(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
