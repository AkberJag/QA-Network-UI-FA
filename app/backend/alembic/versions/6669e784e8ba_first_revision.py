"""first_revision

Revision ID: 6669e784e8ba
Revises: 
Create Date: 2023-04-29 19:39:46.241255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6669e784e8ba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """create the 'users' table"""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("email", sa.String(), unique=True, index=True),
        sa.Column("hashed_password", sa.String()),
    )


def downgrade() -> None:
    """drop the 'users' table"""
    op.drop_table("users")
