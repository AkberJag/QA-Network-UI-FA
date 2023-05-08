"""add_ip_addresses_table

Revision ID: 0eece5f8471e
Revises: fbfab97f1fa9
Create Date: 2023-05-06 01:23:59.595437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eece5f8471e'
down_revision = 'fbfab97f1fa9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ipaddresss',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pc_name', sa.String(), nullable=True),
    sa.Column('ip_address', sa.String(), nullable=True),
    sa.Column('network_template_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['network_template_id'], ['networktemplates.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip_address'),
    sa.UniqueConstraint('pc_name')
    )
    with op.batch_alter_table('ipaddresss', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ipaddresss_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ipaddresss', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ipaddresss_id'))

    op.drop_table('ipaddresss')
    # ### end Alembic commands ###