"""Integration tests for ProcessesAPI with mock HTTP transport."""

from __future__ import annotations

import pytest

from camctl.api.camunda.resources.processes.api import ProcessesAPI
from tests.integration.conftest import make_response


@pytest.fixture
def processes_api(camunda_client):
    client, set_handler = camunda_client
    api = ProcessesAPI(client)
    return api, set_handler


class TestProcessesGet:
    def test_success(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body={
            "id": "proc-1",
            "definitionId": "def-1",
            "definitionKey": "invoiceProcess",
            "businessKey": "INV-001",
            "ended": False,
            "suspended": False,
        }))
        proc = api.get("proc-1")
        assert proc is not None
        assert proc.id == "proc-1"
        assert proc.definition_key == "invoiceProcess"
        assert proc.business_key == "INV-001"

    def test_not_found(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(404, json_body={
            "type": "RestException", "message": "Not found",
        }))
        assert api.get("nonexistent") is None


class TestProcessesList:
    def test_array_response(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body=[
            {"id": "p1", "definitionKey": "proc1"},
            {"id": "p2", "definitionKey": "proc2"},
        ]))
        page = api.list()
        assert len(page.items) == 2
        assert page.items[0].id == "p1"
        assert page.items[1].definition_key == "proc2"

    def test_object_response(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body={
            "items": [{"id": "p1"}],
            "page": {"page": 1, "size": 10, "total": 1},
        }))
        page = api.list()
        assert len(page.items) == 1
        assert page.pagination is not None
        assert page.pagination.total == 1


class TestProcessesCount:
    def test_returns_integer(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body={"count": 15}))
        assert api.count() == 15


class TestProcessesVariables:
    def test_success(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body={
            "amount": {"value": 100.0, "type": "Double"},
            "approved": {"value": True, "type": "Boolean"},
        }))
        variables = api.variables("proc-1")
        assert variables is not None
        assert "amount" in variables
        assert variables["amount"].value == 100.0
        assert variables["approved"].type == "Boolean"

    def test_not_found(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(404, json_body={
            "type": "RestException", "message": "Not found",
        }))
        assert api.variables("nonexistent") is None


class TestProcessesCancel:
    def test_success_with_body(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(200, json_body={
            "processId": "proc-1", "status": "cancelled",
        }))
        result = api.cancel("proc-1")
        assert result is not None
        assert result.process_id == "proc-1"
        assert result.status == "cancelled"

    def test_no_content(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(204))
        result = api.cancel("proc-1")
        assert result is None

    def test_not_found(self, processes_api):
        api, set_handler = processes_api
        set_handler(lambda req: make_response(404, json_body={
            "type": "RestException", "message": "Not found",
        }))
        result = api.cancel("nonexistent")
        assert result is None
