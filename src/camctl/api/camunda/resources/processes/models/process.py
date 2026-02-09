"""Response models for process resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from camctl.api.camunda.common import Resource


@dataclass(kw_only=True)
class ProcessInstance(Resource):
    """Represents a process instance resource returned by the Camunda API."""

    links: list[Mapping[str, Any]] | None = None
    id: str | None = None
    definition_id: str | None = None
    definition_key: str | None = None
    business_key: str | None = None
    case_instance_id: str | None = None
    ended: bool | None = None
    suspended: bool | None = None
    tenant_id: str | None = None


@dataclass(kw_only=True)
class ProcessStartResult(Resource):
    """Represents the response from a process start request."""

    process_instance_id: str | None = None
    status: str | None = None
    message: str | None = None


@dataclass(kw_only=True)
class ProcessCancelResult(Resource):
    """Represents the response from a process cancel request."""

    process_id: str | None = None
    status: str | None = None
    message: str | None = None
