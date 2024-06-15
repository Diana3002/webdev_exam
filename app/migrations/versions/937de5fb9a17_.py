"""empty message

Revision ID: 937de5fb9a17
Revises: 5b22250a0788
Create Date: 2024-06-13 20:30:02.510731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937de5fb9a17'
down_revision = '5b22250a0788'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'cover', ['cover_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###