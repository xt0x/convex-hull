.PHONY: help sync test ci lint format format-check typecheck

help:
	@printf '%s\n' \
		'Targets:' \
		'  sync       Sync project dependencies (locked)' \
		'  test       Run unit tests' \
		'  ci         Run the checks used in CI' \
		'  lint       Run lints (requires network to fetch tools)' \
		'  format     Format code (requires network to fetch tools)' \
		'  format-check  Check formatting without modifying files' \
		'  typecheck  Run static type checks (requires network to fetch tools)'

sync:
	uv sync --frozen --group ci --group dev

test:
	uv run pytest

ci:
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) typecheck
	@$(MAKE) test

# Tooling is intentionally fetched ad-hoc so we don't grow pyproject dev deps early.
lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

typecheck:
	uv run mypy --python-version 3.11 src
	
