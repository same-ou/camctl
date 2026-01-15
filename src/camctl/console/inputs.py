"""Input parsing helpers for CLI commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def parse_json_mapping(raw: str | None, path: Path | None) -> Mapping[str, Any]:
    """Parse a JSON mapping from a string or file."""
    if path:
        content = path.read_text(encoding="utf-8")
        return _load_mapping(content)
    if raw:
        return _load_mapping(raw)
    return {}


def parse_key_value_pairs(pairs: Sequence[str]) -> Mapping[str, Any]:
    """Parse key=value pairs into a mapping, coercing JSON values when possible."""
    values: dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid pair {pair!r}; expected key=value.")
        key, raw_value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("Variable name cannot be empty.")
        values[key] = _coerce_value(raw_value.strip())
    return values


def merge_mappings(*mappings: Mapping[str, Any]) -> Mapping[str, Any]:
    """Merge multiple mappings into one, later values overriding earlier ones."""
    merged: dict[str, Any] = {}
    for mapping in mappings:
        merged.update(mapping)
    return merged


def parse_comma_list(values: Sequence[str] | None) -> list[str] | None:
    """Parse comma-separated list options, preserving order."""
    if not values:
        return None
    items: list[str] = []
    seen: set[str] = set()
    for raw in values:
        for entry in raw.split(","):
            entry = entry.strip()
            if not entry or entry in seen:
                continue
            items.append(entry)
            seen.add(entry)
    return items or None


def _load_mapping(raw: str) -> Mapping[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON payload.") from exc
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object.")
    return payload


def _coerce_value(raw: str) -> Any:
    if raw == "":
        return ""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw
