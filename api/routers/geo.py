"""
geo.py — FastAPI router for the Geo Intelligence Agent.
"""

from fastapi import APIRouter
from agents.geo_agent.schemas import GeoAnalysisRequest, GeoAnalysisResponse
from agents.geo_agent.service import analyze_location

router = APIRouter(prefix="/geo", tags=["Geo Agent"])


@router.post(
    "/analyze",
    response_model=GeoAnalysisResponse,
    summary="Analyze Location Risk",
    description="Detect crime density, hotspot boundaries, and patrol recommendations at a given coordinate.",
)
async def analyze_geo_location(request: GeoAnalysisRequest) -> GeoAnalysisResponse:
    """Analyze Location Risk."""
    return await analyze_location(request)
