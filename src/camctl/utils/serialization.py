"""Serialization helpers for CLI-friendly JSON output."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from camctl.api.http import Resource


def dumps_json(payload: Any) -> str:
    """Serialize payload to pretty-printed JSON."""
    return json.dumps(_normalize(payload), indent=2, ensure_ascii=True)


def write_json(payload: Any, path: Path) -> None:
    """Write payload as JSON to the provided path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps_json(payload) + "\n", encoding="utf-8")


def _normalize(payload: Any) -> Any:
    """Normalize payloads into JSON-serializable structures."""
    if isinstance(payload, Resource):
        return _normalize(payload.to_dict())
    if is_dataclass(payload):
        return _normalize(asdict(payload))
    if isinstance(payload, dict):
        return {key: _normalize(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_normalize(item) for item in payload]
    if isinstance(payload, tuple):
        return [_normalize(item) for item in payload]
    return payload
