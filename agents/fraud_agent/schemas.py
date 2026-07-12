"""
schemas.py — Pydantic models for the Fraud Agent.

Request and response shapes align with the Agent Contract defined in
docs/api.md.  Extra fields (feature values, raw probabilities) are nested
inside ``evidence`` so the top-level shape remains contract-compliant.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Valid transaction types
# ---------------------------------------------------------------------------

VALID_TRANSACTION_TYPES: frozenset[str] = frozenset(
    {"CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"}
)


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------


class TransactionPayload(BaseModel):
    """Agent-specific payload for fraud detection.

    Field names mirror the PaySim dataset schema used during model training.
    All monetary amounts are in the same currency unit as the training data.
    """

    step: Annotated[int, Field(ge=1, description="Simulation step (hour of the simulation).")]
    type: str = Field(
        ...,
        description=(
            "Transaction type. One of: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER."
        ),
    )
    amount: Annotated[
        float,
        Field(
            gt=0.0,
            description="Transaction amount (must be strictly positive).",
        ),
    ]
    oldbalanceOrg: Annotated[
        float,
        Field(ge=0.0, description="Origin account balance before the transaction."),
    ]
    newbalanceOrig: Annotated[
        float,
        Field(ge=0.0, description="Origin account balance after the transaction."),
    ]
    oldbalanceDest: Annotated[
        float,
        Field(ge=0.0, description="Destination account balance before the transaction."),
    ]
    newbalanceDest: Annotated[
        float,
        Field(ge=0.0, description="Destination account balance after the transaction."),
    ]
    isFlaggedFraud: Annotated[
        int,
        Field(
            ge=0,
            le=1,
            description="System flag: 1 if the transaction was flagged by the legacy rule-engine, 0 otherwise.",
        ),
    ] = 0

    @field_validator("type")
    @classmethod
    def validate_transaction_type(cls, v: str) -> str:
        """Reject unknown transaction type strings."""
        upper = v.upper()
        if upper not in VALID_TRANSACTION_TYPES:
            raise ValueError(
                f"Invalid transaction type '{v}'. "
                f"Must be one of: {sorted(VALID_TRANSACTION_TYPES)}."
            )
        return upper


class FraudAnalysisRequest(BaseModel):
    """Standard Agent Contract request envelope for the Fraud Agent."""

    case_id: str = Field(
        ..., description="Unique case identifier (join key across logs and reports)."
    )
    input_type: str = Field(
        default="transaction", description="Always 'transaction' for this agent."
    )
    payload: TransactionPayload


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class FraudEvidence(BaseModel):
    """Extra fields surfaced inside ``evidence`` without breaking the contract."""

    transaction_type: str = Field(..., description="Original transaction type string.")
    type_encoded: int = Field(..., description="LabelEncoded transaction type used by the model.")
    engineered_features: dict[str, Any] = Field(
        ..., description="Computed feature values fed to the model."
    )
    fraud_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Model probability of fraud."
    )
    safe_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Model probability of legitimate transaction."
    )
    model_version: str = Field(default="xgboost_paysim", description="Model identifier.")


class FraudAnalysisResponse(BaseModel):
    """Standard Agent Contract response envelope for the Fraud Agent."""

    agent: str = Field(default="fraud_agent")
    case_id: str
    verdict: str = Field(
        ...,
        description="One of: 'safe', 'fraud', 'suspicious'.",
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence in [0, 1].")
    risk_score: int = Field(..., ge=0, le=100, description="Integer risk score in [0, 100].")
    category: str = Field(
        ...,
        description="One of: 'mule_transaction', 'none'.",
    )
    explanation: str = Field(..., description="Short human-readable explanation.")
    evidence: FraudEvidence
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )


# ---------------------------------------------------------------------------
# Internal prediction result (not part of the HTTP contract)
# ---------------------------------------------------------------------------


class FraudPredictionResult(BaseModel):
    """Internal dataclass returned by predict.py before building the HTTP response."""

    predicted_class: str  # "fraud" or "safe"
    confidence: float = Field(..., ge=0.0, le=1.0)
    fraud_probability: float = Field(..., ge=0.0, le=1.0)
    safe_probability: float = Field(..., ge=0.0, le=1.0)
    type_encoded: int
    engineered_features: dict[str, Any]
