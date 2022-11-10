"""empty message

Revision ID: 03af7e0f1e95
Revises: 
Create Date: 2022-11-10 09:43:48.727343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03af7e0f1e95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('restaurant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('restaurant_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('street_address', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='restaurant_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('review',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('restaurant', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_name', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('review_text', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('review_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], name='review_restaurant_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='review_pkey')
    )
    # ### end Alembic commands ###
