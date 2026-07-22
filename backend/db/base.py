"""
backend/db/base.py — Shared Declarative Base for SentinelAI ORM models.

All future SQLAlchemy ORM models should inherit from this Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative Base class for all SQLAlchemy ORM models."""

    pass
