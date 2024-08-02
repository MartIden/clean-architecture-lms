"""add categories-courses

Revision ID: 21f7da935e9c
Revises: 9c728190cad5
Create Date: 2024-07-27 13:27:56.331734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '21f7da935e9c'
down_revision: Union[str, None] = '9c728190cad5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories_courses',
        sa.Column(
            'id',
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.BigInteger(), nullable=False),
    )

    sa.UniqueConstraint("category_id", "course_id", name="uc_users_courses_to_category_id_course_id")

    sa.ForeignKeyConstraint(
        ['course_id'],
        ['courses.id'],
        name=op.f('users_courses_course_id_fk'),
        onupdate='CASCADE',
        ondelete='CASCADE'
    )

    sa.ForeignKeyConstraint(
        ['category_id'],
        ['categories.id'],
        name=op.f('users_courses_category_id_fk'),
        onupdate='CASCADE',
        ondelete='CASCADE'
    )

    op.create_index(
        "ix_categories_courses",
        "categories_courses",
        ["course_id", "category_id"]
    )

    op.create_index(
        "ix_categories_courses_category_id",
        "categories_courses",
        ["category_id"]
    )


def downgrade() -> None:
    pass
