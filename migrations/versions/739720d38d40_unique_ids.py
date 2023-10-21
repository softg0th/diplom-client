"""unique ids

Revision ID: 739720d38d40
Revises: b9da8aa9ebf9
Create Date: 2023-10-21 04:40:45.113965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '739720d38d40'
down_revision: Union[str, None] = 'b9da8aa9ebf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
