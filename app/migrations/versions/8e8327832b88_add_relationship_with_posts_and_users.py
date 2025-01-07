"""Add relationship with posts and users

Revision ID: 8e8327832b88
Revises: 94208f0123a4
Create Date: 2025-01-04 18:25:42.177728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e8327832b88'
down_revision: Union[str, None] = '94208f0123a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###
