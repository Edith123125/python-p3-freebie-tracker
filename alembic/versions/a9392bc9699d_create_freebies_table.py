from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'a9392bc9699d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Get the current database connection and inspector
    bind = op.get_bind()
    inspector = inspect(bind)

    # Check if 'companies' table already exists
    if 'companies' not in inspector.get_table_names():
        op.create_table('companies',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('founding_year', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Check if 'devs' table already exists
    if 'devs' not in inspector.get_table_names():
        op.create_table('devs',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    # Check if 'freebies' table already exists
    if 'freebies' not in inspector.get_table_names():
        op.create_table('freebies',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('item_name', sa.String(), nullable=True),
            sa.Column('value', sa.Integer(), nullable=True),
            sa.Column('company_id', sa.Integer(), nullable=True),
            sa.Column('dev_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
            sa.ForeignKeyConstraint(['dev_id'], ['devs.id']),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade() -> None:
    # Get the current database connection and inspector
    bind = op.get_bind()
    inspector = inspect(bind)

    # Only drop the table if it exists
    if 'freebies' in inspector.get_table_names():
        op.drop_table('freebies')

    if 'devs' in inspector.get_table_names():
        op.drop_table('devs')

    if 'companies' in inspector.get_table_names():
        op.drop_table('companies')
