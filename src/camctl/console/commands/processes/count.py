"""Count process instances from the Camunda API."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.processes import processes_app
from camctl.console.commands.processes import filters as process_filters
from camctl.console.context import require_context
from camctl.console.display import OutputFormat, print_json, print_raw_json, print_summary
from camctl.utils import write_json


@processes_app.command(
    "count",
    help="Count process instances with optional filters.",
    short_help="Count process instances.",
)
def count_processes(
    ctx: typer.Context,
    process_instance_ids: str | None = process_filters.PROCESS_INSTANCE_IDS,
    business_key: str | None = process_filters.BUSINESS_KEY,
    business_key_like: str | None = process_filters.BUSINESS_KEY_LIKE,
    case_instance_id: str | None = process_filters.CASE_INSTANCE_ID,
    process_definition_id: str | None = process_filters.PROCESS_DEFINITION_ID,
    process_definition_key: str | None = process_filters.PROCESS_DEFINITION_KEY,
    process_definition_key_in: str | None = process_filters.PROCESS_DEFINITION_KEY_IN,
    process_definition_key_not_in: str | None = process_filters.PROCESS_DEFINITION_KEY_NOT_IN,
    deployment_id: str | None = process_filters.DEPLOYMENT_ID,
    super_process_instance: str | None = process_filters.SUPER_PROCESS_INSTANCE,
    sub_process_instance: str | None = process_filters.SUB_PROCESS_INSTANCE,
    super_case_instance: str | None = process_filters.SUPER_CASE_INSTANCE,
    sub_case_instance: str | None = process_filters.SUB_CASE_INSTANCE,
    active: bool = process_filters.ACTIVE,
    suspended: bool = process_filters.SUSPENDED,
    with_incident: bool = process_filters.WITH_INCIDENT,
    incident_id: str | None = process_filters.INCIDENT_ID,
    incident_type: str | None = process_filters.INCIDENT_TYPE,
    incident_message: str | None = process_filters.INCIDENT_MESSAGE,
    incident_message_like: str | None = process_filters.INCIDENT_MESSAGE_LIKE,
    tenant_id_in: str | None = process_filters.TENANT_ID_IN,
    without_tenant_id: bool = process_filters.WITHOUT_TENANT_ID,
    process_definition_without_tenant_id: bool = (
        process_filters.PROCESS_DEFINITION_WITHOUT_TENANT_ID
    ),
    activity_id_in: str | None = process_filters.ACTIVITY_ID_IN,
    root_process_instances: bool = process_filters.ROOT_PROCESS_INSTANCES,
    leaf_process_instances: bool = process_filters.LEAF_PROCESS_INSTANCES,
    variables: str | None = process_filters.VARIABLES,
    variable_names_ignore_case: bool = process_filters.VARIABLE_NAMES_IGNORE_CASE,
    variable_values_ignore_case: bool = process_filters.VARIABLE_VALUES_IGNORE_CASE,
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the process count response to a JSON file.",
        dir_okay=False,
        resolve_path=True,
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.TABLE,
        "--format",
        help="Output format for count results.",
        case_sensitive=False,
    ),
    raw: bool = typer.Option(
        False,
        "--raw",
        help="Print raw JSON instead of a summary.",
    ),
) -> None:
    """Count process instances with filters."""
    filters = process_filters.build_process_filters(locals())
    context = require_context(ctx)
    with context.build_engine() as engine:
        count = engine.processes.count(params=filters)

    payload = {"count": count}
    if output:
        write_json(payload, output)

    if raw:
        print_raw_json(payload)
        return

    if format is OutputFormat.JSON:
        print_json(payload, title="Process Count")
        return

    print_summary(f"{count} process instance(s)")
