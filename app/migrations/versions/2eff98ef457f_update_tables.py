from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2eff98ef457f"
down_revision: Union[str, None] = "9b3559dff4dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tables", sa.Column("guests_def", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE tables
        SET guests_def = (
            SELECT COUNT(*) FROM guest_lists WHERE guest_lists.table_id = tables.id
        );
        """
    )

    op.add_column("tables", sa.Column("guests_now", sa.Integer(), nullable=True))
    op.execute(
        """
        UPDATE tables
        SET guests_now = (
            SELECT COUNT(*) FROM guest_lists
            WHERE guest_lists.table_id = tables.id AND guest_lists.is_present = TRUE
        );
        """
    )

    op.alter_column("tables", "guests_def", nullable=False)
    op.alter_column("tables", "guests_now", nullable=False)

    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_guest_counts() RETURNS TRIGGER AS $$
        BEGIN
            UPDATE tables
            SET guests_def = (
                SELECT COUNT(*)
                FROM guest_lists
                WHERE guest_lists.table_id = NEW.table_id
            ),
            guests_now = (
                SELECT COUNT(*)
                FROM guest_lists
                WHERE guest_lists.table_id = NEW.table_id AND guest_lists.is_present = TRUE
            )
            WHERE tables.id = NEW.table_id;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER guest_counts_trigger
        AFTER INSERT OR UPDATE OR DELETE ON guest_lists
        FOR EACH ROW EXECUTE FUNCTION update_guest_counts();
        """
    )



def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS guest_counts_trigger ON guest_lists;")
    op.execute("DROP FUNCTION IF EXISTS update_guest_counts;")

    op.drop_column("tables", "guests_def")
    op.drop_column("tables", "guests_now")
