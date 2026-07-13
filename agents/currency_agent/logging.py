"""
logging.py — Structured logger for the Currency Agent.

Creates a named ``logging.Logger`` that:
  - Writes to a rotating file under ``logs/agents/currency_agent.log``
  - Also streams to stdout so container logs remain observable
  - Follows the level set in ``CurrencyAgentConfig.log_level``

Import ``get_logger`` from this module in every other file of the agent
so that all records share the same handler configuration.
"""

from __future__ import annotations

import logging

from core.logging import build_agent_logger

from .config import settings

_LOGGER_NAME = "currency_agent"

# Initialise logger at import time so handlers are registered before any
# other module tries to log.
build_agent_logger(_LOGGER_NAME, settings.log_dir, settings.log_level)


def get_logger() -> logging.Logger:
    """Return the shared Currency Agent logger.

    Usage::

        from agents.currency_agent.logging import get_logger

        log = get_logger()
        log.info("Inference complete", extra={"case_id": case_id})
    """
    return logging.getLogger(_LOGGER_NAME)
