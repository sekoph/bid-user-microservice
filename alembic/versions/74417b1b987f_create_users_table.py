"""create users table

Revision ID: 74417b1b987f
Revises: 7c1146640841
Create Date: 2024-10-17 17:38:52.248325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision: str = '74417b1b987f'
down_revision: Union[str, None] = '7c1146640841'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('disabled', sa.Boolean(), default=False),
        sa.Column('date_created', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.Column('user_type_id', sa.Integer),
        sa.PrimaryKeyConstraint('id'),
    )
   
   op.create_foreign_key('fk_user_userType', 'users', 'user_type', ['user_type_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_table('users')
