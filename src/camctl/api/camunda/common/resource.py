"""Base resource models for Camunda API responses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import (
    Any,
    Mapping,
    MutableMapping,
    Self,
    get_args,
    get_origin,
    get_type_hints,
)
from uuid import UUID

from camctl.api.http.serialize import camel_to_snake


def _normalize_keys(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(key, str):
            normalized[camel_to_snake(key)] = value
        else:
            normalized[key] = value
    return normalized


def _resource_type(annotation: Any) -> type["Resource"] | None:
    if isinstance(annotation, type) and issubclass(annotation, Resource):
        return annotation
    origin = get_origin(annotation)
    if origin is None:
        return None
    for arg in get_args(annotation):
        if isinstance(arg, type) and issubclass(arg, Resource):
            return arg
    return None


@dataclass(kw_only=True)
class Resource:
    """Base class for Camunda API response mappings."""

    raw: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Build a resource from a JSON dictionary payload."""
        normalized = _normalize_keys(data)
        field_names = {f.name for f in fields(cls) if f.init and f.name != "raw"}
        filtered: MutableMapping[str, Any] = {
            key: value for key, value in normalized.items() if key in field_names
        }
        type_hints = get_type_hints(cls)
        for name, value in list(filtered.items()):
            resource_type = _resource_type(type_hints.get(name))
            if resource_type and isinstance(value, Mapping):
                filtered[name] = resource_type.from_dict(value)
        return cls(raw=normalized, **filtered)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready dictionary for the resource."""
        data = dict(self.raw)
        for field_def in fields(self):
            if field_def.name == "raw":
                continue
            value = getattr(self, field_def.name)
            if value is None:
                continue
            if isinstance(value, Resource):
                data[field_def.name] = value.to_dict()
            elif is_dataclass(value):
                data[field_def.name] = asdict(value)
            else:
                data[field_def.name] = value
        return data


@dataclass(kw_only=True)
class IdentifiableResource(Resource):
    """Resource identified by a unique ID."""

    id: UUID | str | None = None


@dataclass(kw_only=True)
class CamundaResource(IdentifiableResource):
    """Camunda engine entity with shared operational attributes."""

    tenant_id: str | None = None
    suspended: bool | None = None
    case_instance_id: str | None = None


__all__ = [
    "CamundaResource",
    "IdentifiableResource",
    "Resource",
]
