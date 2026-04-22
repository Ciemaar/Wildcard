from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from wms.database.models import Base
from wms.database.session import get_db
from wms.main import app

# Create an in-memory SQLite database for testing
async_test_database_url = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    async_test_database_url,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
AsyncTestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency override to yield an in-memory test database session."""
    async with AsyncTestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_test_db():
    """Fixture to set up and tear down the database schema for tests."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
