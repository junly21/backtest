"""Create prices table

Revision ID: 210d87aaeb8c
Revises: 
Create Date: 2025-03-08 00:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '210d87aaeb8c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "prices",
        sa.Column("date", sa.Date, primary_key=True),
        sa.Column("ticker", sa.String(10), primary_key=True),
        sa.Column("price", sa.Numeric(13, 4), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("prices")
