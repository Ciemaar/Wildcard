import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from wms.database.models import Mission

logger = logging.getLogger(__name__)

SAMPLE_PROMPTS = [
    {"text": "Photograph a secret", "category": "Abstract", "difficulty": 2},
    {
        "text": "Capture the feeling of Monday morning",
        "category": "Abstract",
        "difficulty": 3,
    },
    {"text": "Find a perfect reflection", "category": "Urban", "difficulty": 1},
    {
        "text": "Take a photo of someone else taking a photo",
        "category": "People",
        "difficulty": 2,
    },
    {
        "text": "Photograph a texture that looks soft but is hard",
        "category": "Nature",
        "difficulty": 2,
    },
    {"text": "An abandoned object", "category": "Urban", "difficulty": 1},
    {"text": "Symmetry in nature", "category": "Nature", "difficulty": 3},
    {"text": "A tiny detail easily missed", "category": "Macro", "difficulty": 1},
    {"text": "Motion blur in the city", "category": "Urban", "difficulty": 2},
    {"text": "Something that is out of place", "category": "Abstract", "difficulty": 2},
]


async def seed_data(session: AsyncSession) -> None:
    """Seed the database with sample missions if it's empty."""
    result = await session.execute(select(Mission).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    for data in SAMPLE_PROMPTS:
        session.add(Mission(**data))
    await session.commit()
