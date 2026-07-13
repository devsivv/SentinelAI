"""
schemas.py — Pydantic models for the Currency Agent.

Request and response shapes align with the Agent Contract defined in
docs/api.md.  Extra fields (probabilities, top-k) are nested inside
``evidence`` so the top-level shape remains contract-compliant.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------


class CurrencyPayload(BaseModel):
    """Agent-specific payload carried inside the standard request envelope.

    The caller passes the raw image as bytes via a multipart upload at the
    FastAPI layer; this schema is used when the predict function receives
    pre-extracted data programmatically.
    """

    image_bytes: bytes = Field(..., description="Raw image bytes (JPEG/PNG/WebP).")


class CurrencyAnalysisRequest(BaseModel):
    """Standard Agent Contract request envelope for the Currency Agent."""

    case_id: str = Field(
        ..., description="Unique case identifier (join key across logs and reports)."
    )
    input_type: str = Field(
        default="image", description="Always 'image' for this agent."
    )
    payload: CurrencyPayload


# ---------------------------------------------------------------------------
# Response
# ---------------------------------------------------------------------------


class CurrencyEvidence(BaseModel):
    """Extra fields surfaced inside ``evidence`` without breaking the contract."""

    predicted_class: str = Field(..., description="Raw model output class label.")
    probabilities: dict[str, float] = Field(
        ...,
        description="Softmax probability for every class (class_name → probability).",
    )
    image_size: tuple[int, int] = Field(
        ..., description="(width, height) of the preprocessed image fed to the model."
    )
    model_version: str = Field(
        default="mobilenetv2", description="Backbone identifier."
    )


class CurrencyAnalysisResponse(BaseModel):
    """Standard Agent Contract response envelope for the Currency Agent."""

    agent: str = Field(default="currency_agent")
    case_id: str
    verdict: str = Field(
        ...,
        description="One of: 'safe' (genuine note), 'fraud' (counterfeit note), 'suspicious' (low-confidence).",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence in [0, 1]."
    )
    risk_score: int = Field(
        ..., ge=0, le=100, description="Integer risk score in [0, 100]."
    )
    category: str = Field(
        ...,
        description="One of: 'counterfeit_note' or 'none'.",
    )
    explanation: str = Field(..., description="Short human-readable explanation.")
    evidence: CurrencyEvidence
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )


# ---------------------------------------------------------------------------
# Internal prediction result (not part of the HTTP contract)
# ---------------------------------------------------------------------------


class PredictionResult(BaseModel):
    """Internal dataclass returned by predict.py before building the HTTP response."""

    predicted_class: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: dict[str, float]
    image_size: tuple[int, int]
