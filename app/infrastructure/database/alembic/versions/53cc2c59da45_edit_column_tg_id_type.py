"""edit column `tg_id` type

Revision ID: 53cc2c59da45
Revises: c410d49a8acb
Create Date: 2022-06-22 16:36:20.492077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53cc2c59da45'
down_revision = 'c410d49a8acb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'tg_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)
    op.alter_column('views', 'user_tg_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('views', 'user_tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('users', 'tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
