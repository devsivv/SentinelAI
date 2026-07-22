"""
backend/db/session.py — SQLAlchemy Session management and FastAPI dependency.

Provides the ``SessionLocal`` session factory and the ``get_db`` generator
for managing database sessions within FastAPI request lifecycles.
"""

from collections.abc import Iterator

from sqlalchemy.orm import Session, sessionmaker

from backend.db.database import engine

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------
# ``autocommit=False``    — explicit transaction management; callers must commit.
# ``autoflush=False``     — prevents implicit flushes before queries, giving
#                           callers full control over when SQL is sent.
# ``expire_on_commit=False`` — ORM objects remain accessible after commit()
#                           without requiring a re-fetch.  Correct for the
#                           FastAPI request/response lifecycle where the session
#                           is closed at the end of the request.
SessionLocal = sessionmaker(
    engine,         # SQLAlchemy 2.x idiom: positional arg, not bind=engine
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Iterator[Session]:
    """FastAPI database session dependency.

    Yields a ``Session`` to route handlers and guarantees it is closed after
    the request completes — whether it succeeds or raises an exception.

    Usage in a route::

        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: An active SQLAlchemy ORM session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
