"""create posts table

Revision ID: 78db950f476d
Revises: 
Create Date: 2025-10-04 19:41:59.247719

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '78db950f476d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False))

def downgrade():
    op.drop_table('posts')
    
