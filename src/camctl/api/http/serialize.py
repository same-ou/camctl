"""Helpers for serializing request data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import fields, is_dataclass
import re
from typing import Any, Mapping, Sequence


def _snake_to_camel(value: str) -> str:
    parts = value.split("_")
    if not parts:
        return value
    head, *tail = parts
    return head + "".join(segment[:1].upper() + segment[1:] for segment in tail if segment)


_CAMEL_RE_1 = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_RE_2 = re.compile(r"([a-z0-9])([A-Z])")


def _camel_to_snake(value: str) -> str:
    value = value.rstrip(":")
    value = value.replace("-", "_")
    step1 = _CAMEL_RE_1.sub(r"\1_\2", value)
    return _CAMEL_RE_2.sub(r"\1_\2", step1).lower()


def _serialize_mapping(value: Mapping[Any, Any]) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key, item in value.items():
        result[key] = _serialize_value(item)
    return result


def _serialize_dataclass(value: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    field_serializer = None
    if isinstance(value, SerializeMixin):
        field_serializer = value._serialize_field
    for field_def in fields(value):
        if not field_def.init:
            continue
        field_value = getattr(value, field_def.name)
        if field_value is None:
            continue
        if field_serializer is None:
            serialized = _serialize_value(field_value)
        else:
            serialized = field_serializer(field_def.name, field_value)
        result[_snake_to_camel(field_def.name)] = serialized
    return result


def _serialize_value(value: Any) -> Any:
    if isinstance(value, SerializeMixin):
        return value.to_api_dict()
    if is_dataclass(value):
        return _serialize_dataclass(value)
    if isinstance(value, Mapping):
        return _serialize_mapping(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_serialize_value(item) for item in value]
    return value


def _camelize_keys(value: Any) -> Any:
    if isinstance(value, Mapping):
        converted: dict[Any, Any] = {}
        for key, item in value.items():
            mapped_key = _snake_to_camel(key) if isinstance(key, str) else key
            converted[mapped_key] = _camelize_keys(item)
        return converted
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_camelize_keys(item) for item in value]
    return value


class SerializeMixin:
    """Mixin for request payload/parameter models."""

    def to_api_dict(self) -> dict[str, Any]:
        """Serialize the object into a camelCase, JSON-ready dictionary."""
        return _serialize_dataclass(self)

    def _serialize_field(self, name: str, value: Any) -> Any:
        return _serialize_value(value)


class Serializer(ABC):
    """Serialize request data for transport."""

    @abstractmethod
    def serialize(self, value: Any) -> Any:
        """Return a serialized representation of the value."""
        raise NotImplementedError


class SnakeToCamelSerializer(Serializer):
    """Serialize request data with snake_case keys converted to camelCase."""

    def serialize(self, value: Any) -> Any:
        if value is None:
            return None
        serialized = _serialize_value(value)
        return _camelize_keys(serialized)


__all__ = [
    "SerializeMixin",
    "Serializer",
    "SnakeToCamelSerializer",
]
