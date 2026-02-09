"""Camunda HTTP client configured for engine REST endpoints."""

from __future__ import annotations

from typing import Mapping

import httpx

from camctl.api.http import BaseHTTPClient, CircuitBreaker
from camctl.api.http.serialize import SnakeToCamelSerializer
from camctl.api.camunda.errors import CamundaAPIError, CamundaError

_BASE_URL = "http://localhost:8080/engine-rest"
_DEFAULT_TIMEOUT_SECONDS = 10.0
_DEFAULT_BREAKER_FAILURE_THRESHOLD = 5
_DEFAULT_BREAKER_RECOVERY_TIMEOUT_SECONDS = 30.0

class CamundaClient(BaseHTTPClient):
    """Client for making authenticated requests against the Camunda REST API."""

    def __init__(
        self,
        *,
        base_url: str = _BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT_SECONDS,
        circuit_breaker: CircuitBreaker | None = None,
        failure_threshold: int = _DEFAULT_BREAKER_FAILURE_THRESHOLD,
        recovery_timeout_seconds: float = _DEFAULT_BREAKER_RECOVERY_TIMEOUT_SECONDS,
    ) -> None:
        resolved_breaker = circuit_breaker or CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout_seconds=recovery_timeout_seconds,
        )
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            serializer=SnakeToCamelSerializer(),
            circuit_breaker=resolved_breaker,
        )

    def _raise_for_status(self, response: httpx.Response) -> None:
        if not response.is_error:
            return
        payload: Mapping[str, object] | None = None
        error: CamundaError | None = None
        try:
            parsed = response.json()
        except ValueError:
            parsed = None
        if isinstance(parsed, Mapping):
            payload = parsed
            if {"type", "message"}.issubset(parsed.keys()):
                error = CamundaError.from_dict(parsed)
        raise CamundaAPIError(
            status_code=response.status_code,
            error=error,
            payload=payload,
        )
