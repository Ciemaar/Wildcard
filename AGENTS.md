# Agent Context

## Always Do

- Use `uv` for package management.
- Use Python 3.12+ idioms and strict type hinting.
- Use `pathlib.Path`.
- Use top-of-file imports.
- Rely on server-side rendering (FastAPI + Jinja2) and HTMX.
- When working on an existing, previous branch (e.g., rebasing or merging), features must not be removed if they've been added to the main branch in the intermediate interval. All branches being merged in, as well as their matching PRs, must be referenced in the commit comments and any new PRs.

## Never Do

- Send sensitive data to third-party LLM APIs.
- Use the `x or y` shortcut syntax for non-boolean results.
- Use `print()` for logging (use the `logging` module).
- Rely solely on implicit schema creation (use Alembic).

## Executable Commands

- Run tests: `uv run pytest` or `uv run tox`
- Run linting: `uv run ruff check`
- Run type checking: `uv run pyright`
- Build CSS: `./tailwindcss -i src/wms/static/input.css -o src/wms/static/output.css --minify`
