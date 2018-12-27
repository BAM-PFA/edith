"""empty message

Revision ID: b1ddfc575736
Revises: 
Create Date: 2018-12-27 14:33:12.460246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ddfc575736'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dbName', sa.String(length=60), nullable=True),
    sa.Column('fmpLayout', sa.String(length=60), nullable=True),
    sa.Column('IPaddress', sa.String(length=60), nullable=True),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('credentials', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('IPaddress'),
    sa.UniqueConstraint('credentials'),
    sa.UniqueConstraint('dbName'),
    sa.UniqueConstraint('fmpLayout'),
    sa.UniqueConstraint('name')
    )
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('paths',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullPath', sa.String(length=60), nullable=True),
    sa.Column('IPaddress', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('IPaddress'),
    sa.UniqueConstraint('fullPath')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('RSusername', sa.String(length=60), nullable=True),
    sa.Column('RSkey', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_RSkey'), 'users', ['RSkey'], unique=True)
    op.create_index(op.f('ix_users_RSusername'), 'users', ['RSusername'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_RSusername'), table_name='users')
    op.drop_index(op.f('ix_users_RSkey'), table_name='users')
    op.drop_table('users')
    op.drop_table('paths')
    op.drop_table('departments')
    op.drop_table('data_sources')
    # ### end Alembic commands ###
