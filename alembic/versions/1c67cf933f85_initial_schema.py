"""initial_schema — ReYMeN ana veritabanlari ilk schema.

Revision ID: 1c67cf933f85
Revises: None
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "1c67cf933f85"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Session DB — tüm tablolar (FTS5 + trigram ile)."""
    # ── sessions ──
    op.create_table(
        "sessions",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("profile", sa.Text(), nullable=False, server_default="default"),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("created_at", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.Text(), nullable=True),
        sa.Column("message_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("token_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("turn_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("tool_call_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("archived", sa.Integer(), nullable=True, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ── session_messages ──
    op.create_table(
        "session_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Text(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("created_at", sa.Text(), nullable=True),
        sa.Column("turn_index", sa.Integer(), nullable=True),
        sa.Column("tool_calls", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # session_messages FTS5 (manuel)
    op.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS session_messages_fts "
        "USING fts5(content, content=session_messages, content_rowid=id)"
    )
    op.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS session_messages_trigram "
        "USING fts5(content, tokenize='trigram', content=session_messages, content_rowid=id)"
    )
    # ── session_tool_calls ──
    op.create_table(
        "session_tool_calls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Text(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=True),
        sa.Column("tool_name", sa.Text(), nullable=True),
        sa.Column("arguments", sa.Text(), nullable=True),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("status", sa.Text(), nullable=True, server_default="success"),
        sa.Column("created_at", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ── ajan_gunlugu ──
    op.create_table(
        "ajan_gunlugu",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Text(), nullable=True),
        sa.Column("olay", sa.Text(), nullable=True),
        sa.Column("detay", sa.Text(), nullable=True),
        sa.Column("zaman", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ajan_gunlugu FTS5
    op.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS ajan_gunlugu_fts "
        "USING fts5(detay, content=ajan_gunlugu, content_rowid=id)"
    )
    op.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS ajan_gunlugu_trigram "
        "USING fts5(detay, tokenize='trigram', content=ajan_gunlugu, content_rowid=id)"
    )


def downgrade() -> None:
    """Tablolari geri al."""
    op.drop_table("sessions")
    op.execute("DROP TABLE IF EXISTS session_messages_fts")
    op.execute("DROP TABLE IF EXISTS session_messages_trigram")
    op.drop_table("session_messages")
    op.drop_table("session_tool_calls")
    op.execute("DROP TABLE IF EXISTS ajan_gunlugu_fts")
    op.execute("DROP TABLE IF EXISTS ajan_gunlugu_trigram")
    op.drop_table("ajan_gunlugu")
