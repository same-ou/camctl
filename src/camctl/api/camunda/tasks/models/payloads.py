"""Request payload models for task endpoints."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from camctl.api.camunda.models import (
    VariableModificationRequest,
    VariablePayload,
)

TaskVariablePayload = VariablePayload
TaskVariableModificationRequest = VariableModificationRequest


@dataclass(kw_only=True)
class TaskCompletionRequest:
    """Payload used to complete a task."""

    variables: Mapping[str, Any] = field(default_factory=dict)
    comment: str | None = None

    def to_payload(self) -> dict[str, Any]:
        """Serialize the request into a JSON-ready payload."""
        payload = dict(asdict(self))
        payload["variables"] = dict(self.variables)
        return payload
