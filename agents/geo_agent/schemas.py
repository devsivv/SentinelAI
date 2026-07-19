"""
schemas.py — Pydantic validation schemas for the Geo Intelligence Agent.

Exposes standard request and response objects complying with the Agent Contract.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator


class GeoPayload(BaseModel):
    """Payload carrying location coordinates and metadata for analysis."""

    latitude: float = Field(..., description="Latitude coordinate in degrees.")
    longitude: float = Field(..., description="Longitude coordinate in degrees.")
    district: Optional[str] = Field(default=None, description="District name.")
    state: Optional[str] = Field(default=None, description="State name.")
    radius_km: Optional[float] = Field(
        default=None, gt=0.0, description="Search radius in kilometers for density analysis."
    )


class GeoAnalysisRequest(BaseModel):
    """Standard Agent Contract request envelope for the Geo Agent."""

    case_id: str = Field(..., description="Unique case identifier.")
    input_type: str = Field(
        default="location", description="Modality of input, always 'location' for this agent."
    )
    payload: GeoPayload

    @field_validator("input_type")
    @classmethod
    def validate_input_type(cls, v: str) -> str:
        """Reject types other than 'location'."""
        if v.lower() != "location":
            raise ValueError("input_type must be 'location'")
        return v.lower()


class Incident(BaseModel):
    """Represents a historical incident record."""

    id: str = Field(..., description="Unique incident identifier.")
    latitude: float = Field(..., description="Incident latitude coordinate.")
    longitude: float = Field(..., description="Incident longitude coordinate.")
    district: str = Field(..., description="District where the incident occurred.")
    state: str = Field(..., description="State where the incident occurred.")
    category: str = Field(..., description="Crime classification / category.")
    timestamp: str = Field(..., description="ISO8601 timestamp of occurrence.")
    distance_km: Optional[float] = Field(
        default=None, description="Distance from the queried target point in kilometers."
    )


class Hotspot(BaseModel):
    """Summary of a identified spatial crime hotspot."""

    center_latitude: float
    center_longitude: float
    incident_count: int
    radius_km: float
    risk_level: str  # 'low', 'medium', 'high'


class IncidentCluster(BaseModel):
    """Heuristically clustered group of nearby historical incidents."""

    cluster_id: int
    center_latitude: float
    center_longitude: float
    node_count: int
    incidents: List[str] = Field(..., description="List of incident IDs in this cluster.")
    typical_category: str = Field(..., description="Most frequent crime category in the cluster.")


class PatrolRecommendation(BaseModel):
    """Actionable patrol recommendations generated from geo heuristics."""

    priority: str = Field(..., description="Patrol urgency: 'low', 'medium', 'high'.")
    patrol_frequency: str = Field(
        ..., description="Recommended frequency: 'daily', 'hourly', 'weekly', 'none'."
    )
    suggested_hubs: List[str] = Field(
        default_factory=list, description="Incident categories or specific coordinates to focus on."
    )
    narrative: str = Field(..., description="Short explanation of patrol recommendation reasoning.")


class GeoEvidence(BaseModel):
    """Aggregated geographical findings returned inside the agent evidence payload."""

    input_coords: Tuple[float, float] = Field(..., description="Queried input (latitude, longitude).")
    valid_coords: bool = Field(..., description="Indicates if coordinates are within valid range.")
    district: str = Field(..., description="Identified / default district name.")
    state: str = Field(..., description="Identified / default state name.")
    nearby_incidents_count: int = Field(..., description="Count of historical incidents within radius.")
    nearby_incidents: List[Incident] = Field(
        default_factory=list, description="List of nearby incidents inside search radius."
    )
    district_aggregation: Dict[str, int] = Field(
        default_factory=dict, description="Incidents count per district across historical DB."
    )
    state_aggregation: Dict[str, int] = Field(
        default_factory=dict, description="Incidents count per state across historical DB."
    )
    relative_crime_density: float = Field(
        ..., description="Calculated crime density (incidents per square kilometer)."
    )
    hotspots: List[Hotspot] = Field(
        default_factory=list, description="Identified hotspots in the vicinity."
    )
    clusters: List[IncidentCluster] = Field(
        default_factory=list, description="Spatial clusters of historical incidents."
    )
    patrol_recommendations: PatrolRecommendation = Field(..., description="Heuristic patrol planning.")


class GeoAnalysisResponse(BaseModel):
    """Standard Agent Contract response envelope for the Geo Agent."""

    agent: str = Field(default="geo_agent")
    case_id: str
    verdict: str = Field(
        ..., description="One of: 'safe' (low crime), 'suspicious' (medium risk), 'fraud' (crime hotspot)."
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Agent confidence score in [0.0, 1.0]."
    )
    risk_score: int = Field(
        ..., ge=0, le=100, description="Geo risk score in range [0, 100]."
    )
    category: str = Field(
        ..., description="Categorization of findings, e.g. 'crime_hotspot' or 'none'."
    )
    explanation: str = Field(..., description="Short explanation summary.")
    evidence: GeoEvidence
    processed_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp.",
    )
