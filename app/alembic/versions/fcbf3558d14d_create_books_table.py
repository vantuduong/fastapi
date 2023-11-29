"""create books table

Revision ID: fcbf3558d14d
Revises: bf445c545e89
Create Date: 2023-11-27 15:52:19.551222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcbf3558d14d'
down_revision: Union[str, None] = 'a6909ee4f34a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'books'

def upgrade() -> None:
    op.create_table(table_name,
        sa.Column('id', sa.Uuid, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author_id', sa.Uuid, nullable=False),
        sa.Column('user_id', sa.Uuid, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_published', sa.Boolean, default=False),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_foreign_key('fk_book_author', table_name, 'authors', ['author_id'], ['id'])
    op.create_foreign_key('fk_book_user', table_name, 'users', ['user_id'], ['id'])

def downgrade() -> None:
    op.drop_table(table_name)
