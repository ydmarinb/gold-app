"""empty message

Revision ID: 4e68329400c0
Revises: 982e45225993
Create Date: 2020-08-04 15:19:15.069331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e68329400c0'
down_revision = '982e45225993'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detalle_compra', sa.Column('vrGramos', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('detalle_compra', 'vrGramos')
    # ### end Alembic commands ###