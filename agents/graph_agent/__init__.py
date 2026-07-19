"""
__init__.py — Public surface of the Graph Intelligence Agent package.

Exposes the primary service functions, schemas, and models.
"""

from __future__ import annotations

from .model import get_global_graph
from .service import analyze_graph
from .schemas import (
    Entity,
    EntityType,
    GraphAnalysisRequest,
    GraphAnalysisResponse,
    GraphEvidence,
    GraphPayload,
    Relationship,
    RelationshipType,
    SharedEntityFinding,
    SuspiciousCluster,
)

__all__ = [
    # Schemas
    "Entity",
    "EntityType",
    "GraphAnalysisRequest",
    "GraphAnalysisResponse",
    "GraphEvidence",
    "GraphPayload",
    "Relationship",
    "RelationshipType",
    "SharedEntityFinding",
    "SuspiciousCluster",
    # Service
    "analyze_graph",
    # Model
    "get_global_graph",
]
