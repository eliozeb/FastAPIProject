"""Add foreign to Posts table

Revision ID: 28297445446b
Revises: d5690e28eb00
Create Date: 2025-01-23 00:20:40.143421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28297445446b'
down_revision: Union[str, None] = 'd5690e28eb00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='Posts', referent_table='Users', 
                          local_cols= ['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='Posts')
    op.drop_column('Posts', 'owner_id')
    pass
