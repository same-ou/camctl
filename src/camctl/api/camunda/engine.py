"""High-level entry point for Camunda services."""

from __future__ import annotations

from typing import Self

from camctl.api.camunda.client import CamundaClient
from camctl.api.camunda.processes import ProcessesAPI
from camctl.api.camunda.tasks import TasksAPI


class CamundaEngine:
    """Provide task and process APIs backed by a shared client."""

    def __init__(self, client: CamundaClient | None = None) -> None:
        self._client = client or CamundaClient()
        self.tasks = TasksAPI(self._client)
        self.processes = ProcessesAPI(self._client)

    @property
    def client(self) -> CamundaClient:
        """Return the underlying Camunda client."""
        return self._client

    def close(self) -> None:
        """Close the underlying client resources."""
        self._client.close()

    def __enter__(self) -> Self:
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._client.__exit__(exc_type, exc_val, exc_tb)


__all__ = ["CamundaEngine"]
