"""create user_type table

Revision ID: 7c1146640841
Revises:
Create Date: 2024-10-17 17:34:19.704685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision: str = '7c1146640841'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        'user_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('date_created', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('user_type')
