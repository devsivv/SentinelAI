"""
main.py — FastAPI Application and Router entry point for the Graph Agent.

Supports running as a standalone microservice or being imported as a prefix router.
"""

from __future__ import annotations

from fastapi import FastAPI, APIRouter
from .schemas import GraphAnalysisRequest, GraphAnalysisResponse
from .service import analyze_graph

# Router for inclusion in unified API gateways
router = APIRouter(prefix="/graph", tags=["Graph Agent"])

@router.post(
    "/analyze",
    response_model=GraphAnalysisResponse,
    summary="Analyze Graph Connectivity (Prefixed)",
    description="Analyze in-memory entity graph to detect shared identities, phones, devices, and accounts."
)
async def analyze_endpoint_prefixed(request: GraphAnalysisRequest) -> GraphAnalysisResponse:
    """Analyze Case Graph Connectivity."""
    return await analyze_graph(request)


# Root/direct router for standalone microservice compliance with `POST /analyze`
standalone_router = APIRouter(tags=["Graph Agent Standalone"])

@standalone_router.post(
    "/analyze",
    response_model=GraphAnalysisResponse,
    summary="Analyze Graph Connectivity (Standard Contract)",
    description="Analyze in-memory entity graph to detect shared identities, phones, devices, and accounts."
)
async def analyze_endpoint_standalone(request: GraphAnalysisRequest) -> GraphAnalysisResponse:
    """Analyze Case Graph Connectivity."""
    return await analyze_graph(request)


# FastAPI Application instance for standalone running
app = FastAPI(
    title="SentinelAI Graph Agent",
    description="FastAPI service for NetworkX in-memory intelligence graph analysis.",
    version="0.1.0"
)

app.include_router(standalone_router)
app.include_router(router)
