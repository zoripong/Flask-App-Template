import os
import sys
from logging.config import fileConfig

from alembic import context

from sqlalchemy import engine_from_config
from sqlalchemy import pool

sys.path.insert(0, os.getcwd())
from app.orm import Base, import_all_modules  # noqa -- 현재 경로 찾을 수 있도록 실행 후 Import

config = context.config
fileConfig(config.config_file_name)

# for 'autogenerate' configuration
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


import_all_modules()  # --autogenerate 를 위해 모든 모듈을 import 합니다.

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
