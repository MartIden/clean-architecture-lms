"""add unique constraint to users_courses

Revision ID: fb2a5e1f7441
Revises: ea922dbed2cc
Create Date: 2024-06-28 15:33:29.050553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb2a5e1f7441'
down_revision: Union[str, None] = 'ea922dbed2cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_user_id_course_id',
        'users_courses',
        ['course_id', "user_id"]
    )


def downgrade() -> None:
    pass
