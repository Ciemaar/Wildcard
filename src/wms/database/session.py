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

engine = create_async_engine(async_database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide an async database session per request."""
    async with AsyncSessionLocal() as session:
        yield session
