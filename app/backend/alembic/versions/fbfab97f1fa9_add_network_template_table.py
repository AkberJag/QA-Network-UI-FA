"""add_network_template_table

Revision ID: fbfab97f1fa9
Revises: 6669e784e8ba
Create Date: 2023-05-05 04:37:15.619276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbfab97f1fa9'
down_revision = '6669e784e8ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('networktemplates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('network_template_name', sa.String(), nullable=True),
    sa.Column('cidr_notation', sa.String(), nullable=True),
    sa.Column('bandwidth_restriction_upload', sa.Float(), nullable=True),
    sa.Column('bandwidth_restriction_download', sa.Float(), nullable=True),
    sa.Column('dns_latency', sa.Float(), nullable=True),
    sa.Column('general_latency', sa.Float(), nullable=True),
    sa.Column('packet_loss', sa.Float(), nullable=True),
    sa.Column('no_of_pcs', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('network_template_name')
    )
    with op.batch_alter_table('networktemplates', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_networktemplates_id'), ['id'], unique=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('networktemplates', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_networktemplates_id'))

    op.drop_table('networktemplates')
    # ### end Alembic commands ###
