"""test

Revision ID: 6b893f4e8b5a
Revises: 980bba7643c5
Create Date: 2023-10-23 07:16:47.044959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b893f4e8b5a'
down_revision: Union[str, None] = '980bba7643c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
