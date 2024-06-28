"""add course

Revision ID: 24e1eee8778c
Revises: a4712db392fe
Create Date: 2024-06-28 07:28:48.840633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '24e1eee8778c'
down_revision: Union[str, None] = 'a4712db392fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'courses',
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
        sa.Column('cover', sa.String(), nullable=False),
    )


def downgrade() -> None:
    pass
