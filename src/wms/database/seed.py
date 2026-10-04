lazy import logging
lazy from pathlib import Path

lazy import yaml
lazy from sqlalchemy import select
lazy from sqlalchemy.ext.asyncio import AsyncSession

lazy from wms.database.models import Mission

logger = logging.getLogger(__name__)


async def seed_data(session: AsyncSession) -> None:
    """Seed the database with sample missions if it's empty."""
    result = await session.execute(select(Mission).limit(1))
    if result.scalar_one_or_none() is not None:
        return

    seed_file = Path(__file__).parent / "seed_data.yaml"
    with open(seed_file, "r") as f:
        sample_missions = yaml.safe_load(f)

    for data in sample_missions:
        session.add(Mission(**data))
    await session.commit()
