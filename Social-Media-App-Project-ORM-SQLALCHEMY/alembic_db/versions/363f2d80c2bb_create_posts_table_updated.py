"""create posts table updated

Revision ID: 363f2d80c2bb
Revises: 78db950f476d
Create Date: 2025-10-04 21:42:01.361678

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = '363f2d80c2bb'
down_revision = '78db950f476d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(sa.Column('published', sa.BOOLEAN(), 
                                               nullable=False, server_default=text('TRUE')))
        batch_op.add_column(sa.Column('created_at',TIMESTAMP(timezone=True), 
                                               nullable=False, server_default=text('now()')))
        batch_op.add_column(sa.Column('updated_at',TIMESTAMP(timezone=True), 
                                      nullable=False, server_default=text('now()'), onupdate=func.now()))

def downgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('published')
        batch_op.drop_column('created_at')
        batch_op.drop_column('updated_at')
