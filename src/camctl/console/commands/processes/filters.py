"""Shared filter options for process instance queries."""

from __future__ import annotations

from dataclasses import fields
from typing import Any, Mapping, get_args

import typer

from camctl.api.camunda.resources.processes import ProcessFilterParams


def _is_optional_bool(annotation: Any) -> bool:
    if annotation is bool:
        return True
    return bool in get_args(annotation)


_FILTER_FIELDS = [field.name for field in fields(ProcessFilterParams)]
_BOOL_FIELDS = {
    name
    for name, annotation in ProcessFilterParams.__annotations__.items()
    if _is_optional_bool(annotation)
}

PROCESS_INSTANCE_IDS = typer.Option(
    None,
    "--process-instance-ids",
    help="Comma-separated process instance ids.",
)

BUSINESS_KEY = typer.Option(
    None,
    "--business-key",
    help="Process instance business key filter.",
)

BUSINESS_KEY_LIKE = typer.Option(
    None,
    "--business-key-like",
    help="Business key substring filter.",
)

CASE_INSTANCE_ID = typer.Option(
    None,
    "--case-instance-id",
    help="Case instance id filter.",
)

PROCESS_DEFINITION_ID = typer.Option(
    None,
    "--process-definition-id",
    help="Process definition id filter.",
)

PROCESS_DEFINITION_KEY = typer.Option(
    None,
    "--process-definition-key",
    help="Process definition key filter.",
)

PROCESS_DEFINITION_KEY_IN = typer.Option(
    None,
    "--process-definition-key-in",
    help="Comma-separated process definition keys.",
)

PROCESS_DEFINITION_KEY_NOT_IN = typer.Option(
    None,
    "--process-definition-key-not-in",
    help="Comma-separated process definition keys to exclude.",
)

DEPLOYMENT_ID = typer.Option(
    None,
    "--deployment-id",
    help="Deployment id filter.",
)

SUPER_PROCESS_INSTANCE = typer.Option(
    None,
    "--super-process-instance",
    help="Super process instance id filter.",
)

SUB_PROCESS_INSTANCE = typer.Option(
    None,
    "--sub-process-instance",
    help="Sub process instance id filter.",
)

SUPER_CASE_INSTANCE = typer.Option(
    None,
    "--super-case-instance",
    help="Super case instance id filter.",
)

SUB_CASE_INSTANCE = typer.Option(
    None,
    "--sub-case-instance",
    help="Sub case instance id filter.",
)

ACTIVE = typer.Option(
    False,
    "--active",
    help="Only include active process instances.",
)

SUSPENDED = typer.Option(
    False,
    "--suspended",
    help="Only include suspended process instances.",
)

WITH_INCIDENT = typer.Option(
    False,
    "--with-incident",
    help="Only include process instances with incidents.",
)

INCIDENT_ID = typer.Option(
    None,
    "--incident-id",
    help="Incident id filter.",
)

INCIDENT_TYPE = typer.Option(
    None,
    "--incident-type",
    help="Incident type filter.",
)

INCIDENT_MESSAGE = typer.Option(
    None,
    "--incident-message",
    help="Incident message filter (exact match).",
)

INCIDENT_MESSAGE_LIKE = typer.Option(
    None,
    "--incident-message-like",
    help="Incident message substring filter.",
)

TENANT_ID_IN = typer.Option(
    None,
    "--tenant-id-in",
    help="Comma-separated tenant ids.",
)

WITHOUT_TENANT_ID = typer.Option(
    False,
    "--without-tenant-id",
    help="Only include process instances with no tenant.",
)

PROCESS_DEFINITION_WITHOUT_TENANT_ID = typer.Option(
    False,
    "--process-definition-without-tenant-id",
    help="Only include instances whose process definition has no tenant id.",
)

ACTIVITY_ID_IN = typer.Option(
    None,
    "--activity-id-in",
    help="Comma-separated activity ids.",
)

ROOT_PROCESS_INSTANCES = typer.Option(
    False,
    "--root-process-instances",
    help="Only include root process instances.",
)

LEAF_PROCESS_INSTANCES = typer.Option(
    False,
    "--leaf-process-instances",
    help="Only include leaf process instances.",
)

VARIABLES = typer.Option(
    None,
    "--variables",
    help="Variable filter expressions.",
)

VARIABLE_NAMES_IGNORE_CASE = typer.Option(
    False,
    "--variable-names-ignore-case",
    help="Match variable names case-insensitively.",
)

VARIABLE_VALUES_IGNORE_CASE = typer.Option(
    False,
    "--variable-values-ignore-case",
    help="Match variable values case-insensitively.",
)


def build_process_filter_kwargs(values: Mapping[str, Any]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for name in _FILTER_FIELDS:
        if name not in values:
            continue
        value = values[name]
        if name in _BOOL_FIELDS:
            if value:
                data[name] = True
            continue
        if value is None:
            continue
        data[name] = value
    return data


def build_process_filters(values: Mapping[str, Any]) -> ProcessFilterParams:
    return ProcessFilterParams(**build_process_filter_kwargs(values))


__all__ = [
    "PROCESS_INSTANCE_IDS",
    "BUSINESS_KEY",
    "BUSINESS_KEY_LIKE",
    "CASE_INSTANCE_ID",
    "PROCESS_DEFINITION_ID",
    "PROCESS_DEFINITION_KEY",
    "PROCESS_DEFINITION_KEY_IN",
    "PROCESS_DEFINITION_KEY_NOT_IN",
    "DEPLOYMENT_ID",
    "SUPER_PROCESS_INSTANCE",
    "SUB_PROCESS_INSTANCE",
    "SUPER_CASE_INSTANCE",
    "SUB_CASE_INSTANCE",
    "ACTIVE",
    "SUSPENDED",
    "WITH_INCIDENT",
    "INCIDENT_ID",
    "INCIDENT_TYPE",
    "INCIDENT_MESSAGE",
    "INCIDENT_MESSAGE_LIKE",
    "TENANT_ID_IN",
    "WITHOUT_TENANT_ID",
    "PROCESS_DEFINITION_WITHOUT_TENANT_ID",
    "ACTIVITY_ID_IN",
    "ROOT_PROCESS_INSTANCES",
    "LEAF_PROCESS_INSTANCES",
    "VARIABLES",
    "VARIABLE_NAMES_IGNORE_CASE",
    "VARIABLE_VALUES_IGNORE_CASE",
    "build_process_filter_kwargs",
    "build_process_filters",
]
