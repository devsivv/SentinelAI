"""
logging.py — Structured logger for the Fraud Agent.

Creates a named ``logging.Logger`` that:
  - Writes to a rotating file under ``logs/agents/fraud_agent.log``
  - Also streams to stdout so container logs remain observable
  - Follows the level set in ``FraudAgentConfig.log_level``

Import ``get_logger`` from this module in every other file of the agent
so that all records share the same handler configuration.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import settings

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_LOGGER_NAME = "fraud_agent"
_LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)-8s | %(message)s"
_MAX_BYTES = 10 * 1024 * 1024  # 10 MiB per log file
_BACKUP_COUNT = 5


def _build_logger() -> logging.Logger:
    """Create and configure the agent logger (called once at module import)."""

    logger = logging.getLogger(_LOGGER_NAME)

    # Guard: avoid adding handlers twice if this module is reimported.
    if logger.handlers:
        return logger

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S")

    # ------------------------------------------------------------------
    # Stream handler (stdout) — always enabled
    # ------------------------------------------------------------------
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # ------------------------------------------------------------------
    # Rotating file handler — writes to logs/agents/fraud_agent.log
    # ------------------------------------------------------------------
    try:
        log_dir: Path = settings.log_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "fraud_agent.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as exc:
        # If the log directory cannot be created (e.g. read-only FS in tests),
        # fall back to stdout-only and emit a warning.
        logger.warning(
            "Could not create file log handler for '%s': %s — using stdout only.",
            settings.log_dir,
            exc,
        )

    # Prevent propagation to the root logger to avoid duplicate records.
    logger.propagate = False

    return logger


def get_logger() -> logging.Logger:
    """Return the shared Fraud Agent logger.

    Usage::

        from agents.fraud_agent.logging import get_logger

        log = get_logger()
        log.info("Inference complete", extra={"case_id": case_id})
    """
    return logging.getLogger(_LOGGER_NAME)


# ---------------------------------------------------------------------------
# Initialise logger at import time so handlers are registered before any
# other module tries to log.
# ---------------------------------------------------------------------------
_build_logger()
