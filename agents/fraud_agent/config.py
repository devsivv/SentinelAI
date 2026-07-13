"""
config.py — Configuration for the Fraud Agent.

All paths and hyperparameters are read from environment variables or YAML
config files so nothing is hardcoded.  The ``FraudAgentConfig`` object is
the single authority for every tuneable in this agent.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field

from core.config import PROJECT_ROOT, AgentBaseConfig


class FraudAgentConfig(AgentBaseConfig):
    """Runtime configuration for the Fraud Agent.

    Values are read from environment variables (``FRAUD_*`` prefix) so they
    can be overridden without touching YAML in CI/CD or Docker.  Defaults
    correspond to the canonical paths agreed in ``configs/models.yaml`` and
    ``PROJECT_STRUCTURE.md``.
    """

    # ------------------------------------------------------------------
    # Model artifacts
    # ------------------------------------------------------------------
    model_path: Path = Field(
        default=PROJECT_ROOT / "models" / "transactions" / "paysim_model.joblib",
        description="Path to the exported XGBoost fraud detection model (joblib).",
    )

    # ------------------------------------------------------------------
    # Feature engineering constants
    # ------------------------------------------------------------------
    large_transaction_threshold: float = Field(
        default=1_200_000.0,
        gt=0.0,
        description=(
            "Amount above which a transaction is flagged as 'large'. "
            "Corresponds to the 95th-percentile of transaction amounts in the "
            "PaySim training dataset."
        ),
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

    model_config = {"env_prefix": "FRAUD_", **AgentBaseConfig.model_config}


# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere instead of instantiating
# ---------------------------------------------------------------------------

settings = FraudAgentConfig()
