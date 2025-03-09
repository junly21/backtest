"""백테스트 테이블 구조 개선

Revision ID: 299480f4ec25
Revises: 90ad1f6e13f4
Create Date: 2025-03-09 13:27:40.294661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299480f4ec25'
down_revision: Union[str, None] = '90ad1f6e13f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('backtests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_year', sa.Integer(), nullable=False),
    sa.Column('start_month', sa.Integer(), nullable=False),
    sa.Column('initial_investment', sa.Float(), nullable=False),
    sa.Column('trade_day', sa.Integer(), nullable=False),
    sa.Column('fee_rate', sa.Float(), nullable=False),
    sa.Column('momentum_window', sa.Integer(), nullable=False),
    sa.Column('nav_history', sa.JSON(), nullable=False),
    sa.Column('weight_history', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('backtests')
    # ### end Alembic commands ###
