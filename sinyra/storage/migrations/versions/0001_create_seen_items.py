"""create seen_items table

Revision ID: 0001
Revises:
Create Date: 2026-05-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "seen_items",
        sa.Column("hash", sa.String(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("link", sa.Text(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("hash"),
    )


def downgrade() -> None:
    op.drop_table("seen_items")
