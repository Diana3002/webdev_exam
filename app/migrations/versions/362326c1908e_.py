"""empty message

Revision ID: 362326c1908e
Revises: 7060385bac8e
Create Date: 2024-06-13 21:22:40.612763

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '362326c1908e'
down_revision = '7060385bac8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.drop_column('rating_count')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating_count', mysql.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
