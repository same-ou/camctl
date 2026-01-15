"""Settings loading and environment interpolation for camctl."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


@dataclass(kw_only=True)
class Settings:
    """Application settings resolved from configuration sources."""

    authority: str = "uat"
    scopes: list[str] = field(default_factory=list)
    config_path: Path | None = None

    @classmethod
    def from_yaml(cls, path: Path | str) -> "Settings":
        """Load settings from a YAML file, resolving environment variables."""
        config_path = Path(path)
        data = config_path.read_text(encoding="utf-8")
        parsed = yaml.safe_load(data) or {}
        if not isinstance(parsed, Mapping):
            raise ValueError("Settings YAML must contain a mapping at the top level.")
        resolved = _resolve_env(parsed)
        settings = cls.from_mapping(resolved)
        settings.config_path = config_path
        return settings

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Settings":
        """Build settings from a mapping, supporting nested configuration keys."""
        source = data.get("auth") if isinstance(data.get("auth"), Mapping) else data
        authority = str(source.get("authority", "uat"))
        scopes = _normalize_scopes(source.get("scopes") or source.get("scope"))
        return cls(
            authority=authority,
            scopes=scopes,
        )


def _resolve_env(value: Any) -> Any:
    """Recursively resolve ${VAR} environment placeholders."""
    if isinstance(value, str):
        return _replace_env(value)
    if isinstance(value, Mapping):
        return {key: _resolve_env(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_resolve_env(item) for item in value]
    return value


def _replace_env(raw: str) -> str:
    """Replace ${VAR} tokens with environment values."""
    def _replace(match: re.Match[str]) -> str:
        var_name = match.group(1)
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable {var_name!r} is not set.")
        return value

    return _ENV_PATTERN.sub(_replace, raw)


def _normalize_scopes(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise TypeError("Scopes must be a string or list of strings.")
