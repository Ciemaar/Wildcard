# Tooling Evaluation: Vercel

## Problem Description

The project needs to be deployed to a web hosting provider. Currently, the project utilizes FastAPI with a strict `uv` and `pyproject.toml` dependency management approach. Additionally, local development utilizes an ephemeral SQLite database, necessitating an external persistent store for production. We need to evaluate hosting providers that can support this architecture efficiently.

## Options Evaluated

### Option 1: Vercel

Vercel is a cloud platform for static sites and Serverless Functions.

- **Pros:**
  - Zero-configuration deployments for many frameworks.
  - Built-in global Edge Network (CDN) for static assets.
  - Provides managed PostgreSQL databases (Vercel Postgres) out of the box, fulfilling our need for a production data store.
  - Excellent developer experience with automatic preview deployments per pull request.
- **Cons:**
  - Vercel's standard Python builder natively expects dependencies to be defined in a `requirements.txt` or `Pipfile`, which conflicts with our `uv`-centric approach.
  - Deployments are ephemeral serverless functions, meaning background tasks or persistent in-memory states are not supported natively without external queues.
  - Expects a specific entrypoint format (`api/index.py`) for Python serverless functions.
- **Mitigation:** Create a custom bash script (`vercel-build.sh`) that dynamically installs `uv` and runs `uv pip compile pyproject.toml -o requirements.txt`, satisfying the python builder without checking `requirements.txt` into git. We can adapt our application entrypoint to `api/index.py` easily.

### Option 2: Heroku / Render (PaaS)

Traditional Platform-as-a-Service providers.

- **Pros:**
  - Supports persistent running processes (web dynos) without the cold starts or ephemeral limits of serverless functions.
  - More flexible dependency management without strict `requirements.txt` requirements if using Dockerfile deployments.
- **Cons:**
  - More configuration required compared to Vercel's seamless GitHub integration.
  - Can become expensive quickly as traffic scales, unlike Vercel's generous free/hobby tiers.
  - CDN setup for static files is often a separate integration step.

### Option 3: AWS / GCP / Azure (IaaS)

Infrastructure-as-a-Service providers using Docker containers (e.g., AWS ECS, GCP Cloud Run).

- **Pros:**
  - Maximum flexibility and control over the environment.
  - Can run anything that fits in a Docker container.
- **Cons:**
  - Significant operational overhead to manage infrastructure, load balancers, and CI/CD pipelines.
  - Overkill for a relatively straightforward FastAPI web application.

## Recommendation & Decision

We proceed with **Option 1: Vercel**. The developer experience, automatic preview environments, and integrated managed PostgreSQL make it the most attractive option. The primary drawback—Vercel's `requirements.txt` expectation—can be cleanly mitigated with a custom build script that integrates our `uv` tooling seamlessly.

### Implementation Details for Vercel Integration

To adopt Vercel while maintaining our project standards, we will:

1. **Use the Native Vercel Python Builder:** We will use the standard `@vercel/python` builder but inject a build step (`vercel-build.sh`) during the `Install Command` phase. This script will dynamically generate `requirements.txt` from our `pyproject.toml` using `uv`.
1. **Optional Dependencies:** We will add Vercel-specific Postgres dependencies (`asyncpg`, `psycopg`) to `[project.optional-dependencies]` under the `vercel` key in `pyproject.toml` to keep the core local installation clean.
1. **Configuration:** We will include `vercel.json` to properly map static routes to the CDN and API requests to the `api/index.py` entry point.
1. **Database Routing:** We will adjust `session.py` to seamlessly upgrade standard `postgres://` URLs (provided by Vercel Postgres) to `postgresql+asyncpg://` to interface with the database natively while retaining SQLite for local development.

## Local Tooling Additions

To replicate Vercel's PostgreSQL database for local development, we added a `docker-compose.yaml` configuration.

Along with the database, we are testing the use of **Adminer**, a lightweight, single-file database management tool running as a container alongside Postgres.

- **Why Adminer?** It requires zero complex configuration compared to alternatives like pgAdmin, and provides a simple, direct interface to manually inspect schema migrations and data inside the ephemeral dockerized database.
