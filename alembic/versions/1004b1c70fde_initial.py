"""Initial

Revision ID: 1004b1c70fde
Revises: 
Create Date: 2023-05-21 04:17:32.729265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1004b1c70fde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('barsa',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('passport', sa.String(), nullable=True),
    sa.Column('nat', sa.String(), nullable=True),
    sa.Column('gunlic', sa.String(), nullable=True),
    sa.Column('crime', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_barsa_passport'), 'barsa', ['passport'], unique=False)
    op.create_table('user',
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_common', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index(op.f('ix_barsa_passport'), table_name='barsa')
    op.drop_table('barsa')
    # ### end Alembic commands ###
