"""create Posts table

Revision ID: 384daca1a508
Revises: 
Create Date: 2025-01-22 08:09:09.521128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '384daca1a508'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Posts', sa.Column('id', sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title', sa.String(length=255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('Posts')
    pass
