"""Tests for the circuit breaker state machine."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from camctl.api.http.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError


class TestCircuitBreakerInit:
    def test_starts_closed(self):
        cb = CircuitBreaker()
        assert cb.state == "closed"

    def test_invalid_failure_threshold(self):
        with pytest.raises(ValueError, match="failure_threshold must be >= 1"):
            CircuitBreaker(failure_threshold=0)

    def test_invalid_recovery_timeout(self):
        with pytest.raises(ValueError, match="recovery_timeout_seconds must be > 0"):
            CircuitBreaker(recovery_timeout_seconds=0)

    def test_negative_recovery_timeout(self):
        with pytest.raises(ValueError, match="recovery_timeout_seconds must be > 0"):
            CircuitBreaker(recovery_timeout_seconds=-1)


class TestCircuitBreakerClosed:
    def test_stays_closed_under_threshold(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "closed"

    def test_before_request_allowed_when_closed(self):
        cb = CircuitBreaker()
        cb.before_request()  # should not raise

    def test_success_resets_failure_count(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        cb.record_success()
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "closed"


class TestCircuitBreakerOpen:
    def test_opens_at_threshold(self):
        cb = CircuitBreaker(failure_threshold=3)
        for _ in range(3):
            cb.record_failure()
        assert cb.state == "open"

    def test_blocks_requests_when_open(self):
        cb = CircuitBreaker(failure_threshold=1)
        cb.record_failure()
        assert cb.state == "open"
        with pytest.raises(CircuitBreakerOpenError):
            cb.before_request()

    def test_error_contains_retry_seconds(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=30.0)
        cb.record_failure()
        with pytest.raises(CircuitBreakerOpenError) as exc_info:
            cb.before_request()
        assert exc_info.value.retry_after_seconds > 0


class TestCircuitBreakerHalfOpen:
    def test_transitions_to_half_open_after_timeout(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=0.01)
        cb.record_failure()
        assert cb.state == "open"
        # Simulate time passing
        with patch("camctl.api.http.circuit_breaker.monotonic") as mock_time:
            mock_time.return_value = cb._opened_at + 1.0
            cb.before_request()
        assert cb.state == "half-open"

    def test_half_open_success_closes(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=0.01)
        cb.record_failure()
        with patch("camctl.api.http.circuit_breaker.monotonic") as mock_time:
            mock_time.return_value = cb._opened_at + 1.0
            cb.before_request()
        assert cb.state == "half-open"
        cb.record_success()
        assert cb.state == "closed"

    def test_half_open_failure_reopens(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=0.01)
        cb.record_failure()
        with patch("camctl.api.http.circuit_breaker.monotonic") as mock_time:
            mock_time.return_value = cb._opened_at + 1.0
            cb.before_request()
        assert cb.state == "half-open"
        cb.record_failure()
        assert cb.state == "open"


class TestCircuitBreakerOpenError:
    def test_message_format(self):
        err = CircuitBreakerOpenError(retry_after_seconds=15.5)
        assert "15.50" in str(err)
        assert err.retry_after_seconds == 15.5
