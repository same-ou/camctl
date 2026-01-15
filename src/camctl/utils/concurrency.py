"""Concurrency helpers for running blocking tasks in parallel."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def gather(
    func: Callable[[T], R],
    items: Iterable[T],
    *,
    max_workers: int = 8,
    return_exceptions: bool = False,
    on_start: Callable[[T], None] | None = None,
    on_complete: Callable[[T, R | Exception], None] | None = None,
) -> list[R | Exception]:
    """
    Run a function for each item concurrently, similar to asyncio.gather.

    Args:
        func: Callable applied to each item.
        items: Input items to process.
        max_workers: Maximum number of worker threads.
        return_exceptions: When True, capture exceptions in the results list.

    Returns:
        Results in the same order as the input items.
    """
    item_list = list(items)
    if not item_list:
        return []

    results: list[R | Exception] = [None for _ in item_list]  # type: ignore[list-item]

    def _run(item: T) -> R:
        if on_start:
            on_start(item)
        try:
            result = func(item)
        except Exception as exc:
            if on_complete:
                on_complete(item, exc)
            raise
        if on_complete:
            on_complete(item, result)
        return result
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(_run, item): index for index, item in enumerate(item_list)
        }
        for future in as_completed(future_map):
            index = future_map[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                if return_exceptions:
                    results[index] = exc
                else:
                    raise
    return results
