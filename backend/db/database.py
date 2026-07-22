"""
backend/db/database.py — SQLAlchemy engine configuration for SentinelAI.

Reads DATABASE_URL from ``core.config.app_config`` (which loads it from the
``.env`` file / environment) and creates a production-ready engine.

Design decisions
----------------
* ``app_config.database_url`` is a ``pydantic.SecretStr``; we call
  ``.get_secret_value()`` exactly once, here, so the raw URL never leaks into
  logs or repr elsewhere.
* ``make_url()`` is used for lightweight URL validation.  SQLAlchemy raises a
  clear ``ArgumentError`` on a malformed connection string before any network
  call is made.
* The engine object is the only object exported from this module.  The raw URL
  string is intentionally kept private (not re-exported).
"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url

from core.config import app_config


def _build_engine() -> Engine:
    """Construct and validate the SQLAlchemy engine.

    Returns:
        Engine: A configured SQLAlchemy engine ready for use.

    Raises:
        sqlalchemy.exc.ArgumentError: If DATABASE_URL is syntactically invalid.
        pydantic.ValidationError: If ``database_url`` was not set and the
            placeholder fails validation (should not happen with the provided
            default, but will fail at connection time if credentials are wrong).
    """
    raw_url: str = app_config.database_url.get_secret_value()

    # make_url() validates the connection string structure and raises a clear
    # ArgumentError immediately if the URL is malformed — before any TCP
    # connection attempt is made.  This is preferable to discovering a bad URL
    # only at the first request.
    url = make_url(raw_url)

    return create_engine(
        url,
        # -----------------------------------------------------------------
        # Connection pool — tuned for a single-process FastAPI application.
        # Adjust pool_size / max_overflow for higher-concurrency deployments.
        # -----------------------------------------------------------------
        pool_size=10,       # persistent connections kept open
        max_overflow=20,    # additional connections allowed under burst load
        pool_timeout=30,    # seconds to wait for a connection from the pool
        pool_recycle=1800,  # recycle connections every 30 min (avoids stale TCP)
        pool_pre_ping=True, # test each connection before use (handles DB restarts)
        echo=False,         # set True locally to log all SQL statements
    )


engine: Engine = _build_engine()
