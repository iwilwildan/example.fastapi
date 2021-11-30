"""add last few columns to posts table

Revision ID: 9f6dac1d5d49
Revises: e7949c46834d
Create Date: 2021-11-26 09:40:06.542774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f6dac1d5d49'
down_revision = 'e7949c46834d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_time')
    pass
