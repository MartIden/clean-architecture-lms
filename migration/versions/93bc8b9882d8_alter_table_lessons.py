"""alter table lessons

Revision ID: 93bc8b9882d8
Revises: fce4b7f70cc0
Create Date: 2024-06-28 11:50:49.827466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93bc8b9882d8'
down_revision: Union[str, None] = 'fce4b7f70cc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('lessons', 'text', new_column_name='content')


def downgrade() -> None:
    pass
