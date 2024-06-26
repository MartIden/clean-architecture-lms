"""create user table

Revision ID: a4712db392fe
Revises: 
Create Date: 2024-06-25 11:34:09.492753

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'a4712db392fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column('created_at', sa.BigInteger(), nullable=False),
        sa.Column('updated_at', sa.BigInteger(), nullable=False),
        sa.Column('login', sa.String(), nullable=False, unique=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('roles', sa.ARRAY(sa.String), nullable=True, default=[]),
    )
    op.create_index("ix_user_login", "users", ["login"])
    op.create_index("ix_user_email", "users", ["email"])


def downgrade() -> None:
    pass
