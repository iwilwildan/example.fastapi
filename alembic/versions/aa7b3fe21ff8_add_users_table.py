"""add users table

Revision ID: aa7b3fe21ff8
Revises: 3a624567f09c
Create Date: 2021-11-25 09:06:23.796112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa7b3fe21ff8'
down_revision = '3a624567f09c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_time', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable= False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
