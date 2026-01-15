"""Parsing helpers for batch identifier inputs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def parse_id_list(raw: str) -> list[str]:
    """Parse a comma or newline separated list of IDs from a string."""
    cleaned = raw.strip()
    if not cleaned:
        return []
    if cleaned.startswith("["):
        data = _parse_json_list(cleaned)
        return _normalize_ids(data)
    parts = re.split(r"[,\n\r]+", cleaned)
    return [part.strip() for part in parts if part.strip()]


def load_id_file(path: Path) -> list[str]:
    """Load IDs from a file containing JSON or delimiter-separated values."""
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []
    if content.startswith("["):
        data = _parse_json_list(content)
        return _normalize_ids(data)
    return parse_id_list(content)


def _parse_json_list(raw: str) -> list[Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON list provided for process IDs.") from exc
    if not isinstance(data, list):
        raise ValueError("JSON input must be a list of process IDs.")
    return data


def _normalize_ids(items: list[Any]) -> list[str]:
    normalized: list[str] = []
    for item in items:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            normalized.append(text)
    return normalized
