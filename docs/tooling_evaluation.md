# Tooling Evaluation: Vercel

## Problem Description
The project needs to be deployed to Vercel, but Vercel's standard Python builder natively expects dependencies to be defined in a `requirements.txt` or `Pipfile`. However, our project strictly uses `uv` and `pyproject.toml` for dependency management. Furthermore, our project utilizes FastAPI, whereas Vercel expects a specific entrypoint format (`api/index.py`) and has specific CDN requirements for static files. Lastly, Vercel deployments are ephemeral, and local development utilizes an ephemeral SQLite database, necessitating an external persistent store for production.

## Options Evaluated
### Option 1: Native Vercel Python Builder with Vercel configuration
Use the standard `@vercel/python` builder but inject a build step.
*   **Pros:** Native integration, easy to configure via `vercel.json` without fighting the platform.
*   **Cons:** Vercel builder *requires* `requirements.txt`.
*   **Mitigation:** Create a custom bash script (`vercel-build.sh`) that Vercel runs during the `Install Command` phase. This script dynamically installs `uv` and runs `uv pip compile pyproject.toml -o requirements.txt`, satisfying the python builder without checking `requirements.txt` into git.

### Option 2: Build Output API (v3)
Manually bundle the application into `.vercel/output/functions` and `.vercel/output/static`.
*   **Pros:** Total control over the python virtual environment. Can use `uv` directly to bundle dependencies.
*   **Cons:** High maintenance burden. Requires a complex custom build script and defeats the purpose of Vercel's zero-config paradigm.

## Recommendation & Decision
We proceed with **Option 1**. It balances the constraint of not committing a `requirements.txt` file while remaining firmly inside the happy path of Vercel's deployment ecosystem.

Additional actions taken:
- Added `vercel` CLI as an optional dependency via `uv add --optional vercel vercel` to enable `uv run vercel ...` commands.
- Included `vercel.json` to properly map routes and API entry points.
- Adjusted `session.py` to seamlessly upgrade standard `postgres://` URLs to `postgresql+asyncpg://` to interface with Vercel Postgres natively while retaining SQLite for local dev.
