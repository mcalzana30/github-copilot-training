# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Project

A small RESTful API built with Python and FastAPI, used as a GitHub Copilot training project. It tracks developer tasks and generates productivity reports.

- **Primary Language:** Python 3.12
- **Framework:** FastAPI with Uvicorn
- **Dependency Manager:** uv (configured via `pyproject.toml`)
- **Data Models:** Pydantic models in `app/models.py`

## Commands

```bash
uv sync                                                              # install dependencies
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000  # dev server
pytest tests/ -v                                                     # run all tests
pytest tests/path/to/test_file.py::test_function_name -v            # run a single test
uv run mypy app --strict                                             # type checking
```

## Architecture

`app/main.py` is the single entry point. It holds the FastAPI app, an in-memory mock database (`MOCK_TASKS` dict), async service functions (`fetch_all_tasks`, `generate_productivity_report`), and all route handlers.

`app/models.py` centralizes all Pydantic models: `TaskStatus` enum, `DeveloperTask`, `ProductivityReport`, and `TaskCompletionMetrics`. All new models must go here.

Routes:

- `GET /status` — health check
- `GET /tasks` — list all tasks
- `GET /report` — calculated productivity report
- `POST /log_task` — add a new task

## Testing Structure

Tests live in `tests/`, organized as `tests/unit/` and `tests/integration/`. Integration tests are marked with `@pytest.mark.integration`. Use `httpx.AsyncClient` for endpoint tests and place shared fixtures (app client, auth tokens) in `tests/conftest.py`. Target 85%+ coverage.

## Mandatory Coding Standards

1. All route handlers and I/O-bound functions must use `async def` with `await`.
2. All function signatures must have explicit type hints on parameters and return values.
3. Every new endpoint or utility function requires a corresponding pytest test using `httpx.AsyncClient`.
4. All Pydantic models must be placed in `app/models.py`.
5. API endpoints must return dicts, lists, or Pydantic models — not raw strings or f-strings.

## Agents

`.github/agents/MyPyFixer.md` defines a specialist agent for resolving mypy type errors. It runs `uv run mypy -- app`, fixes errors iteratively without using `# type: ignore`, and commits with the `fix(types):` prefix.
