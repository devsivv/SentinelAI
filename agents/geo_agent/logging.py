"""
logging.py — Structured logging setup for the Geo Intelligence Agent.
"""

from __future__ import annotations

import logging
from core.logging import build_agent_logger
from .config import settings

_LOGGER_NAME = "geo_agent"

build_agent_logger(_LOGGER_NAME, settings.log_dir, settings.log_level)


def get_logger() -> logging.Logger:
    """Return the shared Geo Agent logger."""
    return logging.getLogger(_LOGGER_NAME)
