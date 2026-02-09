"""Task-focused endpoints for the Camunda API."""

from __future__ import annotations

from typing import Dict, List

from camctl.api.camunda.common import Page
from camctl.api.camunda.service import CamSubService

from .endpoints import TaskEndpoint
from .models import (
    Task,
    TaskCompletionRequest,
    TaskCompletionResult,
    TaskFilterParams,
    TaskListParams,
    CountPerCandidateGroup,
    TaskVariable,
    TaskVariableModificationRequest,
    TaskVariablePayload,
)


class TasksAPI(CamSubService):
    """Wrapper around task-related Camunda endpoints."""

    URL_PREFIX = ""

    def get(self, task_id: str) -> Task | None:
        """Fetch a single task by its identifier."""
        response = self._client.get(
            self._path(TaskEndpoint.DETAIL.value.format(task_id=task_id)),
            allow_error=True,
        )
        if response.status_code == 404:
            return None
        self._client._raise_for_status(response)
        return Task.from_dict(response.json())

    def list(self, *, params: TaskListParams | None = None) -> Page[Task]:
        """List tasks with optional query parameters."""
        response = self._client.get(
            self._path(TaskEndpoint.LIST.value),
            params=params,
        )
        payload = response.json()
        if isinstance(payload, list):
            items = [Task.from_dict(item) for item in payload if isinstance(item, dict)]
            return Page(raw={"items": payload}, items=items)
        if not isinstance(payload, dict):
            raise TypeError("Task list response must be a list or object.")
        return Page.from_dict(payload, item_parser=Task.from_dict)

    def count(self, *, params: TaskFilterParams | None = None) -> int:
        """Count tasks with optional query parameters."""
        response = self._client.get(
            self._path(TaskEndpoint.COUNT.value),
            params=params,
        )
        payload = response.json()
        if isinstance(payload, dict) and "count" in payload:
            return int(payload["count"])
        raise TypeError("Task count response must be an object with a count value.")
    
    def count_by_candidate_group(self) -> List[CountPerCandidateGroup]:
        """Count tasks grouped by candidate group."""
        response = self._client.get(
            self._path(TaskEndpoint.COUNT_BY_CANDIDATE_GROUP.value),
        )
        payload = response.json()
        if isinstance(payload, list):
            return [
                CountPerCandidateGroup.from_dict(item)
                for item in payload
                if isinstance(item, dict)
            ]
        raise TypeError("Task count by candidate group response must be a list.")

    def list_variables(
        self,
        task_id: str,
        *,
        deserialize_values: bool | None = None,
    ) -> Dict[str, TaskVariable]:
        """List global variables for a task."""
        params = {}
        if deserialize_values is not None:
            params["deserializeValues"] = deserialize_values
        response = self._client.get(
            self._path(TaskEndpoint.TASK_VARIABLES.value.format(task_id=task_id)),
            params=params or None,
        )
        payload = response.json()
        if isinstance(payload, dict):
            variables: Dict[str, TaskVariable] = {}
            for name, value in payload.items():
                if isinstance(value, dict):
                    variables[name] = TaskVariable.from_dict(value)
                else:
                    raise TypeError("Task variable payloads must be objects.")
            return variables
        raise TypeError("Task variables response must be an object.")

    def list_local_variables(
        self,
        task_id: str,
        *,
        deserialize_values: bool | None = None,
    ) -> Dict[str, TaskVariable]:
        """List local variables for a task."""
        params = {}
        if deserialize_values is not None:
            params["deserializeValues"] = deserialize_values
        response = self._client.get(
            self._path(TaskEndpoint.LOCAL_TASK_VARIABLES.value.format(task_id=task_id)),
            params=params or None,
        )
        payload = response.json()
        if isinstance(payload, dict):
            variables: Dict[str, TaskVariable] = {}
            for name, value in payload.items():
                if isinstance(value, dict):
                    variables[name] = TaskVariable.from_dict(value)
                else:
                    raise TypeError("Task variable payloads must be objects.")
            return variables
        raise TypeError("Task local variables response must be an object.")

    def modify_local_variables(
        self,
        task_id: str,
        *,
        payload: TaskVariableModificationRequest,
    ) -> None:
        """Update and/or delete local task variables in a single request."""
        self._client.post(
            self._path(
                TaskEndpoint.LOCAL_TASK_VARIABLES.value.format(task_id=task_id)
            ),
            json=payload,
        )

    def modify_variables(
        self,
        task_id: str,
        *,
        payload: TaskVariableModificationRequest,
    ) -> None:
        """Update and/or delete task variables in a single request."""
        self._client.post(
            self._path(TaskEndpoint.TASK_VARIABLES.value.format(task_id=task_id)),
            json=payload,
        )

    def get_variable(
        self,
        task_id: str,
        var_name: str,
        *,
        deserialize_values: bool | None = None,
    ) -> TaskVariable:
        """Fetch a single task variable by name."""
        params = {}
        if deserialize_values is not None:
            params["deserializeValues"] = deserialize_values
        response = self._client.get(
            self._path(
                TaskEndpoint.TASK_VARIABLE.value.format(task_id=task_id, var_name=var_name)
            ),
            params=params or None,
        )
        payload = response.json()
        if isinstance(payload, dict):
            return TaskVariable.from_dict(payload)
        raise TypeError("Task variable response must be an object.")

    def get_local_variable(
        self,
        task_id: str,
        var_name: str,
        *,
        deserialize_values: bool | None = None,
    ) -> TaskVariable:
        """Fetch a single local task variable by name."""
        params = {}
        if deserialize_values is not None:
            params["deserializeValues"] = deserialize_values
        response = self._client.get(
            self._path(
                TaskEndpoint.LOCAL_TASK_VARIABLE.value.format(
                    task_id=task_id, var_name=var_name
                )
            ),
            params=params or None,
        )
        payload = response.json()
        if isinstance(payload, dict):
            return TaskVariable.from_dict(payload)
        raise TypeError("Task local variable response must be an object.")

    def update_variable(
        self,
        task_id: str,
        var_name: str,
        *,
        payload: TaskVariablePayload,
    ) -> None:
        """Update a single task variable."""
        self._client.put(
            self._path(
                TaskEndpoint.TASK_VARIABLE.value.format(task_id=task_id, var_name=var_name)
            ),
            json=payload,
        )

    def update_local_variable(
        self,
        task_id: str,
        var_name: str,
        *,
        payload: TaskVariablePayload,
    ) -> None:
        """Update a single local task variable."""
        self._client.put(
            self._path(
                TaskEndpoint.LOCAL_TASK_VARIABLE.value.format(
                    task_id=task_id, var_name=var_name
                )
            ),
            json=payload,
        )

    def delete_variable(
        self,
        task_id: str,
        var_name: str,
    ) -> None:
        """Delete a single task variable."""
        self._client.delete(
            self._path(
                TaskEndpoint.TASK_VARIABLE.value.format(task_id=task_id, var_name=var_name)
            ),
        )

    def delete_local_variable(
        self,
        task_id: str,
        var_name: str,
    ) -> None:
        """Delete a single local task variable."""
        self._client.delete(
            self._path(
                TaskEndpoint.LOCAL_TASK_VARIABLE.value.format(
                    task_id=task_id, var_name=var_name
                )
            ),
        )

    def complete(
        self,
        task_id: str,
        *,
        payload: TaskCompletionRequest,
    ) -> TaskCompletionResult | None:
        """Complete a task using the supplied payload."""
        response = self._client.post(
            self._path(TaskEndpoint.COMPLETE.value.format(task_id=task_id)),
            json=payload,
            allow_error=True,
        )
        if response.status_code == 404:
            return None
        self._client._raise_for_status(response)
        if response.status_code == 204:
            return None
        return TaskCompletionResult.from_dict(response.json())
