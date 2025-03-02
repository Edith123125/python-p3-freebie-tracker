from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'd236154c1086'
down_revision = 'a9392bc9699d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    
    # Create 'company_dev' table if it doesn't exist
    if 'company_dev' not in inspector.get_table_names():
        op.create_table('company_dev',
                        sa.Column('company_id', sa.Integer(), nullable=False),
                        sa.Column('dev_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name=op.f('fk_company_dev_company_id_companies')),
                        sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], name=op.f('fk_company_dev_dev_id_devs')),
                        sa.PrimaryKeyConstraint('company_id', 'dev_id')
        )
    
    # Workaround for SQLite: Recreate 'freebies' table with the correct constraints
    op.create_table('freebies_new',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('item_name', sa.String(), nullable=False),  # Enforce NOT NULL
        sa.Column('value', sa.Integer(), nullable=False),  # Enforce NOT NULL
        sa.Column('dev_id', sa.Integer(), sa.ForeignKey('devs.id')),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'))
    )

    # Copy data from old table
    op.execute("""
        INSERT INTO freebies_new (id, item_name, value, dev_id, company_id)
        SELECT id, item_name, value, dev_id, company_id FROM freebies
    """)

    # Drop old table and rename new table
    op.drop_table('freebies')
    op.rename_table('freebies_new', 'freebies')


def downgrade() -> None:
    # Reverse the process in downgrade
    op.create_table('freebies_old',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('item_name', sa.String(), nullable=True),  # Allow NULL again
        sa.Column('value', sa.Integer(), nullable=True),
        sa.Column('dev_id', sa.Integer(), sa.ForeignKey('devs.id')),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'))
    )

    op.execute("""
        INSERT INTO freebies_old (id, item_name, value, dev_id, company_id)
        SELECT id, item_name, value, dev_id, company_id FROM freebies
    """)

    op.drop_table('freebies')
    op.rename_table('freebies_old', 'freebies')
