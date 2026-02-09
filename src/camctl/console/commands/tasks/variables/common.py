"""Shared helpers for task variable commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from camctl.api.camunda.resources.tasks import TaskVariablePayload
from camctl.console.inputs import merge_mappings, parse_json_mapping


def parse_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def parse_value_info(
    value_info: str | None,
    value_info_file: Path | None,
) -> Mapping[str, Any] | None:
    if value_info is None and value_info_file is None:
        return None
    return parse_json_mapping(value_info, value_info_file)


def build_modifications(
    mapping: Mapping[str, Any],
) -> Mapping[str, TaskVariablePayload]:
    modifications: dict[str, TaskVariablePayload] = {}
    for name, payload in mapping.items():
        if not isinstance(payload, Mapping):
            raise ValueError(
                f"Modification for {name!r} must be an object with a value key."
            )
        if "value" not in payload:
            raise ValueError(
                f"Modification for {name!r} must include a value key."
            )
        value_info = payload.get("valueInfo") or payload.get("value_info")
        modifications[name] = TaskVariablePayload(
            value=payload["value"],
            type=payload.get("type"),
            value_info=value_info,
        )
    return modifications


def load_modifications(
    modifications: str | None,
    modifications_file: Path | None,
) -> Mapping[str, TaskVariablePayload] | None:
    file_mods = parse_json_mapping(None, modifications_file)
    raw_mods = parse_json_mapping(modifications, None)
    merged = merge_mappings(file_mods, raw_mods)
    if not merged:
        return None
    return build_modifications(merged)
