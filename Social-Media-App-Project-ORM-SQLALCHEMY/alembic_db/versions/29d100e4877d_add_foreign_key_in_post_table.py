"""add foreign key in post table

Revision ID: 29d100e4877d
Revises: c9f99078b005
Create Date: 2025-10-05 11:25:20.861474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29d100e4877d'
down_revision = 'c9f99078b005'
branch_labels = None
depends_on = None


def upgrade():
        op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
        op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("post_user_fk", table_name = "posts", type_ = "foreignkey")
    op.drop_column("posts",'owner_id')
        
