"""Tests for CamundaError and CamundaAPIError."""

from __future__ import annotations

from camctl.api.camunda.errors import CamundaAPIError, CamundaError


class TestCamundaError:
    def test_from_dict(self):
        e = CamundaError.from_dict({
            "type": "RestException",
            "message": "Task not found",
            "code": 404,
        })
        assert e.type == "RestException"
        assert e.message == "Task not found"
        assert e.code == 404

    def test_from_dict_partial(self):
        e = CamundaError.from_dict({"type": "Error", "message": "Oops"})
        assert e.type == "Error"
        assert e.message == "Oops"
        assert e.code is None


class TestCamundaAPIError:
    def test_message_with_error(self):
        error = CamundaError(type="RestException", message="Not found")
        exc = CamundaAPIError(status_code=404, error=error)
        assert str(exc) == "Camunda API error 404: Not found"
        assert exc.status_code == 404
        assert exc.error is error

    def test_message_without_error(self):
        exc = CamundaAPIError(status_code=500)
        assert str(exc) == "Camunda API error 500"
        assert exc.error is None
        assert exc.payload is None

    def test_payload_preserved(self):
        payload = {"type": "Error", "message": "Bad"}
        exc = CamundaAPIError(status_code=400, payload=payload)
        assert exc.payload is payload

    def test_is_runtime_error(self):
        exc = CamundaAPIError(status_code=500)
        assert isinstance(exc, RuntimeError)
