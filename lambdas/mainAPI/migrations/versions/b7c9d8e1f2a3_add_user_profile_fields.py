"""add user profile fields

Revision ID: b7c9d8e1f2a3
Revises: a1b2c3d4e5f6
Create Date: 2026-04-30 18:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "b7c9d8e1f2a3"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("description", sa.String(), nullable=True))
    op.add_column("users", sa.Column("style", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "favoriteClothesIds",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "pinnedFitIds",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "pinnedFitIds")
    op.drop_column("users", "favoriteClothesIds")
    op.drop_column("users", "style")
    op.drop_column("users", "description")
