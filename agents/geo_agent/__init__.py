"""
__init__.py — Public surface of the Geo Intelligence Agent package.
"""

from __future__ import annotations

from .service import analyze_location
from .schemas import (
    GeoPayload,
    GeoAnalysisRequest,
    GeoAnalysisResponse,
    GeoEvidence,
    Incident,
    Hotspot,
    IncidentCluster,
    PatrolRecommendation,
)

__all__ = [
    # Service
    "analyze_location",
    # Schemas
    "GeoPayload",
    "GeoAnalysisRequest",
    "GeoAnalysisResponse",
    "GeoEvidence",
    "Incident",
    "Hotspot",
    "IncidentCluster",
    "PatrolRecommendation",
]
