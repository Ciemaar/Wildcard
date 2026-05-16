import datetime
import uuid
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models."""

    pass


def generate_uuid() -> str:
    """Generate a random UUID string for model primary keys."""
    return str(uuid.uuid4())


class BatchMission(Base):
    """Association table model between Batch and Mission."""

    __tablename__ = "BatchMission"
    batch_id: Mapped[str] = mapped_column(ForeignKey("Batch.id"), primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("Mission.id"), primary_key=True)


class Mission(Base):
    """Model representing a photography game mission."""

    __tablename__ = "Mission"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    text: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="DRAFT")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    batches: Mapped[List["Batch"]] = relationship(
        secondary="BatchMission", back_populates="missions"
    )


class Batch(Base):
    """Model representing a batch of missions generated for printing."""

    __tablename__ = "Batch"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    printed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    missions: Mapped[List["Mission"]] = relationship(
        secondary="BatchMission", back_populates="batches"
    )
