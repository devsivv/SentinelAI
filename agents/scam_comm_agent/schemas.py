"""
schemas.py — Pydantic models for the Scam Communication Agent.

Request and response shapes align with the Agent Contract defined in
docs/api.md.  Extra fields (raw_text, probabilities, url_features) are
nested inside ``evidence`` so the top-level shape remains contract-compliant.

Two independent pipelines share these schemas:
  - SMS scam detection
  - Phishing URL detection
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------


class SMSPayload(BaseModel):
    """Agent-specific payload for SMS scam detection."""

    text: str = Field(..., description="Raw SMS message text to analyse.")


class URLPayload(BaseModel):
    """Agent-specific payload for phishing URL detection."""

    url: str = Field(..., description="URL string to analyse.")


class ScamCommAnalysisRequest(BaseModel):
    """Standard Agent Contract request envelope for the Scam Comm Agent."""

    case_id: str = Field(
        ..., description="Unique case identifier (join key across logs and reports)."
    )
    input_type: str = Field(
        ...,
        description="Input modality: 'sms' or 'url'.",
    )
    payload: SMSPayload | URLPayload


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class SMSEvidence(BaseModel):
    """Extra fields surfaced inside ``evidence`` for SMS predictions."""

    cleaned_text: str = Field(..., description="Preprocessed text fed to TF-IDF.")
    scam_probability: float = Field(..., description="Model probability of scam class.")
    ham_probability: float = Field(..., description="Model probability of ham class.")
    model_version: str = Field(default="calibrated_linearsvc", description="Model identifier.")


class URLEvidence(BaseModel):
    """Extra fields surfaced inside ``evidence`` for URL predictions."""

    url: str = Field(..., description="Original URL analysed.")
    features: dict[str, Any] = Field(..., description="Extracted URL features used by the model.")
    phishing_probability: float = Field(..., description="Model probability of phishing class.")
    safe_probability: float = Field(..., description="Model probability of safe class.")
    model_version: str = Field(default="xgboost_phishing", description="Model identifier.")


class ScamCommAnalysisResponse(BaseModel):
    """Standard Agent Contract response envelope for the Scam Comm Agent."""

    agent: str = Field(default="scam_comm_agent")
    case_id: str
    verdict: str = Field(
        ...,
        description="One of: 'safe', 'fraud', 'suspicious'.",
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence in [0, 1].")
    risk_score: int = Field(..., ge=0, le=100, description="Integer risk score in [0, 100].")
    category: str = Field(
        ...,
        description="One of: 'digital_arrest_scam', 'phishing', 'none'.",
    )
    explanation: str = Field(..., description="Short human-readable explanation.")
    evidence: SMSEvidence | URLEvidence
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )


# ---------------------------------------------------------------------------
# Internal prediction results (not part of the HTTP contract)
# ---------------------------------------------------------------------------


class SMSPredictionResult(BaseModel):
    """Internal dataclass returned by sms_predict.py before building the HTTP response."""

    predicted_class: str  # "scam" or "ham"
    confidence: float = Field(..., ge=0.0, le=1.0)
    scam_probability: float
    ham_probability: float
    cleaned_text: str


class URLPredictionResult(BaseModel):
    """Internal dataclass returned by url_predict.py before building the HTTP response."""

    predicted_class: str  # "phishing" or "safe"
    confidence: float = Field(..., ge=0.0, le=1.0)
    phishing_probability: float
    safe_probability: float
    features: dict[str, Any]
