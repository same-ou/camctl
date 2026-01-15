SHELL := /bin/sh

PYTHON ?= python
UV := $(shell command -v uv 2>/dev/null)

ifeq ($(UV),)
PYTHON_RUN := $(PYTHON)
SYNC := $(PYTHON) -m pip install -e .
else
PYTHON_RUN := uv run python
SYNC := uv sync
endif

APP := camctl

.DEFAULT_GOAL := help

.PHONY: help sync install run test lint format typecheck check clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

sync: ## Install dependencies using uv (or pip if uv is not available)
	$(SYNC)

install: sync ## Alias for sync

run: ## Run the CLI (use ARGS="..." to pass arguments)
	$(PYTHON_RUN) -m $(APP) $(ARGS)

_test_deps:
	@$(PYTHON_RUN) -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('pytest') else 1)" || \
		{ echo "pytest not installed. Install with: uv add --dev pytest"; exit 1; }

test: _test_deps ## Run tests with pytest
	$(PYTHON_RUN) -m pytest -q

_lint_deps:
	@$(PYTHON_RUN) -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('ruff') else 1)" || \
		{ echo "ruff not installed. Install with: uv add --dev ruff"; exit 1; }

lint: _lint_deps ## Run Ruff lints
	$(PYTHON_RUN) -m ruff check .

format: _lint_deps ## Run Ruff formatter
	$(PYTHON_RUN) -m ruff format .

_typecheck_deps:
	@$(PYTHON_RUN) -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('mypy') else 1)" || \
		{ echo "mypy not installed. Install with: uv add --dev mypy"; exit 1; }

typecheck: _typecheck_deps ## Run mypy type checks
	$(PYTHON_RUN) -m mypy src

check: lint test ## Run lint and tests

clean: ## Remove cache files and build artifacts
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	@find . -type d -name '.ruff_cache' -prune -exec rm -rf {} +
	@find . -type d -name '.mypy_cache' -prune -exec rm -rf {} +
	@find . -type d -name 'build' -prune -exec rm -rf {} +
	@find . -type d -name 'dist' -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
