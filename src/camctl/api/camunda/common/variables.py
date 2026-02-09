"""Shared variable models for Camunda resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from camctl.api.camunda.common import Resource
from camctl.api.http.serialize import SerializeMixin, SnakeToCamelSerializer


@dataclass(kw_only=True)
class VariableValueInfo(Resource):
    """Metadata for serialized Camunda variable values."""

    object_type_name: str | None = None
    serialization_data_format: str | None = None
    filename: str | None = None
    mimetype: str | None = None
    encoding: str | None = None
    transient: bool | None = None


@dataclass(kw_only=True)
class Variable(Resource):
    """Represents a variable returned by the Camunda API."""

    value: Any = None
    type: str | None = None
    value_info: VariableValueInfo | None = None


@dataclass(kw_only=True)
class VariablePayload(SerializeMixin):
    """Payload used to create or update a Camunda variable."""

    value: Any
    type: str | None = None
    value_info: VariableValueInfo | Mapping[str, Any] | None = None

    def _serialize_field(self, name: str, value: Any) -> Any:
        if name == "value_info" and isinstance(value, Mapping):
            return SnakeToCamelSerializer().serialize(value)
        return super()._serialize_field(name, value)


@dataclass(kw_only=True)
class VariableModificationRequest(SerializeMixin):
    """Payload used to modify or delete Camunda variables."""

    modifications: Mapping[str, VariablePayload] | None = None
    deletions: Sequence[str] | None = None


__all__ = [
    "Variable",
    "VariablePayload",
    "VariableModificationRequest",
    "VariableValueInfo",
]
