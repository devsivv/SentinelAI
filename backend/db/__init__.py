"""
backend/db — Database infrastructure package for SentinelAI.

Public exports
--------------
Base         — Shared SQLAlchemy ``DeclarativeBase``.  All ORM models inherit
               from this class (introduced in Phase 1.2).
engine       — Project-wide SQLAlchemy ``Engine`` instance.
SessionLocal — ``sessionmaker`` factory for creating ORM sessions.
get_db       — FastAPI dependency that yields a per-request ``Session`` and
               guarantees cleanup.

Internal
--------
The raw DATABASE_URL string is intentionally *not* exported from this package.
It is an implementation detail of ``backend.db.database`` and contains
credentials.  Import ``engine`` if you need the live database connection.
"""

from backend.db.base import Base
from backend.db.database import engine
from backend.db.session import SessionLocal, get_db

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
]
