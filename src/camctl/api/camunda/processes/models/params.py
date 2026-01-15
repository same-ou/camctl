"""Query parameter models for process endpoints."""

from __future__ import annotations

from dataclasses import dataclass

from camctl.api.http import Params


@dataclass(kw_only=True)
class ProcessFilterParams(Params):
    """Filters for process instance queries."""

    process_instance_ids: str | None = None
    business_key: str | None = None
    business_key_like: str | None = None
    case_instance_id: str | None = None
    process_definition_id: str | None = None
    process_definition_key: str | None = None
    process_definition_key_in: str | None = None
    process_definition_key_not_in: str | None = None
    deployment_id: str | None = None
    super_process_instance: str | None = None
    sub_process_instance: str | None = None
    super_case_instance: str | None = None
    sub_case_instance: str | None = None
    active: bool | None = None
    suspended: bool | None = None
    with_incident: bool | None = None
    incident_id: str | None = None
    incident_type: str | None = None
    incident_message: str | None = None
    incident_message_like: str | None = None
    tenant_id_in: str | None = None
    without_tenant_id: bool | None = None
    process_definition_without_tenant_id: bool | None = None
    activity_id_in: str | None = None
    root_process_instances: bool | None = None
    leaf_process_instances: bool | None = None
    variables: str | None = None
    variable_names_ignore_case: bool | None = None
    variable_values_ignore_case: bool | None = None


@dataclass(kw_only=True)
class ProcessListParams(ProcessFilterParams):
    """Parameters for listing process instances."""

    page: int | None = None
    size: int | None = None
    first_result: int | None = None
    max_results: int | None = None
    sort_by: str | None = None
    sort_order: str | None = None
