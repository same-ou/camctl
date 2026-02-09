"""Request payload models for task endpoints."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from camctl.api.camunda.common import (
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
