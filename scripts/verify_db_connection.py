#!/usr/bin/env python3
"""
scripts/verify_db_connection.py — PostgreSQL connectivity verification for SentinelAI.

Executes ``SELECT 1`` via the project's SQLAlchemy engine and reports
success or failure.

Usage (from project root)::

    python scripts/verify_db_connection.py

Exit codes:
    0 — connection succeeded
    1 — connection failed
"""

import sys
from pathlib import Path

# Ensure the project root is on sys.path when the script is run directly
# (i.e. ``python scripts/verify_db_connection.py``).
# When invoked as a module (``python -m scripts.verify_db_connection``) this
# is not needed, but the guard makes both invocations work.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from sqlalchemy import text  # noqa: E402 — import after sys.path adjustment

from backend.db import engine  # noqa: E402


def verify_connection() -> bool:
    """Attempt to connect to PostgreSQL and execute ``SELECT 1``.

    Returns:
        bool: ``True`` if the connection and query succeed, ``False`` otherwise.
    """
    print("Connecting to database...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("SUCCESS: PostgreSQL connection verified (SELECT 1 -> 1).")
                return True
            print(f"FAILED: Unexpected query result: {result!r}")
            return False
    except Exception as exc:  # noqa: BLE001 — intentional catch-all for user-facing output
        print(f"ERROR: Could not connect to the database.\n  {exc}")
        return False


if __name__ == "__main__":
    sys.exit(0 if verify_connection() else 1)
