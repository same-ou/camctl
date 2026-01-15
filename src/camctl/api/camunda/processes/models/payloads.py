"""Request payload models for process endpoints."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(kw_only=True)
class ProcessStartRequest:
    """Payload used to start a process instance."""

    variables: Mapping[str, Any] = field(default_factory=dict)
    business_key: str | None = None
    tenant_id: str | None = None

    def to_payload(self) -> dict[str, Any]:
        """Serialize the request into a JSON-ready payload."""
        payload = dict(asdict(self))
        payload["variables"] = dict(self.variables)
        return payload
