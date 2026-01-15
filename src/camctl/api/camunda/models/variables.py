"""Shared variable models for Camunda resources."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from camctl.api.http import Resource


def _snake_to_camel(value: str) -> str:
    parts = value.split("_")
    if not parts:
        return value
    head, *tail = parts
    return head + "".join(segment[:1].upper() + segment[1:] for segment in tail if segment)


def _value_info_payload(value_info: Any) -> dict[str, Any]:
    if isinstance(value_info, VariableValueInfo):
        data = asdict(value_info)
    elif isinstance(value_info, Mapping):
        data = dict(value_info)
    else:
        raise TypeError("value_info must be a mapping or VariableValueInfo.")
    return {
        _snake_to_camel(key): value
        for key, value in data.items()
        if value is not None
    }


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
class VariablePayload:
    """Payload used to create or update a Camunda variable."""

    value: Any
    type: str | None = None
    value_info: VariableValueInfo | Mapping[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        """Serialize the variable into a JSON-ready payload."""
        payload: dict[str, Any] = {"value": self.value}
        if self.type is not None:
            payload["type"] = self.type
        if self.value_info is not None:
            payload["valueInfo"] = _value_info_payload(self.value_info)
        return payload


@dataclass(kw_only=True)
class VariableModificationRequest:
    """Payload used to modify or delete Camunda variables."""

    modifications: Mapping[str, VariablePayload] | None = None
    deletions: Sequence[str] | None = None

    def to_payload(self) -> dict[str, Any]:
        """Serialize the request into a JSON-ready payload."""
        payload: dict[str, Any] = {}
        if self.modifications is not None:
            payload["modifications"] = {
                key: value.to_payload()
                for key, value in self.modifications.items()
            }
        if self.deletions is not None:
            payload["deletions"] = list(self.deletions)
        return payload


__all__ = [
    "Variable",
    "VariablePayload",
    "VariableModificationRequest",
    "VariableValueInfo",
]
