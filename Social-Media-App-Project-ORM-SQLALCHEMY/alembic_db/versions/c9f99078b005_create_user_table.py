"""create user table

Revision ID: c9f99078b005
Revises: 363f2d80c2bb
Create Date: 2025-10-04 22:40:42.039989

"""
from alembic import op
import sqlalchemy as sa
# from sqlalchemy.sql.sqltypes import TIMESTAMP

# revision identifiers, used by Alembic.
revision = 'c9f99078b005'
down_revision = '363f2d80c2bb'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True), 
                  nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at',sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

def downgrade():
    op.drop_table('users')
