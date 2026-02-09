"""Shared Camunda resource and pagination models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    MutableMapping,
    Sequence,
    TypeVar,
    Self,
    get_args,
    get_origin,
    get_type_hints,
)

from camctl.api.http.serialize import _camel_to_snake

T = TypeVar("T", bound="Resource")


def _normalize_keys(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(key, str):
            normalized[_camel_to_snake(key)] = value
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
class SortInfo:
    """Sorting metadata for paged responses."""

    field: str | None = None
    direction: str | None = None


@dataclass(kw_only=True)
class PaginationInfo:
    """Pagination metadata for paged responses."""

    page: int | None = None
    size: int | None = None
    total: int | None = None
    total_pages: int | None = None
    has_next: bool | None = None
    has_previous: bool | None = None


@dataclass(kw_only=True)
class Page(Resource, Generic[T]):
    """Generic paged response container."""

    items: Sequence[T] = field(default_factory=tuple)
    pagination: PaginationInfo | None = None
    sort: SortInfo | None = None

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any],
        *,
        item_parser: Callable[[Mapping[str, Any]], T],
    ) -> "Page[T]":
        """Build a Page from a JSON payload and item parser."""
        raw_items = data.get("items") or data.get("data") or []
        items: list[T] = []
        for item in raw_items:
            if isinstance(item, Resource):
                items.append(item)
            elif isinstance(item, Mapping):
                items.append(item_parser(item))
            else:
                raise TypeError("Page items must be mappings or Resource instances.")

        pagination_data = data.get("page") or data.get("pagination") or {}
        pagination = None
        if isinstance(pagination_data, Mapping) and pagination_data:
            pagination = PaginationInfo.from_dict(pagination_data)

        sort_data = data.get("sort") or data.get("sorting") or {}
        sort: SortInfo | None = None
        if isinstance(sort_data, Mapping) and sort_data:
            sort = SortInfo(**{k: v for k, v in sort_data.items() if k in {"field", "direction"}})
        elif isinstance(sort_data, SortInfo):
            sort = sort_data

        return cls(raw=dict(data), items=items, pagination=pagination, sort=sort)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready dictionary for the page."""
        base = super().to_dict()
        base["items"] = [
            item.to_dict() if isinstance(item, Resource) else asdict(item)
            for item in self.items
        ]
        if self.pagination:
            base["pagination"] = self.pagination.to_dict()
        if self.sort:
            base["sort"] = asdict(self.sort)
        return base


__all__ = [
    "Page",
    "PaginationInfo",
    "Resource",
    "SortInfo",
]
