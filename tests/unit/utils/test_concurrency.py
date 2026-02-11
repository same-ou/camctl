"""Tests for the gather concurrency helper."""

from __future__ import annotations

import pytest

from camctl.utils.concurrency import gather


class TestGather:
    def test_ordered_results(self):
        results = gather(lambda x: x * 2, [1, 2, 3, 4, 5])
        assert results == [2, 4, 6, 8, 10]

    def test_empty_input(self):
        assert gather(lambda x: x, []) == []

    def test_exception_propagation(self):
        def fail(x):
            if x == 3:
                raise ValueError("boom")
            return x

        with pytest.raises(ValueError, match="boom"):
            gather(fail, [1, 2, 3, 4])

    def test_return_exceptions(self):
        def fail(x):
            if x == 2:
                raise ValueError("boom")
            return x * 10

        results = gather(fail, [1, 2, 3], return_exceptions=True)
        assert results[0] == 10
        assert isinstance(results[1], ValueError)
        assert results[2] == 30

    def test_on_start_callback(self):
        started = []
        gather(lambda x: x, [1, 2, 3], on_start=lambda x: started.append(x))
        assert sorted(started) == [1, 2, 3]

    def test_on_complete_callback(self):
        completed = []
        gather(
            lambda x: x * 2,
            [1, 2],
            on_complete=lambda item, result: completed.append((item, result)),
        )
        completed.sort()
        assert completed == [(1, 2), (2, 4)]

    def test_on_complete_with_exception(self):
        completed = []

        def fail(x):
            raise ValueError("err")

        gather(
            fail,
            [1],
            return_exceptions=True,
            on_complete=lambda item, result: completed.append(
                (item, type(result).__name__)
            ),
        )
        assert completed == [(1, "ValueError")]

    def test_preserves_order_with_varying_work(self):
        import time

        def slow_func(x):
            time.sleep(0.01 * (5 - x))
            return x

        results = gather(slow_func, [1, 2, 3, 4, 5], max_workers=5)
        assert results == [1, 2, 3, 4, 5]
