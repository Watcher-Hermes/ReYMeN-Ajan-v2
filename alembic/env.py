"""alembic/env.py — ReYMeN çoklu DB migration desteği."""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, text

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata (auto-migration için boş — manual migration kullanıyoruz)
target_metadata = None

# Kayıtlı database'ler
DATABASES = {
    "session": "sqlite:///./.ReYMeN/session.db",
    "self_improve": "sqlite:///./reymen/sistem/self_improve.db",
    "hata_toplama": "sqlite:///./reymen/sistem/hata_toplama.db",
    "ogrenmeler": "sqlite:///./reymen/cereyan/ogrenmeler.db",
}


def run_migrations_offline() -> None:
    """Offline migration: SQL script üret, direkt DB'ye uygulama."""
    for db_name, url in DATABASES.items():
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            version_table=f"alembic_version_{db_name}",
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """Online migration: doğrudan DB'ye uygula."""
    connectable = config.attributes.get("connection")
    if connectable is None:
        # Default: session.db
        url = config.get_main_option("sqlalchemy.url")
        connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_session",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
