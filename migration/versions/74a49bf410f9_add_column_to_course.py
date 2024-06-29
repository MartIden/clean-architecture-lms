"""add column to course

Revision ID: 74a49bf410f9
Revises: fb2a5e1f7441
Create Date: 2024-06-29 12:14:46.536885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74a49bf410f9'
down_revision: Union[str, None] = 'fb2a5e1f7441'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("author_id", sa.UUID(), nullable=False))
    sa.ForeignKeyConstraint(
        ['author'],
        ['user.id'],
        name=op.f('courses_author_id_fk'),
        onupdate='CASCADE',
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    pass
