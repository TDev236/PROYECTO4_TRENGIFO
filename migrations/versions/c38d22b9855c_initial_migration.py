"""Initial migration

Revision ID: c38d22b9855c
Revises: 
Create Date: 2025-03-29 21:15:11.236265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c38d22b9855c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heladeria',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ventas_del_dia', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('precio_publico', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('producto_ingrediente',
    sa.Column('producto_id', sa.Integer(), nullable=False),
    sa.Column('ingrediente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ingrediente_id'], ['ingredientes.id'], ),
    sa.ForeignKeyConstraint(['producto_id'], ['productos.id'], ),
    sa.PrimaryKeyConstraint('producto_id', 'ingrediente_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('producto_ingrediente')
    op.drop_table('user')
    op.drop_table('productos')
    op.drop_table('heladeria')
    # ### end Alembic commands ###
