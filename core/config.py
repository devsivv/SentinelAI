"""
core/config.py — Shared configuration infrastructure for SentinelAI agents.

This module provides the ``AgentBaseConfig`` class, which handles:
  - Inheriting from ``pydantic_settings.BaseSettings``
  - Discovering the ``_PROJECT_ROOT`` dynamically
  - Setting up standard ``log_dir`` and ``log_level`` fields
  - Configuring ``.env`` loading (via ``model_config``)

Agent-specific settings (model paths, thresholds, etc.) remain in each
agent's own ``config.py``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

# Dynamically discover the project root assuming this file is in `core/`
_CORE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _CORE_DIR.parent


class AgentBaseConfig(BaseSettings):
    """Base configuration for SentinelAI agents.

    Subclass this in each agent to add agent-specific settings and an
    ``env_prefix`` within a new ``model_config``.
    """

    log_dir: Path = Field(
        default=PROJECT_ROOT / "logs" / "agents",
        description="Absolute path to the directory where agent logs are written.",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (e.g. DEBUG, INFO, WARNING, ERROR).",
    )

    # Note: Pydantic v2 requires subclasses to merge or redefine `model_config`
    # if they want to add an `env_prefix`.
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }
