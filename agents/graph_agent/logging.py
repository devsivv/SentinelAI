"""
logging.py — Structured logger for the Graph Intelligence Agent.
"""

from __future__ import annotations

import logging
from core.logging import build_agent_logger
from .config import settings

_LOGGER_NAME = "graph_agent"

build_agent_logger(_LOGGER_NAME, settings.log_dir, settings.log_level)


def get_logger() -> logging.Logger:
    """Return the shared Graph Agent logger."""
    return logging.getLogger(_LOGGER_NAME)
