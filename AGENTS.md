# Agent Context

## Always Do
- Use `uv` for package management.
- Use Python 3.12+ idioms and strict type hinting.
- Use `pathlib.Path`.
- Use top-of-file imports.
- Rely on server-side rendering (FastAPI + Jinja2) and HTMX.

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
