"""file update

Revision ID: 980bba7643c5
Revises: 739720d38d40
Create Date: 2023-10-23 06:38:08.346892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '980bba7643c5'
down_revision: Union[str, None] = '739720d38d40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
