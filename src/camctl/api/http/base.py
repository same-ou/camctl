"""Core HTTP client abstractions backed by httpx."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from http import HTTPMethod
from typing import Any, Mapping, MutableMapping, Optional, Self
from urllib.parse import urljoin

import httpx

from camctl.api.http.circuit_breaker import CircuitBreaker
from camctl.api.http.serialize import Serializer, SnakeToCamelSerializer

logger = logging.getLogger(__name__)

class HTTPClient(ABC):
    """
    Abstract HTTP client definition.

    Subclasses implement the low-level `request` method. Convenience helpers
    (`get`, `post`, etc.) delegate to that method with an HTTPMethod enum so
    callers remain consistent about HTTP verb usage.
    """

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 10.0,
        serializer: Serializer,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self._serializer: Serializer = serializer

    @abstractmethod
    def request(
        self,
        method: HTTPMethod,
        path: str,
        *,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Execute an HTTP request using the configured transport."""

    def get(
        self,
        path: str,
        *,
        params: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP GET request."""
        return self.request(
            HTTPMethod.GET,
            path,
            params=params,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            allow_error=allow_error,
        )

    def post(
        self,
        path: str,
        *,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP POST request."""
        return self.request(
            HTTPMethod.POST,
            path,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            files=files,
            allow_error=allow_error,
        )

    def put(
        self,
        path: str,
        *,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP PUT request."""
        return self.request(
            HTTPMethod.PUT,
            path,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            files=files,
            allow_error=allow_error,
        )

    def patch(
        self,
        path: str,
        *,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP PATCH request."""
        return self.request(
            HTTPMethod.PATCH,
            path,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            files=files,
            allow_error=allow_error,
        )

    def delete(
        self,
        path: str,
        *,
        params: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP DELETE request."""
        return self.request(
            HTTPMethod.DELETE,
            path,
            params=params,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            allow_error=allow_error,
        )

    def head(
        self,
        path: str,
        *,
        params: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP HEAD request."""
        return self.request(
            HTTPMethod.HEAD,
            path,
            params=params,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            allow_error=allow_error,
        )

    def options(
        self,
        path: str,
        *,
        params: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """Issue an HTTP OPTIONS request."""
        return self.request(
            HTTPMethod.OPTIONS,
            path,
            params=params,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            allow_error=allow_error,
        )

    @abstractmethod
    def close(self) -> None:
        """Dispose of any held resources (sessions, sockets, etc.)."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class BaseHTTPClient(HTTPClient):
    """
    HTTP client implementation for unauthenticated or basic-auth requests.

    The client wraps an httpx.Client and composes request URLs, headers, and
    timeouts so API-specific clients can focus on endpoint behavior.
    """

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 10.0,
        default_headers: Optional[Mapping[str, str]] = None,
        basic_auth: Optional[tuple[str, str]] = None,
        client: Optional[httpx.Client] = None,
        serializer: Serializer | None = None,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        resolved_serializer = serializer or SnakeToCamelSerializer()
        super().__init__(base_url, timeout=timeout, serializer=resolved_serializer)
        self._circuit_breaker = circuit_breaker
        self._owns_client = client is None
        if client is None:
            auth = httpx.BasicAuth(*basic_auth) if basic_auth else None
            self._client = httpx.Client(timeout=timeout, auth=auth)
            self._default_headers: MutableMapping[str, str] = dict(default_headers or {})
        else:
            self._client = client
            self._default_headers = dict(client.headers)
            if default_headers:
                self._default_headers.update(default_headers)

    @property
    def session(self) -> httpx.Client:
        """Return the underlying httpx client instance."""
        return self._client

    def _build_url(self, path: str) -> str:
        """Return an absolute URL for the provided path."""
        return urljoin(self.base_url, path.lstrip("/"))

    def _build_request_headers(
        self,
        headers: Optional[Mapping[str, str]],
    ) -> Mapping[str, str]:
        """Compose merged headers for a single request."""
        merged: MutableMapping[str, str] = dict(self._default_headers)
        if headers:
            merged.update(headers)
        return merged

    def request(
        self,
        method: HTTPMethod,
        path: str,
        *,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        cookies: Optional[Mapping[str, str]] = None,
        files: Optional[Any] = None,
        allow_error: bool = False,
    ) -> httpx.Response:
        """
        Execute an HTTP request using the configured client.

        Args:
            method: HTTP verb from the HTTPMethod enum.
            path: Relative API path appended to `base_url`.
            params: Query string parameters.
            data: Form data payload.
            json: JSON payload.
            headers: Additional request headers.
            timeout: Optional per-request timeout override.
            cookies: Optional cookies to send with the request.
            files: Optional multipart files payload.
            allow_error: When True, do not raise for non-2xx responses.

        Returns:
            The httpx.Response returned by the server.
        """
        url = self._build_url(path)
        request_headers = self._build_request_headers(headers)
        if self._circuit_breaker is not None:
            self._circuit_breaker.before_request()
        logger.debug("HTTP %s %s", method.value, url)
        try:
            response = self._client.request(
                method.value,
                url,
                params=self._serializer.serialize(params),
                data=self._serializer.serialize(data),
                json=self._serializer.serialize(json),
                headers=request_headers,
                timeout=timeout if timeout is not None else self.timeout,
                files=files,
            )
        except httpx.HTTPError:
            if self._circuit_breaker is not None:
                self._circuit_breaker.record_failure()
            raise

        if self._circuit_breaker is not None:
            if response.status_code >= 500:
                self._circuit_breaker.record_failure()
            else:
                self._circuit_breaker.record_success()
        if not allow_error:
            self._raise_for_status(response)
        return response

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise an exception for an error response."""
        response.raise_for_status()

    def set_default_header(self, name: str, value: str) -> None:
        """Persist a default header that is sent with every request."""
        self._default_headers[name] = value

    def remove_default_header(self, name: str) -> None:
        """Remove a previously defined default header."""
        self._default_headers.pop(name, None)

    def update_default_headers(self, headers: Mapping[str, str]) -> None:
        """Merge headers into the default header collection."""
        self._default_headers.update(headers)

    def close(self) -> None:
        """Dispose of the underlying httpx client."""
        if self._owns_client:
            self._client.close()
