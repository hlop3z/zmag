"""empty message

Revision ID: d245cbed3ca7
Revises: 
Create Date: 2023-11-01 22:06:08.229082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd245cbed3ca7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zmag_author',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('_id'),
    sa.UniqueConstraint('first_name')
    )
    op.create_table('zmag_book',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('meta', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('zmag_book')
    op.drop_table('zmag_author')
    # ### end Alembic commands ###
