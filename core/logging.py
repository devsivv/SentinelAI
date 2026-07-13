"""
core/logging.py — Shared logging factory for SentinelAI agents.

All three completed agents (currency, scam_comm, fraud) contained identical
logging setup code.  This module extracts that logic into a single
``build_agent_logger()`` factory so each agent delegates to one place.

Behaviour is identical to the previous per-agent implementations:
  - RotatingFileHandler writing to ``<log_dir>/<name>.log``
  - StreamHandler writing to stdout
  - Both handlers share the same format and level
  - Propagation to the root logger is suppressed
  - Handlers are only added once (guarded against double-registration)

Usage
-----
In each agent's ``logging.py``::

    from core.logging import build_agent_logger
    from .config import settings

    _LOGGER_NAME = "my_agent"
    build_agent_logger(_LOGGER_NAME, settings.log_dir, settings.log_level)

    def get_logger() -> logging.Logger:
        return logging.getLogger(_LOGGER_NAME)
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants shared across all agents
# ---------------------------------------------------------------------------

LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s"
_MAX_BYTES = 10 * 1024 * 1024  # 10 MiB per log file
_BACKUP_COUNT = 5


def build_agent_logger(
    name: str,
    log_dir: Path,
    level: str = "INFO",
) -> logging.Logger:
    """Create (or retrieve) a named logger with rotating-file + stdout handlers.

    This function is idempotent: if the named logger already has handlers
    registered it is returned immediately without adding duplicates.

    Parameters
    ----------
    name:
        Logger name — typically the agent identifier, e.g. ``"fraud_agent"``.
        This name is used for both ``logging.getLogger(name)`` and the log
        file ``<log_dir>/<name>.log``.
    log_dir:
        Directory where the rotating log file is created.  Created
        automatically (with ``parents=True``) if it does not already exist.
    level:
        Python logging level string (``"DEBUG"``, ``"INFO"``, etc.).
        Defaults to ``"INFO"``.  Invalid values fall back to ``INFO``.

    Returns
    -------
    ``logging.Logger``
        The configured logger.  Callers should cache the return value or
        call ``logging.getLogger(name)`` directly.
    """
    logger = logging.getLogger(name)

    # Guard: avoid adding handlers twice if this module is reimported.
    if logger.handlers:
        return logger

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S")

    # ------------------------------------------------------------------
    # Stream handler (stdout) — always enabled
    # ------------------------------------------------------------------
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(numeric_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # ------------------------------------------------------------------
    # Rotating file handler — <log_dir>/<name>.log
    # ------------------------------------------------------------------
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as exc:
        # If the log directory cannot be created (e.g. read-only FS in tests),
        # fall back to stdout-only and emit a warning.
        logger.warning(
            "Could not create file log handler for '%s': %s — using stdout only.",
            log_dir,
            exc,
        )

    # Prevent propagation to the root logger to avoid duplicate records.
    logger.propagate = False

    return logger
