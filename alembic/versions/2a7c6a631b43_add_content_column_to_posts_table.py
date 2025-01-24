"""Add content column to Posts table

Revision ID: 2a7c6a631b43
Revises: 384daca1a508
Create Date: 2025-01-22 21:00:34.825685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a7c6a631b43'
down_revision: Union[str, None] = '384daca1a508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts', 'content')
    pass
