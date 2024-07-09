"""add progress table

Revision ID: 8fa427714cc8
Revises: 74a49bf410f9
Create Date: 2024-07-09 08:30:29.971076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "8fa427714cc8"
down_revision: Union[str, None] = "74a49bf410f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "progress",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("lesson_id", sa.UUID(), nullable=False),
    )

    op.create_unique_constraint(
        "uq_progress_user_id_course_id_lesson_id",
        "progress",
        ["course_id", "user_id", "lesson_id"]
    )

    sa.ForeignKeyConstraint(
        ["course_id"],
        ["courses.id"],
        name=op.f("progress_course_id_fk"),
        onupdate="CASCADE",
        ondelete="CASCADE"
    )

    sa.ForeignKeyConstraint(
        ["user_id"],
        ["users.id"],
        name=op.f("progress_user_id_fk"),
        onupdate="CASCADE",
        ondelete="CASCADE"
    )

    sa.ForeignKeyConstraint(
        ["lesson_id"],
        ["lessons.id"],
        name=op.f("progress_lesson_id_fk"),
        onupdate="CASCADE",
        ondelete="CASCADE"
    )


def downgrade() -> None:
    pass
