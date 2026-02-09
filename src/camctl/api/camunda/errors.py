"""Camunda API error models and exceptions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from camctl.api.camunda.common import Resource


@dataclass(kw_only=True)
class CamundaError(Resource):
    """Represents a formatted Camunda API error response."""

    type: str | None = None
    message: str | None = None
    code: int | None = None


class CamundaAPIError(RuntimeError):
    """Raised when the Camunda API returns an error payload."""

    def __init__(
        self,
        *,
        status_code: int,
        error: CamundaError | None = None,
        payload: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.error = error
        self.payload = payload
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if self.error and self.error.message:
            return f"Camunda API error {self.status_code}: {self.error.message}"
        return f"Camunda API error {self.status_code}"  # pragma: no cover
