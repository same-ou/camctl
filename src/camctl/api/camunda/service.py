"""Base service helpers for API clients."""

from __future__ import annotations

from camctl.api.http.service import SubService
from camctl.api.camunda.client import CamundaClient


class CamSubService(SubService[CamundaClient]):
    """Base class for API sub-services using a shared HTTP client."""

    def __init__(self, client: CamundaClient) -> None:
        super().__init__(client=client)



__all__ = ["CamSubService"]
