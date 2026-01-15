"""Base service helpers for API clients."""

from __future__ import annotations

from typing import Generic, TypeVar

from camctl.api.http import HTTPClient

ClientT = TypeVar("ClientT", bound=HTTPClient)


class SubService(Generic[ClientT]):
    """Base class for API sub-services using a shared HTTP client."""

    URL_PREFIX: str = ""

    def __init__(self, client: ClientT) -> None:
        self._client: ClientT = client

    def _path(self, suffix: str) -> str:
        """Build a path under the service prefix."""
        if suffix.startswith("/"):
            suffix = suffix[1:]
        if self.URL_PREFIX.endswith("/"):
            return f"{self.URL_PREFIX}{suffix}"
        if self.URL_PREFIX:
            return f"{self.URL_PREFIX}/{suffix}"
        return suffix


__all__ = ["SubService"]
