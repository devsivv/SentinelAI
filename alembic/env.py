"""
alembic/env.py — Alembic migration environment for SentinelAI.

Configuration decisions
-----------------------
* DATABASE_URL is read from ``core.config.app_config`` (which sources it from
  the ``.env`` file or environment variable).  Credentials are never stored in
  ``alembic.ini``.
* ``target_metadata`` is wired to ``Base.metadata`` so that ``alembic revision
  --autogenerate`` can detect schema changes once ORM models are added in
  Phase 1.2.
* The project's own ``engine`` from ``backend.db`` is reused in online mode so
  that pool settings, dialect, and SSL configuration stay in one place.
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path when Alembic is run from the command
# line (e.g. ``alembic revision --autogenerate``).
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent.parent  # project root
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# ---------------------------------------------------------------------------
# Project imports — must come after the sys.path adjustment above.
# ---------------------------------------------------------------------------
from backend.db.base import Base  # noqa: E402
from backend.db.database import engine  # noqa: E402
import backend.models  # noqa: F401, E402 — register ORM models with Base.metadata

# ---------------------------------------------------------------------------
# Alembic Config object — provides access to alembic.ini values.
# ---------------------------------------------------------------------------
config = context.config

# ---------------------------------------------------------------------------
# Set up Python logging from alembic.ini (formatters, handlers).
# ---------------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# target_metadata — wired to Base.metadata for autogenerate support.
# Phase 1.2 will register ORM models against Base; at that point
# ``alembic revision --autogenerate`` will detect them automatically.
# ---------------------------------------------------------------------------
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Migration runners
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generate SQL without a live DB).

    Useful for reviewing migration SQL before applying it, or for environments
    where a direct database connection is unavailable.

    Uses ``engine.url`` directly to avoid configparser percent-interpolation
    issues that arise when passwords contain ``%``-encoded characters.
    """
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (apply directly to the database).

    Reuses the project's shared engine (with its pool and dialect settings)
    rather than creating a second engine from config, to ensure consistency.
    Credentials are sourced from ``core.config.app_config`` — never from
    ``alembic.ini``.
    """
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # compare_type=True enables detection of column type changes during
            # autogenerate.  Enable in Phase 1.3 when the first migration is created.
            compare_type=False,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
