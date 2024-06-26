"""empty message

Revision ID: e73053998bae
Revises: a9c12cf01e28
Create Date: 2024-06-15 20:30:22.130761

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e73053998bae'
down_revision = 'a9c12cf01e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'cover', ['cover_id'], ['id'])

    with op.batch_alter_table('cover', schema=None) as batch_op:
        batch_op.drop_constraint('cover_ibfk_1', type_='foreignkey')
        batch_op.drop_column('book_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cover', schema=None) as batch_op:
        batch_op.add_column(sa.Column('book_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('cover_ibfk_1', 'book', ['book_id'], ['id'])

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
