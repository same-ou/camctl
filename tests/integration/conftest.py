"""Integration test fixtures with mock HTTP transport."""

from __future__ import annotations

import json
from typing import Any, Callable

import httpx
import pytest

from camctl.api.camunda.client import CamundaClient


def make_response(
    status_code: int = 200,
    json_body: Any = None,
    text: str = "",
) -> httpx.Response:
    """Build an httpx.Response for mock transport handlers."""
    if json_body is not None:
        content = json.dumps(json_body).encode()
        headers = {"content-type": "application/json"}
    else:
        content = text.encode()
        headers = {"content-type": "text/plain"}
    return httpx.Response(
        status_code=status_code,
        content=content,
        headers=headers,
    )


@pytest.fixture
def mock_transport():
    """Create a mock transport with a configurable handler.

    Returns a tuple of (transport, handler_setter). Call handler_setter
    with a callable(request) -> response to configure responses.
    """
    handler_ref: list[Callable] = [lambda req: make_response(200)]

    def _handler(request: httpx.Request) -> httpx.Response:
        return handler_ref[0](request)

    transport = httpx.MockTransport(_handler)

    def set_handler(fn: Callable[[httpx.Request], httpx.Response]):
        handler_ref[0] = fn

    return transport, set_handler


@pytest.fixture
def camunda_client(mock_transport):
    """CamundaClient backed by mock transport."""
    transport, set_handler = mock_transport
    client = httpx.Client(transport=transport)
    camunda = CamundaClient.__new__(CamundaClient)
    # Manually initialize to inject our mock client
    from camctl.api.http.circuit_breaker import CircuitBreaker
    from camctl.api.http.serialize import SnakeToCamelSerializer

    camunda.base_url = "http://localhost:8080/engine-rest/"
    camunda.timeout = 10.0
    camunda._serializer = SnakeToCamelSerializer()
    camunda._circuit_breaker = CircuitBreaker()
    camunda._owns_client = True
    camunda._client = client
    camunda._default_headers = {}
    return camunda, set_handler
