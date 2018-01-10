"""empty message

Revision ID: a940e55013f6
Revises: 1edd13c438e5
Create Date: 2018-01-10 16:19:27.466000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a940e55013f6'
down_revision = '1edd13c438e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('body', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'body')
    # ### end Alembic commands ###
