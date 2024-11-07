"""Make num unique and add check constraint

Revision ID: ae01315651e6
Revises: 2eff98ef457f
Create Date: 2024-11-07 12:21:11.001090

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ae01315651e6"
down_revision: Union[str, None] = "2eff98ef457f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_tables_num", "tables", ["num"])

    op.create_check_constraint(
        "check_guests_now_less_than_or_equal_to_max_guests",
        "tables",
        "guests_now <= max_guests",
    )


def downgrade() -> None:
    op.drop_constraint("uq_tables_num", "tables", type_="unique")
    op.drop_constraint(
        "check_guests_now_less_than_or_equal_to_max_guests", "tables", type_="check"
    )
