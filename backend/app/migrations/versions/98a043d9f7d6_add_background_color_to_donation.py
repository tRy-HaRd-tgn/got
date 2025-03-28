"""Add background color to donation

Revision ID: 98a043d9f7d6
Revises: 4bdb1d6b03af
Create Date: 2025-01-22 19:25:11.261610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98a043d9f7d6'
down_revision: Union[str, None] = '4bdb1d6b03af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donations', sa.Column('background_color', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donations', 'background_color')
    # ### end Alembic commands ###
