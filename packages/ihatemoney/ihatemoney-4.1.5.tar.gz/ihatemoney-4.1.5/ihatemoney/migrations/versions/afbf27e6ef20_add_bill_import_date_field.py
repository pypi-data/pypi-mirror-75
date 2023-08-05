"""add bill.import_date field

Revision ID: afbf27e6ef20
Revises: b78f8a8bdb16
Create Date: 2018-02-19 20:29:26.286136

"""

# revision identifiers, used by Alembic.
revision = 'afbf27e6ef20'
down_revision = 'b78f8a8bdb16'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bill', sa.Column('creation_date', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bill', 'creation_date')
    ### end Alembic commands ###
