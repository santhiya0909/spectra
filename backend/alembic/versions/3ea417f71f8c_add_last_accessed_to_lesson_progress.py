"""add last_accessed to lesson progress

Revision ID: 3ea417f71f8c
Revises: 38a101bfa821
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ea417f71f8c"
down_revision: Union[str, Sequence[str], None] = "38a101bfa821"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First add the column as nullable because SQLite
    # cannot directly add a NOT NULL column to a table
    # that already contains data.
    op.add_column(
        "lesson_progress",
        sa.Column(
            "last_accessed",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Give existing lesson progress rows a timestamp.
    op.execute(
        """
        UPDATE lesson_progress
        SET last_accessed = CURRENT_TIMESTAMP
        WHERE last_accessed IS NULL
        """
    )

    # Now make the column NOT NULL.
    with op.batch_alter_table("lesson_progress") as batch_op:
        batch_op.alter_column(
            "last_accessed",
            existing_type=sa.DateTime(timezone=True),
            nullable=False,
        )

    # Add index.
    op.create_index(
        "ix_lesson_progress_last_accessed",
        "lesson_progress",
        ["last_accessed"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_lesson_progress_last_accessed",
        table_name="lesson_progress",
    )

    op.drop_column("lesson_progress", "last_accessed")