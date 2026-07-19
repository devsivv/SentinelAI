"""
graph.py — FastAPI router for the Graph Intelligence Agent.
"""

from fastapi import APIRouter
from agents.graph_agent.schemas import GraphAnalysisRequest, GraphAnalysisResponse
from agents.graph_agent.service import analyze_graph

router = APIRouter(prefix="/graph", tags=["Graph Agent"])


@router.post(
    "/analyze",
    response_model=GraphAnalysisResponse,
    summary="Analyze Case Graph Connectivity",
    description="Analyze in-memory entity graph to detect shared identities, phones, devices, and accounts.",
)
async def analyze_case_graph(request: GraphAnalysisRequest) -> GraphAnalysisResponse:
    """Analyze Case Graph Connectivity."""
    return await analyze_graph(request)
