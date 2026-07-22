"""
core/config.py — Shared configuration infrastructure for SentinelAI agents.

This module provides:

``AgentBaseConfig``
    Base ``pydantic_settings.BaseSettings`` subclass for every agent.
    Handles log_dir, log_level, and .env loading.  Agent-specific settings
    (model paths, thresholds, etc.) remain in each agent's own ``config.py``.

``AppConfig``
    Top-level application configuration read by the FastAPI layer (api/main.py).
    Centralises values that were previously hardcoded (API version, CORS origins).
"""

import os
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

# Constrain OpenMP, MKL, OpenBLAS, and NumExpr to 1 thread to avoid memory spikes on multi-core containers
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

# Dynamically discover the project root assuming this file is in `core/`
_CORE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _CORE_DIR.parent

# ---------------------------------------------------------------------------
# Application-level settings (used by the FastAPI layer, not individual agents)
# ---------------------------------------------------------------------------

API_VERSION = "0.1.0"


class AppConfig(BaseSettings):
    """Top-level SentinelAI application configuration.

    All values can be overridden via environment variables or a ``.env`` file.

    Environment variables (no prefix):
        API_HOST          — Host the API server binds to (default: 127.0.0.1)
        API_PORT          — Port the API server listens on (default: 8000)
        CORS_ORIGINS      — Comma-separated list of allowed CORS origins
                            (default: http://localhost:5173,http://127.0.0.1:5173)
        LOG_LEVEL         — Root log level (default: INFO)
        DATABASE_URL      — PostgreSQL connection URL in SQLAlchemy format
                            e.g. postgresql+psycopg://user:pass@host:5432/dbname
                            Must be set in .env — no real default is shipped.
    """

    api_host: str = Field(
        default="127.0.0.1",
        description="Host the API server binds to.",
    )
    api_port: int = Field(
        default=8000,
        description="Port the API server listens on.",
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"],
        description=(
            "Allowed CORS origins.  Set CORS_ORIGINS as a comma-separated string "
            "in .env to override, e.g. CORS_ORIGINS=http://localhost:3000,https://app.example.com"
        ),
    )
    log_level: str = Field(
        default="INFO",
        description="Root logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    # SecretStr prevents the password from appearing in repr(), logs, or
    # validation error messages.  Call .get_secret_value() only where the
    # raw string is strictly required (i.e. engine creation).
    database_url: SecretStr = Field(
        default="postgresql+psycopg://postgres:change_me@localhost:5432/sentinelai",
        description=(
            "PostgreSQL connection URL (SQLAlchemy format). "
            "Override via DATABASE_URL in your .env file. "
            "The default placeholder will connect to a local dev DB; "
            "it is not a real credential and must be changed for any real deployment."
        ),
    )
    low_memory_mode: bool = Field(
        default=True,
        description=(
            "If True, orchestrator executes agent tasks sequentially to keep peak RAM "
            "below 512MB on memory-constrained deployments (e.g. Render Free). "
            "Set LOW_MEMORY_MODE=false in .env to enable full concurrent execution."
        ),
    )

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


# Module-level singleton — import ``app_config`` from here to avoid re-instantiation.
app_config = AppConfig()


# ---------------------------------------------------------------------------
# Agent base configuration (shared by all AI agents)
# ---------------------------------------------------------------------------


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
