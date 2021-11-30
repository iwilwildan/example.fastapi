"""add foreignkey to posts table

Revision ID: e7949c46834d
Revises: aa7b3fe21ff8
Create Date: 2021-11-26 09:34:01.790743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7949c46834d'
down_revision = 'aa7b3fe21ff8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table= "users",
        local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
