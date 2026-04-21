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


class BatchPrompt(Base):
    """Association table model between Batch and Prompt."""

    __tablename__ = "BatchPrompt"
    batch_id: Mapped[str] = mapped_column(ForeignKey("Batch.id"), primary_key=True)
    prompt_id: Mapped[str] = mapped_column(ForeignKey("Prompt.id"), primary_key=True)


class Prompt(Base):
    """Model representing a photography game prompt."""

    __tablename__ = "Prompt"
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
        secondary="BatchPrompt", back_populates="prompts"
    )


class Batch(Base):
    """Model representing a batch of prompts generated for printing."""

    __tablename__ = "Batch"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    printed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    prompts: Mapped[List["Prompt"]] = relationship(
        secondary="BatchPrompt", back_populates="batches"
    )
