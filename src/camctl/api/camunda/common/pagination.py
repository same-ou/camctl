"""Pagination and sorting models for paged API responses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import (
    Any,
    Callable,
    Generic,
    Mapping,
    Sequence,
    TypeVar,
)

from camctl.api.camunda.common.resource import Resource

T = TypeVar("T", bound=Resource)


@dataclass(kw_only=True)
class SortInfo(Resource):
    """Sorting metadata for paged responses."""

    field: str | None = None
    direction: str | None = None


@dataclass(kw_only=True)
class PaginationInfo(Resource):
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
            sort = SortInfo.from_dict(sort_data)
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
        return base


__all__ = [
    "Page",
    "PaginationInfo",
    "SortInfo",
]
