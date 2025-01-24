"""Add last few columns to Posts table

Revision ID: 2e34d4fcc13a
Revises: 28297445446b
Create Date: 2025-01-23 07:39:28.528766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e34d4fcc13a'
down_revision: Union[str, None] = '28297445446b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column(
                  'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('Posts', sa.Column( 
                  'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
                 ('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    pass
