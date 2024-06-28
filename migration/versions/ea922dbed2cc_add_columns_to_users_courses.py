"""add columns to users_courses

Revision ID: ea922dbed2cc
Revises: bc480f3db517
Create Date: 2024-06-28 15:23:19.720266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea922dbed2cc'
down_revision: Union[str, None] = 'bc480f3db517'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users_courses", sa.Column("created_at", sa.Integer(), nullable=False))
    op.add_column("users_courses", sa.Column("updated_at", sa.Integer(), nullable=False))


def downgrade() -> None:
    pass
