"""auto votes

Revision ID: 41e34cf8d90a
Revises: 29d100e4877d
Create Date: 2025-10-05 11:59:37.861715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41e34cf8d90a'
down_revision = '29d100e4877d'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('votes', 
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )


def downgrade():
    op.drop_table('votes')
