"""create_users_table

Revision ID: 8c4ef4505c22
Revises: 163374e87166
Create Date: 2024-08-28 16:10:24.791929

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.configs.app_settings import bcrypt_context, app_settings

# revision identifiers, used by Alembic.
revision: str = "8c4ef4505c22"
down_revision: Union[str, None] = "163374e87166"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        "fk_users_companies_company_id", "users", "companies", ["company_id"], ["id"]
    )
    hashed_default_user_password = bcrypt_context.hash(
        app_settings.DEFAULT_USER_PASSWORD
    )
    op.bulk_insert(
        users_table,
        [
            {
                "id": "8d6e8f4c-3121-42ef-8ee7-e700fd121f8a",
                "username": "admin",
                "email": "admin@local.com",
                "hashed_password": hashed_default_user_password,
                "is_active": True,
                "is_admin": True,
                "first_name": "Admin",
                "last_name": "Local",
                "company_id": "3a388e09-7d0e-4460-9c48-698e0211694e",
            },
            {
                "id": "7557b36f-9949-4e61-a923-b22d75896cb4",
                "username": "user",
                "email": "user@local.com",
                "hashed_password": hashed_default_user_password,
                "is_active": True,
                "is_admin": False,
                "first_name": "User",
                "last_name": "Local",
                "company_id": "3a388e09-7d0e-4460-9c48-698e0211694e",
            },
            {
                "id": "7557b36f-9949-4e61-a923-b22d75896cb5",
                "username": "string",
                "email": "string@local.com",
                "hashed_password": hashed_default_user_password,
                "is_active": True,
                "is_admin": True,
                "first_name": "String",
                "last_name": "Local",
                "company_id": "3a388e09-7d0e-4460-9c48-698e0211694e",
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_users_companies_company_id", "users", type_="foreignkey")
    op.execute("DROP TABLE users")
    # ### end Alembic commands ###
