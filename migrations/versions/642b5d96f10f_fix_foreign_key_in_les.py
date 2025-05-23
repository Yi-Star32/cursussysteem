"""Fix foreign key in Les

Revision ID: 642b5d96f10f
Revises: b65013e19bf5
Create Date: 2025-04-16 16:04:36.303139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642b5d96f10f'
down_revision = 'b65013e19bf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('les', schema=None) as batch_op:
        batch_op.drop_constraint('fk_les_inschrijving', type_='foreignkey')
        batch_op.drop_column('inschrijving_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('les', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inschrijving_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_les_inschrijving', 'inschrijving', ['inschrijving_id'], ['cursus_id'])

    # ### end Alembic commands ###
