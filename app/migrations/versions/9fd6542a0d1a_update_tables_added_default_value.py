"""Update tables, added default value

Revision ID: 9fd6542a0d1a
Revises: 74a38b86317b
Create Date: 2024-11-06 13:24:16.852432

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9fd6542a0d1a"
down_revision: Union[str, None] = "74a38b86317b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tables", "guests_def", server_default=sa.text("0"))
    op.alter_column("tables", "guests_now", server_default=sa.text("0"))
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
