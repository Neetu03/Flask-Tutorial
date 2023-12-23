"""added about author

Revision ID: 29bb4459a787
Revises: 69a03129bf82
Create Date: 2023-12-02 02:48:16.050630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29bb4459a787'
down_revision = '69a03129bf82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_author', sa.Text(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('about_author')

    # ### end Alembic commands ###
