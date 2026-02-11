"""Response models for task resources."""

from __future__ import annotations

from dataclasses import dataclass

from camctl.api.camunda.common import CamundaResource, Resource, Variable, VariableValueInfo


@dataclass(kw_only=True)
class CamundaFormRef(Resource):
    """Represents a Camunda form reference for a task."""

    key: str | None = None
    binding: str | None = None
    version: int | None = None


TaskVariableValueInfo = VariableValueInfo
TaskVariable = Variable


@dataclass(kw_only=True)
class Task(CamundaResource):
    """Represents a task resource returned by the Camunda API."""

    name: str | None = None
    assignee: str | None = None
    created: str | None = None
    due: str | None = None
    follow_up: str | None = None
    last_updated: str | None = None
    delegation_state: str | None = None
    description: str | None = None
    execution_id: str | None = None
    owner: str | None = None
    parent_task_id: str | None = None
    priority: int | None = None
    process_definition_id: str | None = None
    process_instance_id: str | None = None
    case_definition_id: str | None = None
    case_execution_id: str | None = None
    task_definition_key: str | None = None
    form_key: str | None = None
    camunda_form_ref: CamundaFormRef | None = None
    task_state: str | None = None
    status: str | None = None


@dataclass(kw_only=True)
class TaskCompletionResult(Resource):
    """Represents the response from a task completion request."""

    task_id: str | None = None
    status: str | None = None
    message: str | None = None


@dataclass(kw_only=True)
class CountPerCandidateGroup(Resource):
    """Represents the response from a task count by candidate group request."""

    group_name: str | None = None
    task_count: int | None = None
