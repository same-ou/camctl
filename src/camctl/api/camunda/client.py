"""Camunda HTTP client configured for engine REST endpoints."""

from __future__ import annotations

from typing import Mapping

import httpx

from camctl.api.http import BaseHTTPClient
from camctl.api.camunda.errors import CamundaAPIError, CamundaError

_BASE_URL = "http://localhost:8080/engine-rest"  



class CamundaClient(BaseHTTPClient):
    """Client for making authenticated requests against the Camunda REST API."""

    def __init__(
        self,
    ) -> None:
        
        super().__init__(
            base_url=_BASE_URL
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
