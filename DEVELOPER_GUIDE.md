# Developer Guide

## Architecture

- **Backend:** FastAPI, HTMX, Jinja2. This application prefers server-side rendering over a complex SPA JavaScript framework.
- **Database:** SQLite via SQLAlchemy with Alembic migrations. `JSONB` columns are strictly utilized for unstructured data when using Postgres.
- **PDF Generation:** WeasyPrint.
- **Styling:** Tailwind CSS.

## Local Setup

1. **Python Environment:** Ensure Python 3.12+ is installed.
1. **Package Management:** We strictly use `uv` for package management. To sync dependencies, run:
   ```bash
   uv sync
   ```
1. **Database Setup:**
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

## API Router Architecture

The application is structured into domain-specific Fast API routers mounted in `src/wms/main.py`.

- **`dashboard.py`**: Manages all CRUD operations for the `Mission` models and renders the `dashboard.html` view.
- **`print_studio.py`**: Handles batch generation logic, joining approved missions together, and serving the WeasyPrint PDF generation logic from `pdf_layout.html`.

## Vercel Deployment

This project is configured to be deployed on Vercel using the `@vercel/python` builder. Vercel is a cloud platform for static and serverless deployments.

**Important Note on Databases:** Vercel Serverless Functions have a read-only filesystem. If you do not provision an external database, the application will default to an in-memory SQLite database (`sqlite+aiosqlite:///:memory:`) in Vercel to prevent a startup crash, meaning your data will not persist. **You must provision a Vercel Postgres database via the Vercel Dashboard and link it to your project to populate the `DATABASE_URL` environment variable for production data persistence.**

### Local Tooling & Deployment

1. Ensure the `vercel` optional dependency group is installed in your python environment: `uv sync --extra vercel`
1. Install the Vercel CLI via npm: `npm i -g vercel`
1. Link the project: `vercel link`
1. Pull the environment variables (this should include the `DATABASE_URL` from Vercel Postgres): `vercel env pull .env`
1. Deploy the project: `vercel --prod`

### Tool Evaluation Required

Whenever a new third-party integration or deployment strategy like Vercel is proposed, developers must first evaluate the tooling. If a major platform constraint or new dependency system is introduced (e.g., dynamically building `requirements.txt` via `vercel-build.sh` because Vercel requires it over `pyproject.toml`), a tool evaluation must be documented in `docs/tooling_evaluation.md`.
