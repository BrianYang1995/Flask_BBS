"""empty message

Revision ID: f5f14002e661
Revises: aa58b9aa8868
Create Date: 2018-12-03 20:34:59.768305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5f14002e661'
down_revision = 'aa58b9aa8868'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('author_id', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'posts', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    # ### end Alembic commands ###
