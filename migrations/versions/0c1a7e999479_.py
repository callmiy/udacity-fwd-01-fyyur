"""empty message

Revision ID: 0c1a7e999479
Revises: a5eaaf63e139
Create Date: 2020-05-17 21:23:50.831961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0c1a7e999479"
down_revision = "a5eaaf63e139"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("venue", sa.Column("genres", sa.String(length=120), nullable=False))
    op.add_column("venue", sa.Column("seeking_description", sa.String(), nullable=True))
    op.add_column("venue", sa.Column("seeking_talent", sa.Boolean(), nullable=False))
    op.add_column("venue", sa.Column("website", sa.String(length=120), nullable=True))
    op.alter_column("venue", "name", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("venue", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("venue", "website")
    op.drop_column("venue", "seeking_talent")
    op.drop_column("venue", "seeking_description")
    op.drop_column("venue", "genres")
    # ### end Alembic commands ###