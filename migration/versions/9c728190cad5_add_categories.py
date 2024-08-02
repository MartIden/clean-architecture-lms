"""add categories

Revision ID: 9c728190cad5
Revises: 8fa427714cc8
Create Date: 2024-07-27 13:22:54.700737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '9c728190cad5'
down_revision: Union[str, None] = '8fa427714cc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'categories',
        sa.Column(
            'id',
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column('created_at', sa.BigInteger(), nullable=False),
        sa.Column('updated_at', sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(), nullable=False, unique=True),
        sa.Column("description", sa.String(), nullable=False),
    )


def downgrade() -> None:
    pass
