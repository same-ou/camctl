# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**camctl** is a CLI for managing Camunda workflow engine processes and tasks. It wraps the Camunda REST API with a Typer-based CLI, Rich terminal output, and an httpx-backed HTTP client with circuit breaker support.

Python 3.11+ required. Uses `uv` for dependency management.

## Common Commands

```bash
make sync              # Install/sync dependencies (uv preferred, pip fallback)
make test              # Run pytest (install first: uv add --dev pytest)
make lint              # Ruff linting
make format            # Ruff formatting
make typecheck         # mypy type checking
make check             # lint + test
make run ARGS="--help" # Run the CLI
```

Single test: `uv run python -m pytest tests/path/to/test.py::test_name -q`

The CLI entry point is `camctl.console.app:app`. Can also run via `python -m camctl`.

## Architecture

### Layered HTTP Client

```
HTTPClient (abstract, api/http/base.py)
  → BaseHTTPClient (httpx-backed, adds circuit breaker + serialization)
    → CamundaClient (api/camunda/client.py, adds Camunda error handling)
```

All request payloads pass through a `SnakeToCamelSerializer` (api/http/serialize.py) which converts snake_case Python fields to camelCase for the Camunda API. Responses are deserialized in reverse via `Resource.from_dict()`.

### Service Pattern

```
SubService[ClientT] (api/http/service.py, generic base)
  → CamSubService (api/camunda/service.py, binds to CamundaClient)
    → TasksAPI (api/camunda/resources/tasks/api.py)
    → ProcessesAPI (api/camunda/resources/processes/api.py)
```

Each resource API lives under `api/camunda/resources/<resource>/` with its own `api.py`, `endpoints.py` (enum of URL paths), and `models/` directory.

### Resource Models

All API response dataclasses inherit from `Resource` (api/camunda/common/models.py):
- `Resource.from_dict(data)` — auto-converts camelCase keys to snake_case, stores original payload in `raw`
- `Resource.to_dict()` — serializes back to JSON-ready dict
- `Page[T]` — generic paginated response container with `PaginationInfo` and `SortInfo`

Shared models (variables, pagination) live in `api/camunda/common/`.

### CLI Structure (Typer)

`CamctlApp` (console/app.py) is the root Typer app with two command groups:
- `tasks_app` — list, get, complete, count + nested `variables` (with `local` subgroup)
- `processes_app` — list, get, cancel, count + variables

Commands use `CLIContext` (console/context.py) via `typer.Context.obj` for shared state (authority, scopes). Call `ctx.obj.build_engine()` to get a `CamundaEngine` instance.

Filter parameters for list commands are defined in dedicated `filters.py` modules. Display output uses Rich tables/panels via helpers in `console/display.py`. The `console/inputs.py` module handles parsing user input (JSON strings, key=value pairs).

### Serialization Convention

Python models use `snake_case`. The Camunda REST API uses `camelCase`. Conversion happens automatically:
- **Outbound** (requests): `SnakeToCamelSerializer` in the HTTP client layer
- **Inbound** (responses): `_camel_to_snake` via `Resource.from_dict()`

### Environment

- `CAMCTL_AUTHORITY` env var sets the target authority (default: `uat`)
