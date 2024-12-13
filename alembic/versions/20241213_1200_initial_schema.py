"""Initial schema

Revision ID: initial_schema
Create Date: 2024-12-13 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Research Jobs table
    op.create_table(
        'research_jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('company_url', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('progress', sa.Float(), nullable=False),
        sa.Column('result', postgresql.JSONB(), nullable=True),
        sa.Column('error', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  onupdate=sa.text('now()')),
        sa.Column('cache_valid_until', sa.DateTime(timezone=True)),
        sa.Column('version', sa.Integer(), default=1),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index(op.f('ix_research_jobs_company_url'),
                    'research_jobs', ['company_url'])
    op.create_index(op.f('ix_research_jobs_status'),
                    'research_jobs', ['status'])
    op.create_index(op.f('ix_research_jobs_created_at'),
                    'research_jobs', ['created_at'])

    # Research Cache table
    op.create_table(
        'research_cache',
        sa.Column('company_url', sa.String(), nullable=False),
        sa.Column('crawl_data', postgresql.JSONB(), nullable=True),
        sa.Column('analyzed_data', postgresql.JSONB(), nullable=True),
        sa.Column('enriched_data', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  onupdate=sa.text('now()')),
        sa.Column('cache_valid_until', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('company_url')
    )

    # API Usage tracking
    op.create_table(
        'api_key_usage',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('api_key', sa.String(), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True),
                  server_default=sa.text('now()')),
        sa.Column('response_time', sa.Float(), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_api_key_usage_api_key'),
                    'api_key_usage', ['api_key'])
    op.create_index(op.f('ix_api_key_usage_timestamp'),
                    'api_key_usage', ['timestamp'])


def downgrade() -> None:
    op.drop_table('api_key_usage')
    op.drop_table('research_cache')
    op.drop_table('research_jobs')