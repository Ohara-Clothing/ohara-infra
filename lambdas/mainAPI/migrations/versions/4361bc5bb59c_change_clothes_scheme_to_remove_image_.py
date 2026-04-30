"""change clothes scheme to remove image key

Revision ID: 4361bc5bb59c
Revises: d259afdf793b
Create Date: 2026-04-30 10:44:53.864010

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4361bc5bb59c"
down_revision: Union[str, Sequence[str], None] = "d259afdf793b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Drop all known foreign key constraints
    op.drop_constraint(
        "user_clothes_clothesId_fkey", "user_clothes", type_="foreignkey"
    )
    op.drop_constraint("fit_clothes_clothesId_fkey", "fit_clothes", type_="foreignkey")

    # 2. Remap legacy string ids to generated UUID values first
    op.execute(
        """
        CREATE TEMP TABLE clothes_uuid_map AS
        SELECT DISTINCT old_id, gen_random_uuid()::text AS new_id
        FROM (
            SELECT "clothesId"::text AS old_id FROM clothes
            UNION
            SELECT "clothesId"::text AS old_id FROM user_clothes
            UNION
            SELECT "clothesId"::text AS old_id FROM fit_clothes
        ) AS clothes_ids
        WHERE old_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE clothes AS c
        SET "clothesId" = m.new_id
        FROM clothes_uuid_map AS m
        WHERE c."clothesId"::text = m.old_id
        """
    )
    op.execute(
        """
        UPDATE user_clothes AS c
        SET "clothesId" = m.new_id
        FROM clothes_uuid_map AS m
        WHERE c."clothesId"::text = m.old_id
        """
    )
    op.execute(
        """
        UPDATE fit_clothes AS c
        SET "clothesId" = m.new_id
        FROM clothes_uuid_map AS m
        WHERE c."clothesId"::text = m.old_id
        """
    )

    # 3. Convert the Parent table (clothes) and children to UUID
    op.execute(
        'ALTER TABLE clothes ALTER COLUMN "clothesId" TYPE UUID USING "clothesId"::uuid'
    )
    op.execute(
        'ALTER TABLE user_clothes ALTER COLUMN "clothesId" TYPE UUID USING "clothesId"::uuid'
    )
    op.execute(
        'ALTER TABLE fit_clothes ALTER COLUMN "clothesId" TYPE UUID USING "clothesId"::uuid'
    )
    op.execute('ALTER TABLE clothes ALTER COLUMN "clothesId" SET DEFAULT gen_random_uuid()')

    # 4. Re-create all foreign key constraints
    op.create_foreign_key(
        "user_clothes_clothesId_fkey",
        "user_clothes",
        "clothes",
        ["clothesId"],
        ["clothesId"],
    )
    op.create_foreign_key(
        "fit_clothes_clothesId_fkey",
        "fit_clothes",
        "clothes",
        ["clothesId"],
        ["clothesId"],
    )

    # 5. Final cleanup
    op.drop_index("ix_clothes_clothesId", table_name="clothes")
    op.drop_column("clothes", "imageKey")


def downgrade() -> None:
    # Standard reverse procedure
    op.drop_constraint(
        "user_clothes_clothesId_fkey", "user_clothes", type_="foreignkey"
    )
    op.drop_constraint("fit_clothes_clothesId_fkey", "fit_clothes", type_="foreignkey")

    op.alter_column("clothes", "clothesId", type_=sa.VARCHAR())
    op.alter_column("user_clothes", "clothesId", type_=sa.VARCHAR())
    op.alter_column("fit_clothes", "clothesId", type_=sa.VARCHAR())

    op.create_foreign_key(
        "user_clothes_clothesId_fkey",
        "user_clothes",
        "clothes",
        ["clothesId"],
        ["clothesId"],
    )
    op.create_foreign_key(
        "fit_clothes_clothesId_fkey",
        "fit_clothes",
        "clothes",
        ["clothesId"],
        ["clothesId"],
    )

    op.add_column("clothes", sa.Column("imageKey", sa.VARCHAR(), nullable=True))
    op.create_index("ix_clothes_clothesId", "clothes", ["clothesId"])
