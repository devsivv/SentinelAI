"""
schemas.py — Pydantic models for the Graph Intelligence Agent.

Enforces compliance with the standard Agent Contract. All graph-specific
findings and network metrics are stored inside the ``evidence`` block.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    CASE = "Case"
    VICTIM = "Victim"
    PHONE = "Phone Number"
    EMAIL = "Email"
    BANK_ACCOUNT = "Bank Account"
    UPI = "UPI ID"
    DEVICE = "Device ID"
    IP = "IP Address"
    URL = "URL"
    MERCHANT = "Merchant"
    TRANSACTION = "Transaction"
    SUSPECT = "Suspect"


class RelationshipType(str, Enum):
    USED = "USED"
    CONNECTED_TO = "CONNECTED_TO"
    TRANSFERRED_TO = "TRANSFERRED_TO"
    SHARES_PHONE = "SHARES_PHONE"
    SHARES_DEVICE = "SHARES_DEVICE"
    SHARES_ACCOUNT = "SHARES_ACCOUNT"
    SHARES_URL = "SHARES_URL"
    INVOLVES = "INVOLVES"
    LINKED_WITH = "LINKED_WITH"


class Entity(BaseModel):
    """Represents a node in the intelligence graph."""

    type: EntityType = Field(..., description="The classification of the entity.")
    id: str = Field(..., description="The unique value/identifier of the entity.")
    properties: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata properties."
    )


class Relationship(BaseModel):
    """Represents a directed edge between two entities."""

    source_type: EntityType = Field(..., description="The type of the source entity.")
    source_id: str = Field(..., description="The identifier of the source entity.")
    target_type: EntityType = Field(..., description="The type of the target entity.")
    target_id: str = Field(..., description="The identifier of the target entity.")
    type: RelationshipType = Field(..., description="The type of the relationship.")
    properties: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata properties."
    )


class GraphPayload(BaseModel):
    """Pydantic schema for the Graph Agent payload."""

    entities: List[Entity] = Field(
        default_factory=list, description="List of pre-extracted entities."
    )
    relationships: List[Relationship] = Field(
        default_factory=list, description="List of relationships between entities."
    )
    raw_evidence: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Raw case data/evidence lists (e.g. from orchestrator) to extract dynamically.",
    )


class GraphAnalysisRequest(BaseModel):
    """Standard Agent Contract request envelope for the Graph Agent."""

    case_id: str = Field(..., description="Unique case identifier.")
    input_type: str = Field(
        default="graph_data",
        description="Modality of input: 'graph_data' or 'case_evidence'.",
    )
    payload: GraphPayload


class SharedEntityFinding(BaseModel):
    """Details about a shared entity bridging multiple victims, suspects, or cases."""

    entity_type: str
    entity_id: str
    connected_cases: List[str]
    connected_victims: List[str]
    connected_suspects: List[str]


class SuspiciousCluster(BaseModel):
    """Sub-graph representing a potential organized fraud ring."""

    cluster_id: int
    nodes: List[str]
    node_count: int
    case_ids: List[str]
    suspect_count: int
    victim_count: int
    risk_level: str  # 'low', 'medium', 'high'


class GraphEvidence(BaseModel):
    """Evidence schema containing detailed in-memory graph analysis findings."""

    num_nodes: int = Field(..., description="Total nodes in local/global graph partition.")
    num_edges: int = Field(..., description="Total edges in local/global graph partition.")
    connected_components: List[List[str]] = Field(
        ..., description="List of connected components (groups of linked nodes)."
    )
    repeated_entities: Dict[str, List[str]] = Field(
        ..., description="Entities linking to multiple nodes/cases."
    )
    shared_phones: List[SharedEntityFinding] = Field(
        default_factory=list, description="Phone numbers shared across cases/entities."
    )
    shared_urls: List[SharedEntityFinding] = Field(
        default_factory=list, description="URLs shared across cases/entities."
    )
    shared_upis: List[SharedEntityFinding] = Field(
        default_factory=list, description="UPI IDs shared across cases/entities."
    )
    shared_accounts: List[SharedEntityFinding] = Field(
        default_factory=list, description="Bank accounts shared across cases/entities."
    )
    shared_devices: List[SharedEntityFinding] = Field(
        default_factory=list, description="Device IDs shared across cases/entities."
    )
    repeated_identities: List[SharedEntityFinding] = Field(
        default_factory=list, description="Identities of victims/suspects repeated in multiple cases."
    )
    degree_centrality: Dict[str, float] = Field(
        ..., description="Top degree centrality scores in the analyzed graph."
    )
    suspicious_clusters: List[SuspiciousCluster] = Field(
        default_factory=list, description="Identified suspicious sub-graphs or clusters."
    )
    network_risk_score: float = Field(
        ..., ge=0.0, le=100.0, description="Estimated risk score from network structures."
    )


class GraphAnalysisResponse(BaseModel):
    """Standard Agent Contract response envelope for the Graph Agent."""

    agent: str = Field(default="graph_agent")
    case_id: str
    verdict: str = Field(
        ..., description="One of: 'safe', 'suspicious', 'fraud'."
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Agent confidence score in [0.0, 1.0]."
    )
    risk_score: int = Field(
        ..., ge=0, le=100, description="Risk score in range [0, 100]."
    )
    category: str = Field(
        ..., description="Categorization of findings, e.g. 'fraud_ring' or 'none'."
    )
    explanation: str = Field(..., description="Short explanation summary.")
    evidence: GraphEvidence
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )
