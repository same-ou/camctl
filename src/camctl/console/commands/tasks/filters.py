"""Shared filter options for task queries."""

from __future__ import annotations

from dataclasses import fields
from typing import Any, Mapping, get_args

import typer

from camctl.api.camunda.tasks import TaskFilterParams


def _is_optional_bool(annotation: Any) -> bool:
    if annotation is bool:
        return True
    return bool in get_args(annotation)


_FILTER_FIELDS = [field.name for field in fields(TaskFilterParams)]
_BOOL_FIELDS = {
    name
    for name, annotation in TaskFilterParams.__annotations__.items()
    if _is_optional_bool(annotation)
}


TASK_ID = typer.Option(None, "--task-id", help="Task id filter.")

TASK_ID_IN = typer.Option(
    None,
    "--task-id-in",
    help="Comma-separated task ids to include.",
    )

PROCESS_INSTANCE_ID = typer.Option(
    None, "--process-instance-id", help="Process instance filter."
    )

PROCESS_INSTANCE_ID_IN = typer.Option(
    None,
    "--process-instance-id-in",
    help="Comma-separated process instance ids.",
    )

PROCESS_INSTANCE_BUSINESS_KEY = typer.Option(
    None,
    "--process-instance-business-key",
    help="Process instance business key filter.",
    )

PROCESS_INSTANCE_BUSINESS_KEY_EXPRESSION = typer.Option(
    None,
    "--process-instance-business-key-expression",
    help="Business key expression filter.",
    )

PROCESS_INSTANCE_BUSINESS_KEY_IN = typer.Option(
    None,
    "--process-instance-business-key-in",
    help="Comma-separated process instance business keys.",
    )

PROCESS_INSTANCE_BUSINESS_KEY_LIKE = typer.Option(
    None,
    "--process-instance-business-key-like",
    help="Business key substring filter.",
    )

PROCESS_INSTANCE_BUSINESS_KEY_LIKE_EXPRESSION = typer.Option(
    None,
    "--process-instance-business-key-like-expression",
    help="Business key substring expression filter.",
    )

PROCESS_DEFINITION_ID = typer.Option(
    None, "--process-definition-id", help="Process definition filter."
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

PROCESS_DEFINITION_NAME = typer.Option(
    None,
    "--process-definition-name",
    help="Process definition name filter.",
    )

PROCESS_DEFINITION_NAME_LIKE = typer.Option(
    None,
    "--process-definition-name-like",
    help="Process definition name substring filter.",
    )

EXECUTION_ID = typer.Option(
    None, "--execution-id", help="Execution id filter."
    )

CASE_INSTANCE_ID = typer.Option(
    None, "--case-instance-id", help="Case instance id filter."
    )

CASE_INSTANCE_BUSINESS_KEY = typer.Option(
    None,
    "--case-instance-business-key",
    help="Case instance business key filter.",
    )

CASE_INSTANCE_BUSINESS_KEY_LIKE = typer.Option(
    None,
    "--case-instance-business-key-like",
    help="Case instance business key substring filter.",
    )

CASE_DEFINITION_ID = typer.Option(
    None, "--case-definition-id", help="Case definition id filter."
    )

CASE_DEFINITION_KEY = typer.Option(
    None, "--case-definition-key", help="Case definition key filter."
    )

CASE_DEFINITION_NAME = typer.Option(
    None, "--case-definition-name", help="Case definition name filter."
    )

CASE_DEFINITION_NAME_LIKE = typer.Option(
    None,
    "--case-definition-name-like",
    help="Case definition name substring filter.",
    )

CASE_EXECUTION_ID = typer.Option(
    None, "--case-execution-id", help="Case execution id filter."
    )

ACTIVITY_INSTANCE_ID_IN = typer.Option(
    None,
    "--activity-instance-id-in",
    help="Comma-separated activity instance ids.",
    )

TENANT_ID_IN = typer.Option(
    None,
    "--tenant-id-in",
    help="Comma-separated tenant ids.",
    )

WITHOUT_TENANT_ID = typer.Option(
    False,
    "--without-tenant-id",
    help="Only include tasks with no tenant.",
    )

ASSIGNEE = typer.Option(None, "--assignee", help="Assignee filter.")

ASSIGNEE_EXPRESSION = typer.Option(
    None,
    "--assignee-expression",
    help="Assignee expression filter.",
    )

ASSIGNEE_LIKE = typer.Option(
    None, "--assignee-like", help="Assignee substring filter."
    )

ASSIGNEE_LIKE_EXPRESSION = typer.Option(
    None,
    "--assignee-like-expression",
    help="Assignee substring expression filter.",
    )

ASSIGNEE_IN = typer.Option(
    None,
    "--assignee-in",
    help="Comma-separated assignee ids.",
    )

ASSIGNEE_NOT_IN = typer.Option(
    None,
    "--assignee-not-in",
    help="Comma-separated assignee ids to exclude.",
    )

OWNER = typer.Option(None, "--owner", help="Owner filter.")

OWNER_EXPRESSION = typer.Option(
    None,
    "--owner-expression",
    help="Owner expression filter.",
    )

CANDIDATE_GROUP = typer.Option(
    None,
    "--candidate-group",
    help="Candidate group filter.",
    )

CANDIDATE_GROUP_LIKE = typer.Option(
    None,
    "--candidate-group-like",
    help="Candidate group substring filter.",
    )

CANDIDATE_GROUP_EXPRESSION = typer.Option(
    None,
    "--candidate-group-expression",
    help="Candidate group expression filter.",
    )

CANDIDATE_USER = typer.Option(
    None,
    "--candidate-user",
    help="Candidate user filter.",
    )

CANDIDATE_USER_EXPRESSION = typer.Option(
    None,
    "--candidate-user-expression",
    help="Candidate user expression filter.",
    )

INCLUDE_ASSIGNED_TASKS = typer.Option(
    False,
    "--include-assigned-tasks",
    help="Also include tasks that are assigned in candidate queries.",
    )

INVOLVED_USER = typer.Option(
    None,
    "--involved-user",
    help="Involved user filter.",
    )

INVOLVED_USER_EXPRESSION = typer.Option(
    None,
    "--involved-user-expression",
    help="Involved user expression filter.",
    )

ASSIGNED = typer.Option(False, "--assigned", help="Only include assigned tasks.")

UNASSIGNED = typer.Option(
    False, "--unassigned", help="Only include unassigned tasks."
    )

TASK_DEFINITION_KEY = typer.Option(
    None,
    "--task-definition-key",
    help="Task definition key filter.",
    )

TASK_DEFINITION_KEY_IN = typer.Option(
    None,
    "--task-definition-key-in",
    help="Comma-separated task definition keys.",
    )

TASK_DEFINITION_KEY_LIKE = typer.Option(
    None,
    "--task-definition-key-like",
    help="Task definition key substring filter.",
    )

NAME = typer.Option(None, "--name", help="Task name filter.")

NAME_NOT_EQUAL = typer.Option(
    None,
    "--name-not-equal",
    help="Exclude tasks with the given name.",
    )

NAME_LIKE = typer.Option(
    None,
    "--name-like",
    help="Task name substring filter.",
    )

NAME_NOT_LIKE = typer.Option(
    None,
    "--name-not-like",
    help="Exclude tasks with a matching name substring.",
    )

DESCRIPTION = typer.Option(
    None,
    "--description",
    help="Task description filter.",
    )

DESCRIPTION_LIKE = typer.Option(
    None,
    "--description-like",
    help="Task description substring filter.",
    )

PRIORITY = typer.Option(
    None,
    "--priority",
    help="Priority filter.",
    )

MAX_PRIORITY = typer.Option(
    None,
    "--max-priority",
    help="Maximum priority filter.",
    )

MIN_PRIORITY = typer.Option(
    None,
    "--min-priority",
    help="Minimum priority filter.",
    )

DUE_DATE = typer.Option(
    None,
    "--due-date",
    help="Due date filter.",
    )

DUE_DATE_EXPRESSION = typer.Option(
    None,
    "--due-date-expression",
    help="Due date expression filter.",
    )

DUE_AFTER = typer.Option(
    None,
    "--due-after",
    help="Due after date filter.",
    )

DUE_AFTER_EXPRESSION = typer.Option(
    None,
    "--due-after-expression",
    help="Due after date expression filter.",
    )

DUE_BEFORE = typer.Option(
    None,
    "--due-before",
    help="Due before date filter.",
    )

DUE_BEFORE_EXPRESSION = typer.Option(
    None,
    "--due-before-expression",
    help="Due before date expression filter.",
    )

WITHOUT_DUE_DATE = typer.Option(
    False,
    "--without-due-date",
    help="Only include tasks without a due date.",
    )

FOLLOW_UP_DATE = typer.Option(
    None,
    "--follow-up-date",
    help="Follow-up date filter.",
    )

FOLLOW_UP_DATE_EXPRESSION = typer.Option(
    None,
    "--follow-up-date-expression",
    help="Follow-up date expression filter.",
    )

FOLLOW_UP_AFTER = typer.Option(
    None,
    "--follow-up-after",
    help="Follow-up after date filter.",
    )

FOLLOW_UP_AFTER_EXPRESSION = typer.Option(
    None,
    "--follow-up-after-expression",
    help="Follow-up after date expression filter.",
    )

FOLLOW_UP_BEFORE = typer.Option(
    None,
    "--follow-up-before",
    help="Follow-up before date filter.",
    )

FOLLOW_UP_BEFORE_EXPRESSION = typer.Option(
    None,
    "--follow-up-before-expression",
    help="Follow-up before date expression filter.",
    )

FOLLOW_UP_BEFORE_OR_NOT_EXISTENT = typer.Option(
    None,
    "--follow-up-before-or-not-existent",
    help="Follow-up before date or not existent filter.",
    )

FOLLOW_UP_BEFORE_OR_NOT_EXISTENT_EXPRESSION = typer.Option(
    None,
    "--follow-up-before-or-not-existent-expression",
    help="Follow-up before date or not existent expression filter.",
    )

CREATED_ON = typer.Option(
    None,
    "--created-on",
    help="Created on date filter.",
    )

CREATED_ON_EXPRESSION = typer.Option(
    None,
    "--created-on-expression",
    help="Created on date expression filter.",
    )

CREATED_AFTER = typer.Option(
    None,
    "--created-after",
    help="Created after date filter.",
    )

CREATED_AFTER_EXPRESSION = typer.Option(
    None,
    "--created-after-expression",
    help="Created after date expression filter.",
    )

CREATED_BEFORE = typer.Option(
    None,
    "--created-before",
    help="Created before date filter.",
    )

CREATED_BEFORE_EXPRESSION = typer.Option(
    None,
    "--created-before-expression",
    help="Created before date expression filter.",
    )

UPDATED_AFTER = typer.Option(
    None,
    "--updated-after",
    help="Updated after date filter.",
    )

UPDATED_AFTER_EXPRESSION = typer.Option(
    None,
    "--updated-after-expression",
    help="Updated after date expression filter.",
    )

DELEGATION_STATE = typer.Option(
    None,
    "--delegation-state",
    help="Delegation state filter.",
    )

CANDIDATE_GROUPS = typer.Option(
    None,
    "--candidate-groups",
    help="Comma-separated candidate groups.",
    )

CANDIDATE_GROUPS_EXPRESSION = typer.Option(
    None,
    "--candidate-groups-expression",
    help="Candidate groups expression filter.",
    )

WITH_CANDIDATE_GROUPS = typer.Option(
    False,
    "--with-candidate-groups",
    help="Only include tasks with candidate groups.",
    )

WITHOUT_CANDIDATE_GROUPS = typer.Option(
    False,
    "--without-candidate-groups",
    help="Only include tasks without candidate groups.",
    )

WITH_CANDIDATE_USERS = typer.Option(
    False,
    "--with-candidate-users",
    help="Only include tasks with candidate users.",
    )

WITHOUT_CANDIDATE_USERS = typer.Option(
    False,
    "--without-candidate-users",
    help="Only include tasks without candidate users.",
    )

ACTIVE = typer.Option(False, "--active", help="Only include active tasks.")

SUSPENDED = typer.Option(
    False, "--suspended", help="Only include suspended tasks."
    )

TASK_VARIABLES = typer.Option(
    None,
    "--task-variables",
    help="Task variable filters.",
    )

PROCESS_VARIABLES = typer.Option(
    None,
    "--process-variables",
    help="Process variable filters.",
    )

CASE_INSTANCE_VARIABLES = typer.Option(
    None,
    "--case-instance-variables",
    help="Case instance variable filters.",
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

PARENT_TASK_ID = typer.Option(
    None,
    "--parent-task-id",
    help="Parent task id filter.",
    )

WITH_COMMENT_ATTACHMENT_INFO = typer.Option(
    False,
    "--with-comment-attachment-info",
    help="Include comment and attachment info.",
    )

STATUS = typer.Option(None, "--status", help="Status filter.")


def build_task_filter_kwargs(values: Mapping[str, Any]) -> dict[str, Any]:
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


def build_task_filters(values: Mapping[str, Any]) -> TaskFilterParams:
    return TaskFilterParams(**build_task_filter_kwargs(values))

