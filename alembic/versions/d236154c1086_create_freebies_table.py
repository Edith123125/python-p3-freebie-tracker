from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'd236154c1086'
down_revision = 'a9392bc9699d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Use SQLAlchemy's inspection system to check if the table already exists
    bind = op.get_bind()
    inspector = inspect(bind)
    
    if 'company_dev' not in inspector.get_table_names():
        op.create_table('company_dev',
                        sa.Column('company_id', sa.Integer(), nullable=False),
                        sa.Column('dev_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name=op.f('fk_company_dev_company_id_companies')),
                        sa.ForeignKeyConstraint(['dev_id'], ['devs.id'], name=op.f('fk_company_dev_dev_id_devs')),
                        sa.PrimaryKeyConstraint('company_id', 'dev_id')
        )
    
    # Make columns in the 'freebies' table non-nullable
    op.alter_column('freebies', 'item_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('freebies', 'value',
               existing_type=sa.INTEGER(),
               nullable=False)
