"""
config.py — Configuration for the Scam Communication Agent.

All paths and hyperparameters are read from environment variables or YAML
config files so nothing is hardcoded.  The ``ScamCommAgentConfig`` object is
the single authority for every tuneable in this agent.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


# ---------------------------------------------------------------------------
# Resolve project root so relative config paths work regardless of CWD
# ---------------------------------------------------------------------------

# agents/scam_comm_agent/ → agents/ → project root
_AGENT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _AGENT_DIR.parent.parent


class ScamCommAgentConfig(BaseSettings):
    """Runtime configuration for the Scam Communication Agent.

    Values are read from environment variables (``SCAM_COMM_*`` prefix) so they
    can be overridden without touching YAML in CI/CD or Docker.  Defaults
    correspond to the canonical paths agreed in ``configs/models.yaml`` and
    ``PROJECT_STRUCTURE.md``.
    """

    # ------------------------------------------------------------------
    # SMS model artifacts
    # ------------------------------------------------------------------
    sms_model_path: Path = Field(
        default=_PROJECT_ROOT / "models" / "sms" / "sms_model.pkl",
        description="Path to the trained CalibratedClassifierCV(LinearSVC) model.",
    )
    tfidf_path: Path = Field(
        default=_PROJECT_ROOT / "models" / "sms" / "tfidf_vectorizer.pkl",
        description="Path to the fitted TF-IDF vectorizer.",
    )

    # ------------------------------------------------------------------
    # Phishing URL model artifacts
    # ------------------------------------------------------------------
    phishing_model_path: Path = Field(
        default=_PROJECT_ROOT / "models" / "phishing" / "phishing_model.joblib",
        description="Path to the trained XGBoost phishing model.",
    )

    # ------------------------------------------------------------------
    # Inference thresholds
    # ------------------------------------------------------------------
    sms_confidence_threshold: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
        description=(
            "Minimum confidence required to emit a definitive SMS verdict. "
            "Predictions below this threshold are labelled 'suspicious'."
        ),
    )
    url_confidence_threshold: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
        description=(
            "Minimum confidence required to emit a definitive URL verdict. "
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

    model_config = {"env_prefix": "SCAM_COMM_", "env_file": ".env", "extra": "ignore"}


# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere instead of instantiating
# ---------------------------------------------------------------------------

settings = ScamCommAgentConfig()
