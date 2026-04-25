"""Rename Prompt to Mission.

Revision ID: 7611442310ec
Revises: f6093771bac3
Create Date: 2026-04-25 00:48:26.287494

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7611442310ec"
down_revision: Union[str, Sequence[str], None] = "f6093771bac3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("Prompt", "Mission")
    op.rename_table("BatchPrompt", "BatchMission")
    with op.batch_alter_table("BatchMission") as batch_op:
        batch_op.alter_column("prompt_id", new_column_name="mission_id")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("BatchMission") as batch_op:
        batch_op.alter_column("mission_id", new_column_name="prompt_id")
    op.rename_table("BatchMission", "BatchPrompt")
    op.rename_table("Mission", "Prompt")
