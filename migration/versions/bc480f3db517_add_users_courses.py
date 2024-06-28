"""add users_courses

Revision ID: bc480f3db517
Revises: 93bc8b9882d8
Create Date: 2024-06-28 12:53:20.947551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'bc480f3db517'
down_revision: Union[str, None] = '93bc8b9882d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users_courses',
        sa.Column(
            'id',
            sa.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
    )

    sa.UniqueConstraint("user_id", "course_id", name="uc_users_courses_to_user_id_course_id")

    sa.ForeignKeyConstraint(
        ['course_id'],
        ['courses.id'],
        name=op.f('users_courses_course_id_fk'),
        onupdate='CASCADE',
        ondelete='CASCADE'
    )

    sa.ForeignKeyConstraint(
        ['user_id'],
        ['users.id'],
        name=op.f('users_courses_user_id_fk'),
        onupdate='CASCADE',
        ondelete='CASCADE'
    )

    op.create_index("ix_users_courses", "users_courses", ["course_id", "user_id"])
    op.create_index("ix_users_courses_user_id", "users_courses", ["user_id"])


def downgrade() -> None:
    pass
