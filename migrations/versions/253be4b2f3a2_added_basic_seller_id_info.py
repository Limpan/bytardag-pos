"""Added basic seller-ID info.

Revision ID: 253be4b2f3a2
Revises: 864194dc07a1
Create Date: 2020-09-08 21:14:51.676787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "253be4b2f3a2"
down_revision = "864194dc07a1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "seller",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("seller_id", sa.String(length=4), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("seller", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_seller_seller_id"), ["seller_id"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("seller", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_seller_seller_id"))

    op.drop_table("seller")
    # ### end Alembic commands ###
