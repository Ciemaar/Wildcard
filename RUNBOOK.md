# Runbook

This guide covers the necessary steps to set up, build, run, and maintain the Wildcard Management System (WMS) application.

## 1. Prerequisites
Ensure you have the following installed on your machine:
- Python 3.12+
- `uv` (for package management)

## 2. Virtual Environment Setup & Installation
The project exclusively uses `uv` for dependency management.
To set up the virtual environment and install all dependencies:
```bash
uv sync
```

## 3. Database Initialization
Before running the application, ensure the database is fully initialized to the latest schema using Alembic:
```bash
PYTHONPATH=src uv run alembic upgrade head
```
*(Note: On application startup, the `seed_data` script will automatically inject 10 sample prompts if the database is empty.)*

## 4. Frontend Assets (Tailwind CSS)
The application uses Tailwind CSS. To build the required CSS file for development or production:
1. Ensure the standalone tailwind CLI (`./tailwindcss`) is present in the root. If not, download it according to `DEVELOPER_GUIDE.md`.
2. Run the build command:
```bash
./tailwindcss -i src/wms/static/input.css -o src/wms/static/output.css --minify
```

## 5. Running the Application (Development)
Start the application server using `uvicorn`:
```bash
PYTHONPATH=src uv run uvicorn wms.main:app --reload --port 3000
```
Access the application at `http://localhost:3000`.

## 6. Running the Application (Production)
For production deployments, remove the `--reload` flag and consider using `gunicorn` with `uvicorn` workers for better performance.
```bash
PYTHONPATH=src uv run uvicorn wms.main:app --host 0.0.0.0 --port 8000
```

## 7. Regular Maintenance
- **Dependencies:** Periodically review and update `uv.lock`.
- **Database Migrations:** If changes are made to `models.py`, generate a new migration: `PYTHONPATH=src uv run alembic revision --autogenerate -m "description"`
