"""Add metrics tables

Revision ID: add_metrics_tables
Create Date: 2024-12-13 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_metrics_tables'
down_revision = 'initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Service Metrics table
    op.create_table(
        'service_metrics',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('service_name', sa.String(), nullable=False),
        sa.Column('request_count', sa.Integer(), nullable=False, default=0),
        sa.Column('success_count', sa.Integer(), nullable=False, default=0),
        sa.Column('error_count', sa.Integer(), nullable=False, default=0),
        sa.Column('total_response_time', sa.Float(), nullable=False, default=0),
        sa.Column('timestamp', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_service_metrics_service_name'),
                    'service_metrics', ['service_name'])
    op.create_index(op.f('ix_service_metrics_timestamp'),
                    'service_metrics', ['timestamp'])

    # System Metrics table
    op.create_table(
        'system_metrics',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cpu_usage', sa.Float(), nullable=False),
        sa.Column('memory_usage', sa.BigInteger(), nullable=False),
        sa.Column('disk_usage', sa.Float(), nullable=False),
        sa.Column('queue_size', sa.Integer(), nullable=False),
        sa.Column('active_workers', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_system_metrics_timestamp'),
                    'system_metrics', ['timestamp'])


def downgrade() -> None:
    op.drop_table('system_metrics')
    op.drop_table('service_metrics')