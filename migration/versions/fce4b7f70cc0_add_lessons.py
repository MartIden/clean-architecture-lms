"""add lessons

Revision ID: fce4b7f70cc0
Revises: 24e1eee8778c
Create Date: 2024-06-28 09:22:51.123344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text, ForeignKey

# revision identifiers, used by Alembic.
revision: str = 'fce4b7f70cc0'
down_revision: Union[str, None] = '24e1eee8778c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'lessons',
        sa.Column(
            'id',
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column('created_at', sa.BigInteger(), nullable=False),
        sa.Column('updated_at', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.String(), nullable=False, unique=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('cover', sa.String(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
    )

    sa.ForeignKeyConstraint(
        ['course_id'],
        ['courses.id'],
        name=op.f('refinance_credit_fk'),
        onupdate='CASCADE',
        ondelete='CASCADE'
    ),
    op.create_index("ix_lessons_course_id", "lessons", ["course_id"])


def downgrade() -> None:
    pass
