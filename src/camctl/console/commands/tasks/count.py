"""Count tasks from the Camunda API."""

from __future__ import annotations

from pathlib import Path

import typer

from camctl.console.commands.tasks import tasks_app
from camctl.console.commands.tasks import filters as task_filters
from camctl.console.context import require_context
from camctl.console.display import OutputFormat, print_json, print_raw_json, print_summary
from camctl.utils import write_json


@tasks_app.command(
    "count",
    help="Count tasks with optional filters.",
    short_help="Count tasks.",
)
def count_tasks(
    ctx: typer.Context,
    task_id: str | None = task_filters.TASK_ID,
    task_id_in: str | None = task_filters.TASK_ID_IN,
    process_instance_id: str | None = task_filters.PROCESS_INSTANCE_ID,
    process_instance_id_in: str | None = task_filters.PROCESS_INSTANCE_ID_IN,
    process_instance_business_key: str | None = task_filters.PROCESS_INSTANCE_BUSINESS_KEY,
    process_instance_business_key_expression: str | None = task_filters.PROCESS_INSTANCE_BUSINESS_KEY_EXPRESSION,
    process_instance_business_key_in: str | None = task_filters.PROCESS_INSTANCE_BUSINESS_KEY_IN,
    process_instance_business_key_like: str | None = task_filters.PROCESS_INSTANCE_BUSINESS_KEY_LIKE,
    process_instance_business_key_like_expression: str | None = task_filters.PROCESS_INSTANCE_BUSINESS_KEY_LIKE_EXPRESSION,
    process_definition_id: str | None = task_filters.PROCESS_DEFINITION_ID,
    process_definition_key: str | None = task_filters.PROCESS_DEFINITION_KEY,
    process_definition_key_in: str | None = task_filters.PROCESS_DEFINITION_KEY_IN,
    process_definition_name: str | None = task_filters.PROCESS_DEFINITION_NAME,
    process_definition_name_like: str | None = task_filters.PROCESS_DEFINITION_NAME_LIKE,
    execution_id: str | None = task_filters.EXECUTION_ID,
    case_instance_id: str | None = task_filters.CASE_INSTANCE_ID,
    case_instance_business_key: str | None = task_filters.CASE_INSTANCE_BUSINESS_KEY,
    case_instance_business_key_like: str | None = task_filters.CASE_INSTANCE_BUSINESS_KEY_LIKE,
    case_definition_id: str | None = task_filters.CASE_DEFINITION_ID,
    case_definition_key: str | None = task_filters.CASE_DEFINITION_KEY,
    case_definition_name: str | None = task_filters.CASE_DEFINITION_NAME,
    case_definition_name_like: str | None = task_filters.CASE_DEFINITION_NAME_LIKE,
    case_execution_id: str | None = task_filters.CASE_EXECUTION_ID,
    activity_instance_id_in: str | None = task_filters.ACTIVITY_INSTANCE_ID_IN,
    tenant_id_in: str | None = task_filters.TENANT_ID_IN,
    without_tenant_id: bool = task_filters.WITHOUT_TENANT_ID,
    assignee: str | None = task_filters.ASSIGNEE,
    assignee_expression: str | None = task_filters.ASSIGNEE_EXPRESSION,
    assignee_like: str | None = task_filters.ASSIGNEE_LIKE,
    assignee_like_expression: str | None = task_filters.ASSIGNEE_LIKE_EXPRESSION,
    assignee_in: str | None = task_filters.ASSIGNEE_IN,
    assignee_not_in: str | None = task_filters.ASSIGNEE_NOT_IN,
    owner: str | None = task_filters.OWNER,
    owner_expression: str | None = task_filters.OWNER_EXPRESSION,
    candidate_group: str | None = task_filters.CANDIDATE_GROUP,
    candidate_group_like: str | None = task_filters.CANDIDATE_GROUP_LIKE,
    candidate_group_expression: str | None = task_filters.CANDIDATE_GROUP_EXPRESSION,
    candidate_user: str | None = task_filters.CANDIDATE_USER,
    candidate_user_expression: str | None = task_filters.CANDIDATE_USER_EXPRESSION,
    include_assigned_tasks: bool = task_filters.INCLUDE_ASSIGNED_TASKS,
    involved_user: str | None = task_filters.INVOLVED_USER,
    involved_user_expression: str | None = task_filters.INVOLVED_USER_EXPRESSION,
    assigned: bool = task_filters.ASSIGNED,
    unassigned: bool = task_filters.UNASSIGNED,
    task_definition_key: str | None = task_filters.TASK_DEFINITION_KEY,
    task_definition_key_in: str | None = task_filters.TASK_DEFINITION_KEY_IN,
    task_definition_key_like: str | None = task_filters.TASK_DEFINITION_KEY_LIKE,
    name: str | None = task_filters.NAME,
    name_not_equal: str | None = task_filters.NAME_NOT_EQUAL,
    name_like: str | None = task_filters.NAME_LIKE,
    name_not_like: str | None = task_filters.NAME_NOT_LIKE,
    description: str | None = task_filters.DESCRIPTION,
    description_like: str | None = task_filters.DESCRIPTION_LIKE,
    priority: int | None = task_filters.PRIORITY,
    max_priority: int | None = task_filters.MAX_PRIORITY,
    min_priority: int | None = task_filters.MIN_PRIORITY,
    due_date: str | None = task_filters.DUE_DATE,
    due_date_expression: str | None = task_filters.DUE_DATE_EXPRESSION,
    due_after: str | None = task_filters.DUE_AFTER,
    due_after_expression: str | None = task_filters.DUE_AFTER_EXPRESSION,
    due_before: str | None = task_filters.DUE_BEFORE,
    due_before_expression: str | None = task_filters.DUE_BEFORE_EXPRESSION,
    without_due_date: bool = task_filters.WITHOUT_DUE_DATE,
    follow_up_date: str | None = task_filters.FOLLOW_UP_DATE,
    follow_up_date_expression: str | None = task_filters.FOLLOW_UP_DATE_EXPRESSION,
    follow_up_after: str | None = task_filters.FOLLOW_UP_AFTER,
    follow_up_after_expression: str | None = task_filters.FOLLOW_UP_AFTER_EXPRESSION,
    follow_up_before: str | None = task_filters.FOLLOW_UP_BEFORE,
    follow_up_before_expression: str | None = task_filters.FOLLOW_UP_BEFORE_EXPRESSION,
    follow_up_before_or_not_existent: str | None = task_filters.FOLLOW_UP_BEFORE_OR_NOT_EXISTENT,
    follow_up_before_or_not_existent_expression: str | None = task_filters.FOLLOW_UP_BEFORE_OR_NOT_EXISTENT_EXPRESSION,
    created_on: str | None = task_filters.CREATED_ON,
    created_on_expression: str | None = task_filters.CREATED_ON_EXPRESSION,
    created_after: str | None = task_filters.CREATED_AFTER,
    created_after_expression: str | None = task_filters.CREATED_AFTER_EXPRESSION,
    created_before: str | None = task_filters.CREATED_BEFORE,
    created_before_expression: str | None = task_filters.CREATED_BEFORE_EXPRESSION,
    updated_after: str | None = task_filters.UPDATED_AFTER,
    updated_after_expression: str | None = task_filters.UPDATED_AFTER_EXPRESSION,
    delegation_state: str | None = task_filters.DELEGATION_STATE,
    candidate_groups: str | None = task_filters.CANDIDATE_GROUPS,
    candidate_groups_expression: str | None = task_filters.CANDIDATE_GROUPS_EXPRESSION,
    with_candidate_groups: bool = task_filters.WITH_CANDIDATE_GROUPS,
    without_candidate_groups: bool = task_filters.WITHOUT_CANDIDATE_GROUPS,
    with_candidate_users: bool = task_filters.WITH_CANDIDATE_USERS,
    without_candidate_users: bool = task_filters.WITHOUT_CANDIDATE_USERS,
    active: bool = task_filters.ACTIVE,
    suspended: bool = task_filters.SUSPENDED,
    task_variables: str | None = task_filters.TASK_VARIABLES,
    process_variables: str | None = task_filters.PROCESS_VARIABLES,
    case_instance_variables: str | None = task_filters.CASE_INSTANCE_VARIABLES,
    variable_names_ignore_case: bool = task_filters.VARIABLE_NAMES_IGNORE_CASE,
    variable_values_ignore_case: bool = task_filters.VARIABLE_VALUES_IGNORE_CASE,
    parent_task_id: str | None = task_filters.PARENT_TASK_ID,
    with_comment_attachment_info: bool = task_filters.WITH_COMMENT_ATTACHMENT_INFO,
    status: str | None = task_filters.STATUS,
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write the task count response to a JSON file.",
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
    """Count tasks with filters."""
    filters = task_filters.build_task_filters(locals())
    context = require_context(ctx)
    with context.build_engine() as engine:
        count = engine.tasks.count(params=filters)

    payload = {"count": count}
    if output:
        write_json(payload, output)

    if raw:
        print_raw_json(payload)
        return

    if format is OutputFormat.JSON:
        print_json(payload, title="Task Count")
        return

    print_summary(f"{count} task(s)")

