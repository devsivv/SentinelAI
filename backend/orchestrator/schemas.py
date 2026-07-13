"""
schemas.py — Pydantic models for the Orchestrator Agent.
"""

from typing import Any

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """A generic evidence item containing its modality type and raw fields."""

    input_type: str = Field(..., description="E.g., 'sms', 'url', 'transaction'.")
    payload: dict[str, Any] = Field(
        ..., description="Agent-specific payload fields (e.g. {'text': '...'})."
    )


class InvestigateRequest(BaseModel):
    """Multi-modal request envelope for holistic case processing."""

    case_id: str = Field(..., description="Unique case identifier.")
    evidence: list[EvidenceItem] = Field(
        default_factory=list, description="List of multi-modal evidence items."
    )
