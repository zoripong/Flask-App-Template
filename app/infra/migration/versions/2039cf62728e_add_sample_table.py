"""add sample table

Revision ID: 2039cf62728e
Revises:
Create Date: 2021-06-12 13:40:13.612632

"""
from alembic import op

from sqlalchemy import Column, PrimaryKeyConstraint

from sqlalchemy_utils import UUIDType

# revision identifiers, used by Alembic.
revision = '2039cf62728e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sample',
        Column('id', UUIDType(), nullable=False, comment='ID'),
        PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sample')
