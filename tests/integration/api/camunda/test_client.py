"""Integration tests for CamundaClient error handling and serialization."""

from __future__ import annotations

import json

import pytest

from camctl.api.camunda.errors import CamundaAPIError
from camctl.api.http.circuit_breaker import CircuitBreakerOpenError
from tests.integration.conftest import make_response


class TestRequestSerialization:
    def test_snake_case_params_to_camel(self, camunda_client):
        client, set_handler = camunda_client
        captured = {}

        def handler(request):
            captured["url"] = str(request.url)
            return make_response(200, json_body=[])

        set_handler(handler)
        client.get("task", params={"sort_by": "name", "max_results": 10})

        assert "sortBy=name" in captured["url"]
        assert "maxResults=10" in captured["url"]

    def test_snake_case_json_body_to_camel(self, camunda_client):
        client, set_handler = camunda_client
        captured = {}

        def handler(request):
            captured["body"] = json.loads(request.content)
            return make_response(200, json_body={})

        set_handler(handler)
        client.post("task/123/complete", json={"worker_id": "w1", "task_state": "done"})

        assert captured["body"] == {"workerId": "w1", "taskState": "done"}


class TestErrorHandling:
    def test_structured_error_body(self, camunda_client):
        client, set_handler = camunda_client
        set_handler(lambda req: make_response(
            400,
            json_body={"type": "RestException", "message": "Bad request", "code": 400},
        ))
        with pytest.raises(CamundaAPIError) as exc_info:
            client.get("task/123")
        assert exc_info.value.status_code == 400
        assert exc_info.value.error is not None
        assert exc_info.value.error.type == "RestException"
        assert exc_info.value.error.message == "Bad request"

    def test_error_without_structured_body(self, camunda_client):
        client, set_handler = camunda_client
        set_handler(lambda req: make_response(
            500,
            json_body={"error": "Internal Server Error"},
        ))
        with pytest.raises(CamundaAPIError) as exc_info:
            client.get("task/123")
        assert exc_info.value.status_code == 500
        assert exc_info.value.error is None
        assert exc_info.value.payload is not None

    def test_non_json_error_response(self, camunda_client):
        client, set_handler = camunda_client
        set_handler(lambda req: make_response(502, text="Bad Gateway"))
        with pytest.raises(CamundaAPIError) as exc_info:
            client.get("task/123")
        assert exc_info.value.status_code == 502
        assert exc_info.value.error is None
        assert exc_info.value.payload is None

    def test_allow_error_skips_raise(self, camunda_client):
        client, set_handler = camunda_client
        set_handler(lambda req: make_response(404, json_body={"type": "NotFound", "message": "Not found"}))
        response = client.get("task/123", allow_error=True)
        assert response.status_code == 404


class TestCircuitBreakerIntegration:
    def test_5xx_triggers_breaker(self, camunda_client):
        client, set_handler = camunda_client
        set_handler(lambda req: make_response(500, json_body={"error": "fail"}))

        for _ in range(5):
            with pytest.raises(CamundaAPIError):
                client.get("task")

        with pytest.raises(CircuitBreakerOpenError):
            client.get("task")

    def test_success_resets_breaker(self, camunda_client):
        client, set_handler = camunda_client
        # Record 4 failures (under threshold of 5)
        set_handler(lambda req: make_response(500, json_body={"error": "fail"}))
        for _ in range(4):
            with pytest.raises(CamundaAPIError):
                client.get("task")

        # Success resets counter
        set_handler(lambda req: make_response(200, json_body=[]))
        client.get("task")

        # 4 more failures should not open breaker
        set_handler(lambda req: make_response(500, json_body={"error": "fail"}))
        for _ in range(4):
            with pytest.raises(CamundaAPIError):
                client.get("task")

        # Should still work (not open)
        set_handler(lambda req: make_response(200, json_body=[]))
        client.get("task")
