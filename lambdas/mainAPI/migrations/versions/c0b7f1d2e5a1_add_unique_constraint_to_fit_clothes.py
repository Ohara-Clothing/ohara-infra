"""add unique constraint to fit_clothes

Revision ID: c0b7f1d2e5a1
Revises: 081df979b0fa
Create Date: 2026-04-30 16:40:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c0b7f1d2e5a1"
down_revision: Union[str, Sequence[str], None] = "081df979b0fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM fit_clothes a
        USING fit_clothes b
        WHERE a.ctid < b.ctid
          AND a."fitId" = b."fitId"
          AND a."clothesId" = b."clothesId"
        """
    )
    op.create_unique_constraint(
        "uq_fit_clothes_fitId_clothesId",
        "fit_clothes",
        ["fitId", "clothesId"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_fit_clothes_fitId_clothesId",
        "fit_clothes",
        type_="unique",
    )
