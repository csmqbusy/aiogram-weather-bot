"""add tables

Revision ID: 3045a3f2d9e1
Revises: 
Create Date: 2024-11-25 17:05:09.745979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3045a3f2d9e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('connection_date', sa.DateTime(), server_default=sa.text("TIMEZONE ('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weather_reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text("TIMEZONE ('utc', now())"), nullable=False),
    sa.Column('temp', sa.Float(), nullable=False),
    sa.Column('feels_like', sa.Float(), nullable=False),
    sa.Column('wind_speed', sa.Float(), nullable=False),
    sa.Column('pressure_mm', sa.Float(), nullable=False),
    sa.Column('visibility', sa.Float(), nullable=False),
    sa.Column('weather_condition', sa.String(), server_default='Данные отсутствуют', nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather_reports')
    op.drop_table('users')
    # ### end Alembic commands ###
