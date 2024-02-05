"""some changes

Revision ID: 9d4c71bd2a39
Revises: 8c71fa923d4c
Create Date: 2024-01-29 13:17:05.951264

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9d4c71bd2a39'
down_revision: str | None = '8c71fa923d4c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
                    existing_type=sa.DOUBLE_PRECISION(precision=53),
                    type_=sa.String(),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'price',
                    existing_type=sa.String(),
                    type_=sa.DOUBLE_PRECISION(precision=53),
                    existing_nullable=True)
    # ### end Alembic commands ###
