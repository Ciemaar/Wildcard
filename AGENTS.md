# Agent Context

## Project Context
- **Wildcard Management System (WMS)**: A FastAPI, HTMX, Tailwind application that manages photography game missions. It uses SQLite for local development and PostgreSQL for Vercel deployments, and generates print-ready PDFs using WeasyPrint.
- **Licensing**: The project is strictly proprietary and uses an 'All Rights Reserved' license to ensure the creator retains full control of the intellectual property. Do not apply open-source licenses or assume the code can be freely distributed.

## Framework & Architecture
- **Framework Choice**: Prefer FastAPI paired with HTMX and server-side rendered Jinja2 templates for UI web apps. Avoid complex JavaScript SPA frameworks.
- **Project Layout**: Always use a strict `src`-based directory layout.
- **Vercel Deployment Architecture**: Route the FastAPI application through an `api/index.py` entrypoint. Use `vercel.json` rewrites to serve static files from Vercel's CDN (`/static/` to `/src/wms/static/`) and forward other requests to the API.

## Package Management & Dependencies
- **Package Management**: Exclusively use `uv` for managing dependencies and environments; `pip`, `poetry`, and `pipenv` are prohibited. Ensure `uv.lock` is checked in.
- **Dependency Management (Vercel)**: Keep core dependencies clean by placing Vercel-specific packages (e.g., Postgres drivers) in `[project.optional-dependencies]` under the `vercel` key. Do not commit `requirements.txt` or `install_uv.sh`. Dynamically generate the requirements list via a build script (e.g., `vercel-build.sh`) running `uv pip compile pyproject.toml --extra vercel -o requirements.txt`, and configure `vercel.json` with an `installCommand` to execute this script and install the packages.
- **Dependency Security**: Use `uv audit` to check for vulnerability issues in project dependencies. Enforce this via a local pre-commit hook in `.pre-commit-config.yaml` (`pass_filenames: false`) and a dedicated GitHub Actions CI workflow (e.g., `.github/workflows/audit.yml`).

## Configuration & Documentation
- **Configuration**: Use `pyproject.toml` as the single source of truth for tooling. Universally use `pydantic-settings` for application environment variables and configurations.
- **Documentation Requirements**: Projects must include `README.md`, `SOURCES.md`, `USER_GUIDE.md`, `DEVELOPER_GUIDE.md`, `RUNBOOK.md`, and `AGENTS.md`. Keep agent session documentation in `prompts/`, `plans/`, and `reports/`.

## Code Standards
- **Python Standards**: Use modern Python (3.12+) with built-in type hints (e.g., `list[str]`, `str | None`), strictly enforce top-of-file imports, and avoid `typing.Any`.
- **Standard Libraries**: Always use `pathlib.Path` instead of `os.path`, the `logging` module instead of `print()`, and `yaml.safe_load` for serialization instead of `pickle`.
- **Code Logic Constraints**: Never use the `x or y` shortcut syntax for non-boolean results. Always use explicit ternary operations like `x if x is not None else y`.
- **Linting & Formatting**: Use `ruff` for Python code, `mdformat` for Markdown, and enforce Ruff's `pydocstyle (D)` ruleset for docstrings.
- **Type Checking**: Standardize on `pyright` in strict mode as the universal default.
- **Seed Data**: Seed data should be stored in external YAML files (e.g., `seed_data.yaml`) and loaded dynamically rather than being hardcoded as data structures directly in Python code.

## Database & Persistence
- **Database URLs**: Session setup must support dynamic protocol mapping to the respective async drivers (e.g., adapting `postgres://` or `postgresql://` to `postgresql+asyncpg://`, and `sqlite:///` to `sqlite+aiosqlite:///`).
- **Database Migrations**: Use automated migrations (e.g., Alembic) for relational databases like SQLAlchemy. Never rely on implicit creation like `Base.metadata.create_all()` in production.

## Testing Standards
- **Runners & CI**: Use `tox`, `pytest`, and `hypothesis` as universal test runners. Require `pre-commit` hooks and GitHub Actions (`.github/workflows/ci.yml`) for CI, ensuring workflows are split into multiple parallel jobs (e.g., separate `lint` and `test` jobs) and set `env: FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` to avoid Node 20 deprecation warnings.
- **Unit & Integration Tests**: Use `unittest.mock` for unit tests and ephemeral Docker databases (or in-memory SQLite) for integration tests.
- **SQLite Testing**: For SQLite testing, use an in-memory database (`sqlite+aiosqlite:///:memory:`) configured with `sqlalchemy.pool.StaticPool` and `connect_args={"check_same_thread": False}` in `conftest.py` to correctly share the database connection across FastAPI test client threads. Additionally, patch the application's session maker (e.g., `wms.main.AsyncSessionLocal`) via `unittest.mock.patch` in test fixtures to ensure FastAPI lifespan events initialize schemas in the test database instead of the physical database.
- **Test Coverage**: Always document and explicitly cover all initial requirements and requested features with tests.
- **Frontend Verification**: Frontend UI changes require visual verification using a local Playwright script to screenshot and confirm rendering before committing.

## Version Control Workflow
- **Rebasing & Merging**: When working on an existing, previous branch (e.g., rebasing or merging), features that have been added to the main branch in the intermediate interval must not be removed. All branches being merged in, along with their matching PRs, must be explicitly referenced in the commit comments and any new PRs.

## Never Do
- Send sensitive data to third-party LLM APIs.
- Use `# noqa` or `# ruff: noqa` directives to suppress linting and formatting errors; always resolve the underlying issues (e.g., missing docstrings, line length violations, import sorting) to strictly enforce project standards.
- Use `print()` for logging (use the `logging` module).
- Rely solely on implicit schema creation (use Alembic).
- Commit physical database files (e.g., `*.db`, `*.sqlite`) to version control; always include them in `.gitignore`.
- Use the `x or y` shortcut syntax for non-boolean results.

## Executable Commands
- **Run the app**: `uv run uvicorn wms.main:app`
- **Run tests**: `uv run pytest` or `uv run tox`
- **Run linting**: `uv run ruff check`
- **Run type checking**: `uv run pyright`
- **Build CSS**: `./tailwindcss -i src/wms/static/input.css -o src/wms/static/output.css --minify`
