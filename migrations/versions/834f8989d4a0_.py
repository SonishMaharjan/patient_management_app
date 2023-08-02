"""empty message

Revision ID: 834f8989d4a0
Revises: 92ac14847416
Create Date: 2023-08-02 18:36:58.296154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '834f8989d4a0'
down_revision = '92ac14847416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=80), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###