"""change ids to UUID and mapped columns to everything

Revision ID: 081df979b0fa
Revises: 4361bc5bb59c
Create Date: 2026-04-30 12:09:10.155415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "081df979b0fa"
down_revision: Union[str, Sequence[str], None] = "4361bc5bb59c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. DROP ALL CONSTRAINTS FIRST
    # Table: user_clothes
    op.drop_constraint("user_clothes_userId_fkey", "user_clothes", type_="foreignkey")
    # Table: fits
    op.drop_constraint("fits_userId_fkey", "fits", type_="foreignkey")
    # Table: fit_clothes
    op.drop_constraint("fit_clothes_fitId_fkey", "fit_clothes", type_="foreignkey")

    # 2. Remap legacy string ids to generated UUID values first
    op.execute(
        """
        CREATE TEMP TABLE users_uuid_map AS
        SELECT DISTINCT old_id, gen_random_uuid()::text AS new_id
        FROM (
            SELECT "userId"::text AS old_id FROM users
            UNION
            SELECT "userId"::text AS old_id FROM user_clothes
            UNION
            SELECT "userId"::text AS old_id FROM fits
        ) AS user_ids
        WHERE old_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE users AS u
        SET "userId" = m.new_id
        FROM users_uuid_map AS m
        WHERE u."userId"::text = m.old_id
        """
    )
    op.execute(
        """
        UPDATE user_clothes AS u
        SET "userId" = m.new_id
        FROM users_uuid_map AS m
        WHERE u."userId"::text = m.old_id
        """
    )
    op.execute(
        """
        UPDATE fits AS f
        SET "userId" = m.new_id
        FROM users_uuid_map AS m
        WHERE f."userId"::text = m.old_id
        """
    )

    op.execute(
        """
        CREATE TEMP TABLE fits_uuid_map AS
        SELECT DISTINCT old_id, gen_random_uuid()::text AS new_id
        FROM (
            SELECT "fitId"::text AS old_id FROM fits
            UNION
            SELECT "fitId"::text AS old_id FROM fit_clothes
        ) AS fit_ids
        WHERE old_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE fits AS f
        SET "fitId" = m.new_id
        FROM fits_uuid_map AS m
        WHERE f."fitId"::text = m.old_id
        """
    )
    op.execute(
        """
        UPDATE fit_clothes AS f
        SET "fitId" = m.new_id
        FROM fits_uuid_map AS m
        WHERE f."fitId"::text = m.old_id
        """
    )

    op.execute(
        """
        CREATE TEMP TABLE user_clothes_uuid_map AS
        SELECT DISTINCT "userClothesId"::text AS old_id, gen_random_uuid()::text AS new_id
        FROM user_clothes
        WHERE "userClothesId" IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE user_clothes AS u
        SET "userClothesId" = m.new_id
        FROM user_clothes_uuid_map AS m
        WHERE u."userClothesId"::text = m.old_id
        """
    )

    op.execute(
        """
        CREATE TEMP TABLE fit_clothes_uuid_map AS
        SELECT DISTINCT "fitClothesId"::text AS old_id, gen_random_uuid()::text AS new_id
        FROM fit_clothes
        WHERE "fitClothesId" IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE fit_clothes AS f
        SET "fitClothesId" = m.new_id
        FROM fit_clothes_uuid_map AS m
        WHERE f."fitClothesId"::text = m.old_id
        """
    )

    # 3. Convert tables to UUID
    op.execute('ALTER TABLE users ALTER COLUMN "userId" TYPE UUID USING "userId"::uuid')
    op.execute('ALTER TABLE fits ALTER COLUMN "fitId" TYPE UUID USING "fitId"::uuid')
    op.execute('ALTER TABLE fits ALTER COLUMN "userId" TYPE UUID USING "userId"::uuid')
    op.execute(
        'ALTER TABLE user_clothes ALTER COLUMN "userClothesId" TYPE UUID USING "userClothesId"::uuid'
    )
    op.execute(
        'ALTER TABLE user_clothes ALTER COLUMN "userId" TYPE UUID USING "userId"::uuid'
    )
    op.execute(
        'ALTER TABLE fit_clothes ALTER COLUMN "fitClothesId" TYPE UUID USING "fitClothesId"::uuid'
    )
    op.execute('ALTER TABLE fit_clothes ALTER COLUMN "fitId" TYPE UUID USING "fitId"::uuid')

    op.execute('ALTER TABLE users ALTER COLUMN "userId" SET DEFAULT gen_random_uuid()')
    op.execute('ALTER TABLE fits ALTER COLUMN "fitId" SET DEFAULT gen_random_uuid()')
    op.execute('ALTER TABLE user_clothes ALTER COLUMN "userClothesId" SET DEFAULT gen_random_uuid()')
    op.execute('ALTER TABLE fit_clothes ALTER COLUMN "fitClothesId" SET DEFAULT gen_random_uuid()')

    # 4. RECREATE CONSTRAINTS
    op.create_foreign_key(
        "user_clothes_userId_fkey", "user_clothes", "users", ["userId"], ["userId"]
    )
    op.create_foreign_key("fits_userId_fkey", "fits", "users", ["userId"], ["userId"])
    op.create_foreign_key(
        "fit_clothes_fitId_fkey", "fit_clothes", "fits", ["fitId"], ["fitId"]
    )

    # 5. CLEANUP INDEXES (Alembic auto-gen was right about these)
    op.drop_index("ix_fit_clothes_fitClothesId", table_name="fit_clothes")
    op.drop_index("ix_fits_fitId", table_name="fits")
    op.drop_index("ix_user_clothes_userClothesId", table_name="user_clothes")
    op.drop_index("ix_users_userId", table_name="users")


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_users_userId", "users", ["userId"], unique=False)
    op.alter_column(
        "users",
        "userId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.create_index(
        "ix_user_clothes_userClothesId", "user_clothes", ["userClothesId"], unique=False
    )
    op.alter_column(
        "user_clothes",
        "userId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "user_clothes",
        "userClothesId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.create_index("ix_fits_fitId", "fits", ["fitId"], unique=False)
    op.alter_column(
        "fits",
        "userId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "fits",
        "fitId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.create_index(
        "ix_fit_clothes_fitClothesId", "fit_clothes", ["fitClothesId"], unique=False
    )
    op.alter_column(
        "fit_clothes",
        "fitId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "fit_clothes",
        "fitClothesId",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
