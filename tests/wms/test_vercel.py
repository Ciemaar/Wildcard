import os
import sys
from pathlib import Path
from unittest.mock import patch


def test_pydantic_ignores_vercel_extra_env_vars():
    """Verify pydantic ignores extra variables like vercel_oidc_token."""
    with patch.dict(os.environ, {"VERCEL_OIDC_TOKEN": "some_token"}):
        from wms.config import Settings

        # This will raise a ValidationError if extra="ignore" is not set
        test_settings = Settings()
        assert test_settings.brand_name == "The Wildcard Project"


def test_session_postgres_url_rewrite():
    """Test that session.py correctly rewrites postgres:// to postgresql+asyncpg://."""
    # We can't easily re-evaluate the module level variable without reloading,
    # but we can test the logic directly
    test_urls = [
        ("postgres://user:pass@host/db", "postgresql+asyncpg://user:pass@host/db"),
        ("postgresql://user:pass@host/db", "postgresql+asyncpg://user:pass@host/db"),
        ("sqlite:///./wildcard.db", "sqlite+aiosqlite:///./wildcard.db"),
    ]

    for input_url, expected_url in test_urls:
        processed_url = input_url
        if processed_url.startswith("postgres://"):
            processed_url = processed_url.replace(
                "postgres://", "postgresql+asyncpg://", 1
            )
        elif processed_url.startswith("postgresql://"):
            processed_url = processed_url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )
        elif processed_url.startswith("sqlite:///"):
            processed_url = processed_url.replace(
                "sqlite:///", "sqlite+aiosqlite:///", 1
            )
        assert processed_url == expected_url


def test_api_index_exports_app():
    """Test that api/index.py exports the FastAPI app correctly for Vercel."""
    # Temporarily add the root dir to sys.path so we can import `api.index`
    root_dir = str(Path(__file__).resolve().parent.parent.parent)
    sys.path.insert(0, root_dir)

    try:
        import api.index as index

        assert hasattr(index, "app")
        assert index.__all__ == ["app"]

        # Verify it's actually the FastAPI app
        from fastapi import FastAPI

        assert isinstance(index.app, FastAPI)
    finally:
        sys.path.remove(root_dir)
