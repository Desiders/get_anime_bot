"""create tables

Revision ID: c410d49a8acb
Revises:
Create Date: 2022-06-22 13:21:36.554347

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c410d49a8acb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sources',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    sa.UniqueConstraint('url')
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('tg_id', sa.Integer(), nullable=False),
                    sa.Column('language_code', sa.String(), nullable=True),
                    sa.Column('show_nsfw', sa.Boolean(), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('tg_id')
                    )
    op.create_table('media',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('genre', sa.String(), nullable=True),
                    sa.Column('media_type', sa.String(), nullable=False),
                    sa.Column('is_sfw', sa.Boolean(), nullable=True),
                    sa.Column('source_id', sa.Integer(), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['source_id'], ['sources.id'],
                        onupdate='CASCADE',
                        ondelete='SET NULL',
                    ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('url', 'genre', 'media_type')
                    )
    op.create_table('views',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_tg_id', sa.Integer(), nullable=True),
                    sa.Column('media_id', sa.Integer(), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['media_id'], ['media.id'],
                        onupdate='CASCADE',
                        ondelete='SET NULL',
                    ),
                    sa.ForeignKeyConstraint(
                        ['user_tg_id'], ['users.tg_id'],
                        onupdate='CASCADE',
                        ondelete='CASCADE',
                    ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('views')
    op.drop_table('media')
    op.drop_table('users')
    op.drop_table('sources')
    # ### end Alembic commands ###
