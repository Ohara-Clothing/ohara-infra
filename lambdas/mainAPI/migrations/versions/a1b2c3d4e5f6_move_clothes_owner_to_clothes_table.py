"""move clothes ownership to clothes table

Revision ID: a1b2c3d4e5f6
Revises: c0b7f1d2e5a1
Create Date: 2026-04-30 17:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "c0b7f1d2e5a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("clothes", sa.Column("userId", sa.Uuid(), nullable=True))
    op.execute(
        """
        UPDATE clothes AS c
        SET "userId" = owner_map."userId"
        FROM (
            SELECT DISTINCT ON ("clothesId") "clothesId", "userId"
            FROM user_clothes
            ORDER BY "clothesId", "addedAt" DESC
        ) AS owner_map
        WHERE c."clothesId" = owner_map."clothesId"
        """
    )
    op.create_foreign_key("clothes_userId_fkey", "clothes", "users", ["userId"], ["userId"])
    op.create_index("ix_clothes_userId", "clothes", ["userId"], unique=False)
    op.drop_table("user_clothes")


def downgrade() -> None:
    op.create_table(
        "user_clothes",
        sa.Column("userClothesId", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("userId", sa.Uuid(), nullable=False),
        sa.Column("clothesId", sa.Uuid(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("addedAt", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["clothesId"], ["clothes.clothesId"]),
        sa.ForeignKeyConstraint(["userId"], ["users.userId"]),
        sa.PrimaryKeyConstraint("userClothesId"),
    )
    op.execute(
        """
        INSERT INTO user_clothes ("userId", "clothesId", "quantity", "addedAt")
        SELECT "userId", "clothesId", 1, now()
        FROM clothes
        WHERE "userId" IS NOT NULL
        """
    )
    op.drop_index("ix_clothes_userId", table_name="clothes")
    op.drop_constraint("clothes_userId_fkey", "clothes", type_="foreignkey")
    op.drop_column("clothes", "userId")
