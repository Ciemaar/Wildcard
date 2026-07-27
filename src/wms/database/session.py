import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from wms.config import settings

logger = logging.getLogger(__name__)

async_database_url = settings.database_url
if async_database_url.startswith("postgres://"):
    async_database_url = async_database_url.replace(
        "postgres://", "postgresql+asyncpg://", 1
    )
elif async_database_url.startswith("postgresql://"):
    async_database_url = async_database_url.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )
elif async_database_url.startswith("sqlite:///"):
    async_database_url = async_database_url.replace(
        "sqlite:///", "sqlite+aiosqlite:///", 1
    )

if async_database_url.startswith(
    "sqlite+aiosqlite:///"
) and async_database_url != "sqlite+aiosqlite:///:memory:":
    # Vercel's serverless environment has a read-only filesystem (except /tmp)
    # If the user forgot to set the DATABASE_URL environment variable to a
    # Postgres instance, it will fall back to the default file-based SQLite URL
    # and crash on startup. We intercept this here and default to an in-memory
    # DB to prevent a hard 500 error. Persistence will be lost between requests.
    if "/var/task" in __file__:
        logger.warning(
            "Running in Vercel with a file-based SQLite database. "
            "Falling back to in-memory SQLite to prevent a crash. "
            "Please configure a Postgres DATABASE_URL."
        )
        async_database_url = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(async_database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide an async database session per request."""
    async with AsyncSessionLocal() as session:
        yield session
