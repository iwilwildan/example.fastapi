"""add content column to table posts

Revision ID: 3a624567f09c
Revises: 032c2695a863
Create Date: 2021-11-25 09:02:16.616258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a624567f09c'
down_revision = '032c2695a863'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
