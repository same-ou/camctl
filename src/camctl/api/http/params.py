"""Base parameter helper for API requests."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

def _snake_to_camel(value: str) -> str:
    parts = value.split("_")
    if not parts:
        return value
    head, *tail = parts
    return head + "".join(segment[:1].upper() + segment[1:] for segment in tail if segment)


@dataclass
class Params:
    """Base class for request parameter objects."""

    def to_params(self) -> Mapping[str, Any]:
        """Return a dict of non-null fields with camelCased keys."""
        data = asdict(self)
        result: dict[str, Any] = {}
        for key, value in data.items():
            if value is None:
                continue
            result[_snake_to_camel(key)] = value
        return result


__all__ = ["Params"]
