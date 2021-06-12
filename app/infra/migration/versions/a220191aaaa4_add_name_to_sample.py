"""add name to sample
Revision ID: a220191aaaa4
Revises: 2039cf62728e
Create Date: 2021-06-12 13:52:53.949264

"""
from alembic import op


# revision identifiers, used by Alembic.
from sqlalchemy import Column, String

revision = 'a220191aaaa4'
down_revision = '2039cf62728e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'sample',
        Column('name', String(), nullable=False, comment='이름'),
    )


def downgrade():
    op.drop_column('sample', 'name')
