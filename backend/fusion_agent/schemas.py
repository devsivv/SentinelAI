"""
schemas.py — Pydantic models for the Intelligence Fusion Agent.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    FRAUD = "fraud_agent"
    SCAM_SMS = "scam_comm_agent_sms"
    SCAM_URL = "scam_comm_agent_url"
    CURRENCY = "currency_agent"
    GRAPH = "graph_agent"
    GEO = "geo_agent"


class AgentResult(BaseModel):
    """Canonical model for Fusion input."""

    agent: str = Field(..., description="The name or type of the agent.")
    case_id: str = Field(..., description="Unique case identifier.")
    verdict: str = Field(..., description="The verdict given by the agent.")
    confidence: float = Field(..., description="The confidence score.")
    risk_score: int = Field(..., description="The risk score.")
    category: str = Field(..., description="The category of the finding.")
    evidence: dict[str, Any] | BaseModel = Field(
        ..., description="Agent-specific evidence."
    )


class FusionVerdict(BaseModel):
    """Holistic verdict produced by the Fusion Agent."""

    final_verdict: str = Field(
        ..., description="Holistic verdict: 'safe', 'suspicious', 'high_risk_fraud'."
    )
    overall_risk: int = Field(
        ..., ge=0, le=100, description="Aggregated risk score in [0, 100]."
    )
    narrative: str = Field(
        ..., description="Human-readable explanation of the risk aggregation."
    )
    recommended_action: list[str] = Field(
        ..., description="Recommended actions based on the holistic risk."
    )


class AggregatedRiskResponse(BaseModel):
    """Response envelope for the Fusion Agent."""

    agent: str = Field(default="fusion_agent")
    case_id: str = Field(..., description="Unique case identifier.")
    final_verdict: str = Field(..., description="Holistic verdict.")
    overall_risk: int = Field(..., ge=0, le=100, description="Holistic risk score.")
    narrative: str = Field(..., description="Overall narrative of the case.")
    recommended_action: list[str] = Field(..., description="List of actions to take.")
    evidence: dict[str, Any] = Field(
        ..., description="Raw outputs from contributing agents."
    )
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )
