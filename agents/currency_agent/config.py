"""
config.py — Configuration for the Currency Agent.

All paths and hyperparameters are read from environment variables or YAML
config files so nothing is hardcoded.  The ``CurrencyAgentConfig`` object is
the single authority for every tuneable in this agent.
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


# ---------------------------------------------------------------------------
# Resolve project root so relative config paths work regardless of CWD
# ---------------------------------------------------------------------------

# agents/currency_agent/ → agents/ → project root
_AGENT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _AGENT_DIR.parent.parent


class CurrencyAgentConfig(BaseSettings):
    """Runtime configuration for the Currency Agent.

    Values are read from environment variables (``CURRENCY_*`` prefix) so they
    can be overridden without touching YAML in CI/CD or Docker.  Defaults
    correspond to the canonical paths agreed in ``configs/models.yaml`` and
    ``PROJECT_STRUCTURE.md``.
    """

    # ------------------------------------------------------------------
    # Model artifacts
    # ------------------------------------------------------------------
    model_path: Path = Field(
        default=_PROJECT_ROOT / "models" / "currency" / "mobilenet_v2.pt",
        description="Path to the exported TorchScript / state-dict file.",
    )
    class_names_path: Path = Field(
        default=_PROJECT_ROOT / "models" / "currency" / "class_names.json",
        description="Path to the class_names.json produced during training.",
    )

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------
    image_size: tuple[int, int] = Field(
        default=(224, 224),
        description="(height, width) expected by MobileNetV2.",
    )

    # ImageNet normalisation constants — these must match the values used
    # during training (standard torchvision defaults).
    normalize_mean: tuple[float, float, float] = Field(
        default=(0.485, 0.456, 0.406),
        description="Per-channel mean for ImageNet normalisation.",
    )
    normalize_std: tuple[float, float, float] = Field(
        default=(0.229, 0.224, 0.225),
        description="Per-channel std for ImageNet normalisation.",
    )

    # ------------------------------------------------------------------
    # Inference thresholds
    # ------------------------------------------------------------------
    confidence_threshold: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
        description=(
            "Minimum confidence required to emit a definitive verdict. "
            "Predictions below this threshold are labelled 'suspicious'."
        ),
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    log_dir: Path = Field(
        default=_PROJECT_ROOT / "logs" / "agents",
        description="Directory where agent log files are written.",
    )
    log_level: str = Field(
        default="INFO",
        description="Python logging level (DEBUG, INFO, WARNING, ERROR).",
    )

    model_config = {"env_prefix": "CURRENCY_", "env_file": ".env", "extra": "ignore"}


# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere instead of instantiating
# ---------------------------------------------------------------------------

settings = CurrencyAgentConfig()
