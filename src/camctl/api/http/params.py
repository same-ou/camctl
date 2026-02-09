"""Base parameter helper for API requests."""

from __future__ import annotations

from dataclasses import dataclass

from camctl.api.http.serialize import SerializeMixin


@dataclass
class Params(SerializeMixin):
    """Base class for request parameter objects."""


__all__ = ["Params"]
