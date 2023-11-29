"""create authors table

Revision ID: a6909ee4f34a
Revises: fcbf3558d14d
Create Date: 2023-11-27 15:52:27.288575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas.base_entity import Gender

# revision identifiers, used by Alembic.
revision: str = 'a6909ee4f34a'
down_revision: Union[str, None] = 'bf445c545e89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'authors'


def upgrade() -> None:
    op.create_table(table_name,
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('full_name', sa.String, nullable=False),
        sa.Column('gender', sa.Enum(Gender), nullable=False, default=Gender.NONE),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    op.drop_table(table_name)
    op.execute('DROP TYPE gender;')
