# Developer Guide

## Architecture
- **Backend:** FastAPI, HTMX, Jinja2. This application prefers server-side rendering over a complex SPA JavaScript framework.
- **Database:** SQLite via SQLAlchemy with Alembic migrations. `JSONB` columns are strictly utilized for unstructured data when using Postgres.
- **PDF Generation:** WeasyPrint.
- **Styling:** Tailwind CSS.

## Local Setup
1. **Python Environment:** Ensure Python 3.12+ is installed.
2. **Package Management:** We strictly use `uv` for package management. To sync dependencies, run:
   ```bash
   uv sync
   ```
3. **Database Setup:** 
   The database uses SQLite and migrations are handled by Alembic. 
   Apply the migrations before starting the app:
   ```bash
   PYTHONPATH=src uv run alembic upgrade head
   ```

## Development Commands
- **Testing:** Run tests via `uv run pytest` or `uv run tox`. Isolated unit tests use `unittest.mock`, integration tests require ephemeral databases via Docker.
- **Formatting and Linting:** Run `uv run ruff format` and `uv run ruff check`. All warnings must be resolved.
- **Type Checking:** Strict type checking with `pyright` is universally enforced. Run `uv run pyright`.

## Tooling & Constraints
- Always use `pathlib.Path`.
- Top-of-file imports are enforced.
- Do not use `print()` for log information; always use the `logging` module.
- Never use the `x or y` shortcut syntax for non-boolean results.
- `pyproject.toml` is the single source of truth for all configurations except for tox (`tox.ini`).

### Tailwind CSS Setup
Tailwind CSS is used to build the stylesheet. Since we want to avoid Node.js dependencies where possible, we use the standalone Tailwind CLI executable.

The CLI is included or can be downloaded as `./tailwindcss`.

To compile the CSS during development, run:
```bash
./tailwindcss -i src/wms/static/input.css -o src/wms/static/output.css --watch
```

For production build (minified):
```bash
./tailwindcss -i src/wms/static/input.css -o src/wms/static/output.css --minify
```
*Note: Do not check `src/wms/static/output.css` into version control. Build it before testing/deployment.*

## Contributing
- All environment variables should be defined in `src/wms/config.py` using `pydantic-settings`.
- When proposing new tools, evaluate them in `docs/tooling_evaluation.md` first.
