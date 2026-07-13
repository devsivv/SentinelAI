"""
config.py — Configuration for the Scam Communication Agent.

All paths and hyperparameters are read from environment variables or YAML
config files so nothing is hardcoded.  The ``ScamCommAgentConfig`` object is
the single authority for every tuneable in this agent.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field

from core.config import PROJECT_ROOT, AgentBaseConfig





class ScamCommAgentConfig(AgentBaseConfig):
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
        default=PROJECT_ROOT / "models" / "sms" / "sms_model.pkl",
        description="Path to the trained CalibratedClassifierCV(LinearSVC) model.",
    )
    tfidf_path: Path = Field(
        default=PROJECT_ROOT / "models" / "sms" / "tfidf_vectorizer.pkl",
        description="Path to the fitted TF-IDF vectorizer.",
    )

    # ------------------------------------------------------------------
    # Phishing URL model artifacts
    # ------------------------------------------------------------------
    phishing_model_path: Path = Field(
        default=PROJECT_ROOT / "models" / "phishing" / "phishing_model.joblib",
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



    model_config = {"env_prefix": "SCAM_COMM_", **AgentBaseConfig.model_config}


# ---------------------------------------------------------------------------
# Module-level singleton — import this everywhere instead of instantiating
# ---------------------------------------------------------------------------

settings = ScamCommAgentConfig()
