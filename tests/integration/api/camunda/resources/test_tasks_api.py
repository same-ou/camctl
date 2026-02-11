"""Integration tests for TasksAPI with mock HTTP transport."""

from __future__ import annotations

import pytest

from camctl.api.camunda.resources.tasks.api import TasksAPI
from camctl.api.camunda.resources.tasks.models import (
    TaskCompletionRequest,
    TaskListParams,
    TaskVariableModificationRequest,
    TaskVariablePayload,
)
from tests.integration.conftest import make_response


@pytest.fixture
def tasks_api(camunda_client):
    client, set_handler = camunda_client
    api = TasksAPI(client)
    return api, set_handler


class TestTasksGet:
    def test_success(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={
            "id": "task-1",
            "name": "Review",
            "assignee": "john",
            "processInstanceId": "proc-1",
        }))
        task = api.get("task-1")
        assert task is not None
        assert task.id == "task-1"
        assert task.name == "Review"
        assert task.assignee == "john"

    def test_not_found(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(404, json_body={
            "type": "RestException", "message": "Task not found",
        }))
        assert api.get("nonexistent") is None


class TestTasksList:
    def test_array_response(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body=[
            {"id": "t1", "name": "Task 1"},
            {"id": "t2", "name": "Task 2"},
        ]))
        page = api.list()
        assert len(page.items) == 2
        assert page.items[0].id == "t1"
        assert page.items[1].name == "Task 2"

    def test_object_response(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={
            "items": [{"id": "t1"}],
            "page": {"page": 1, "size": 10, "total": 1},
        }))
        page = api.list()
        assert len(page.items) == 1
        assert page.pagination is not None
        assert page.pagination.total == 1

    def test_with_params(self, tasks_api):
        api, set_handler = tasks_api
        captured = {}

        def handler(req):
            captured["url"] = str(req.url)
            return make_response(200, json_body=[])

        set_handler(handler)
        api.list(params=TaskListParams(assignee="john", max_results=5))
        assert "assignee=john" in captured["url"]
        assert "maxResults=5" in captured["url"]


class TestTasksCount:
    def test_returns_integer(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={"count": 42}))
        assert api.count() == 42


class TestTasksVariables:
    def test_list_variables(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={
            "var1": {"value": "hello", "type": "String"},
            "var2": {"value": 42, "type": "Integer"},
        }))
        variables = api.list_variables("task-1")
        assert "var1" in variables
        assert variables["var1"].value == "hello"
        assert variables["var2"].type == "Integer"

    def test_get_variable(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={
            "value": "world", "type": "String",
        }))
        var = api.get_variable("task-1", "myVar")
        assert var.value == "world"
        assert var.type == "String"


class TestTasksComplete:
    def test_success_with_body(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(200, json_body={
            "taskId": "task-1", "status": "completed",
        }))
        result = api.complete("task-1", payload=TaskCompletionRequest())
        assert result is not None
        assert result.task_id == "task-1"
        assert result.status == "completed"

    def test_no_content(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(204))
        result = api.complete("task-1", payload=TaskCompletionRequest())
        assert result is None

    def test_not_found(self, tasks_api):
        api, set_handler = tasks_api
        set_handler(lambda req: make_response(404, json_body={
            "type": "RestException", "message": "Not found",
        }))
        result = api.complete("task-1", payload=TaskCompletionRequest())
        assert result is None


class TestTasksModifyVariables:
    def test_modify_variables_sends_post(self, tasks_api):
        api, set_handler = tasks_api
        captured = {}

        def handler(req):
            captured["method"] = req.method
            captured["url"] = str(req.url)
            return make_response(204)

        set_handler(handler)
        payload = TaskVariableModificationRequest(
            modifications={"var1": TaskVariablePayload(value=42)},
            deletions=["var2"],
        )
        api.modify_variables("task-1", payload=payload)
        assert captured["method"] == "POST"
        assert "task-1/variables" in captured["url"]
