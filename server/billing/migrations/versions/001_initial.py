"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-19 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema."""
    # Create enum types
    op.execute("CREATE TYPE invoice_status AS ENUM ('PENDING', 'PAID', 'OVERDUE')")
    
    # Create invoices table
    op.create_table(
        'invoices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('status', postgresql.ENUM('PENDING', 'PAID', 'OVERDUE', name='invoice_status'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number')
    )
    
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_invoices_status', 'invoices', ['status'])
    op.create_index('ix_invoices_created_at', 'invoices', ['created_at'])
    op.create_index('ix_audit_logs_event_type', 'audit_logs', ['event_type'])
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])


def downgrade():
    """Downgrade database schema."""
    # Drop indexes
    op.drop_index('ix_audit_logs_timestamp')
    op.drop_index('ix_audit_logs_event_type')
    op.drop_index('ix_invoices_created_at')
    op.drop_index('ix_invoices_status')
    
    # Drop tables
    op.drop_table('audit_logs')
    op.drop_table('invoices')
    
    # Drop enum type
    op.execute('DROP TYPE invoice_status') 