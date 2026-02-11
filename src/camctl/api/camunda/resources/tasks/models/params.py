"""Query parameter models for task endpoints."""

from __future__ import annotations

from dataclasses import dataclass

from camctl.api.http import SerializeMixin


@dataclass(kw_only=True)
class TaskFilterParams(SerializeMixin):
    """Filters for task queries."""

    task_id: str | None = None
    task_id_in: str | None = None
    process_instance_id: str | None = None
    process_instance_id_in: str | None = None
    process_instance_business_key: str | None = None
    process_instance_business_key_expression: str | None = None
    process_instance_business_key_in: str | None = None
    process_instance_business_key_like: str | None = None
    process_instance_business_key_like_expression: str | None = None
    process_definition_id: str | None = None
    process_definition_key: str | None = None
    process_definition_key_in: str | None = None
    process_definition_name: str | None = None
    process_definition_name_like: str | None = None
    execution_id: str | None = None
    case_instance_id: str | None = None
    case_instance_business_key: str | None = None
    case_instance_business_key_like: str | None = None
    case_definition_id: str | None = None
    case_definition_key: str | None = None
    case_definition_name: str | None = None
    case_definition_name_like: str | None = None
    case_execution_id: str | None = None
    activity_instance_id_in: str | None = None
    tenant_id_in: str | None = None
    without_tenant_id: bool | None = None
    assignee: str | None = None
    assignee_expression: str | None = None
    assignee_like: str | None = None
    assignee_like_expression: str | None = None
    assignee_in: str | None = None
    assignee_not_in: str | None = None
    owner: str | None = None
    owner_expression: str | None = None
    candidate_group: str | None = None
    candidate_group_like: str | None = None
    candidate_group_expression: str | None = None
    candidate_user: str | None = None
    candidate_user_expression: str | None = None
    include_assigned_tasks: bool | None = None
    involved_user: str | None = None
    involved_user_expression: str | None = None
    assigned: bool | None = None
    unassigned: bool | None = None
    task_definition_key: str | None = None
    task_definition_key_in: str | None = None
    task_definition_key_like: str | None = None
    name: str | None = None
    name_not_equal: str | None = None
    name_like: str | None = None
    name_not_like: str | None = None
    description: str | None = None
    description_like: str | None = None
    priority: int | None = None
    max_priority: int | None = None
    min_priority: int | None = None
    due_date: str | None = None
    due_date_expression: str | None = None
    due_after: str | None = None
    due_after_expression: str | None = None
    due_before: str | None = None
    due_before_expression: str | None = None
    without_due_date: bool | None = None
    follow_up_date: str | None = None
    follow_up_date_expression: str | None = None
    follow_up_after: str | None = None
    follow_up_after_expression: str | None = None
    follow_up_before: str | None = None
    follow_up_before_expression: str | None = None
    follow_up_before_or_not_existent: str | None = None
    follow_up_before_or_not_existent_expression: str | None = None
    created_on: str | None = None
    created_on_expression: str | None = None
    created_after: str | None = None
    created_after_expression: str | None = None
    created_before: str | None = None
    created_before_expression: str | None = None
    updated_after: str | None = None
    updated_after_expression: str | None = None
    delegation_state: str | None = None
    candidate_groups: str | None = None
    candidate_groups_expression: str | None = None
    with_candidate_groups: bool | None = None
    without_candidate_groups: bool | None = None
    with_candidate_users: bool | None = None
    without_candidate_users: bool | None = None
    active: bool | None = None
    suspended: bool | None = None
    task_variables: str | None = None
    process_variables: str | None = None
    case_instance_variables: str | None = None
    variable_names_ignore_case: bool | None = None
    variable_values_ignore_case: bool | None = None
    parent_task_id: str | None = None
    with_comment_attachment_info: bool | None = None
    status: str | None = None


@dataclass(kw_only=True)
class TaskListParams(TaskFilterParams):
    """Parameters for listing tasks."""

    page: int | None = None
    size: int | None = None
    first_result: int | None = None
    max_results: int | None = None
    sort_by: str | None = None
    sort_order: str | None = None
