"""Request payload models for process endpoints."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(kw_only=True)
class ProcessStartRequest:
    """Payload used to start a process instance."""

    variables: Mapping[str, Any] = field(default_factory=dict)
    business_key: str | None = None
    tenant_id: str | None = None
