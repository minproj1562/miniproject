"""Make User.created_at/updated_at timezone‑aware

Revision ID: 2ac5e92bfdd5
Revises: 2d7e9018b3e9
Create Date: 2025-04-10 10:40:07.564740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ac5e92bfdd5'
down_revision = '2d7e9018b3e9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now()
        ))
        batch_op.add_column(sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now()
        ))

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
