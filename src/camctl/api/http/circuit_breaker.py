"""Circuit breaker support for outbound HTTP calls."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic


class CircuitBreakerOpenError(RuntimeError):
    """Raised when a request is blocked by an open circuit breaker."""

    def __init__(self, retry_after_seconds: float) -> None:
        super().__init__(
            f"Circuit breaker is open. Retry after {retry_after_seconds:.2f}s."
        )
        self.retry_after_seconds = retry_after_seconds


@dataclass
class CircuitBreaker:
    """
    Basic circuit breaker with `closed`, `open`, and `half-open` states.

    The breaker opens after `failure_threshold` consecutive failures. After
    `recovery_timeout_seconds`, one trial request is permitted in half-open.
    """

    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be >= 1")
        if self.recovery_timeout_seconds <= 0:
            raise ValueError("recovery_timeout_seconds must be > 0")
        self._failure_count = 0
        self._state = "closed"
        self._opened_at = 0.0

    @property
    def state(self) -> str:
        return self._state

    def before_request(self) -> None:
        """Check whether a request is allowed and update state if needed."""
        if self._state != "open":
            return
        now = monotonic()
        elapsed = now - self._opened_at
        if elapsed >= self.recovery_timeout_seconds:
            self._state = "half-open"
            return
        raise CircuitBreakerOpenError(self.recovery_timeout_seconds - elapsed)

    def record_success(self) -> None:
        """Record a successful call and close/reset the breaker."""
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self) -> None:
        """Record a failed call and open/keep-open the breaker if needed."""
        if self._state == "half-open":
            self._open()
            return
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold:
            self._open()

    def _open(self) -> None:
        self._state = "open"
        self._opened_at = monotonic()


__all__ = [
    "CircuitBreaker",
    "CircuitBreakerOpenError",
]
