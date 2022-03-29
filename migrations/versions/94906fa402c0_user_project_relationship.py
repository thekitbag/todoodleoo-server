"""user project relationship

Revision ID: 94906fa402c0
Revises: 
Create Date: 2022-02-08 21:08:53.962053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94906fa402c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'project', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'user_id')
    # ### end Alembic commands ###