"""empty message

Revision ID: 294b7aba4ef5
Revises: 335d1f79bfaa
Create Date: 2024-06-11 22:00:55.138927

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '294b7aba4ef5'
down_revision = '335d1f79bfaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint('book_ibfk_1', type_='foreignkey')
        batch_op.drop_column('id_cover')

    with op.batch_alter_table('cover', schema=None) as batch_op:
        batch_op.add_column(sa.Column('book_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'book', ['book_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cover', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('book_id')

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_cover', mysql.VARCHAR(length=100), nullable=True))
        batch_op.create_foreign_key('book_ibfk_1', 'cover', ['id_cover'], ['id'])

    # ### end Alembic commands ###
