"""create users table

Revision ID: bf445c545e89
Revises: 
Create Date: 2023-11-27 15:52:11.942569

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision: str = 'bf445c545e89'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = 'users'

def upgrade() -> None:
    user_table = op.create_table(table_name,
        sa.Column('id', sa.Uuid, primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_admin', sa.Boolean, nullable=False, default=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True)
    )

    op.bulk_insert(user_table, [
        {
            "id": uuid.uuid4(),
            "email": "admin@gmail.com",
            "username": "admin",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "Tu",
            "last_name": "Duong",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ])

def downgrade() -> None:
    op.drop_table(table_name)
