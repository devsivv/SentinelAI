"""
main.py — FastAPI Application and Router entry point for the Geo Agent.
"""

from __future__ import annotations

from fastapi import FastAPI, APIRouter
from .schemas import GeoAnalysisRequest, GeoAnalysisResponse
from .service import analyze_location

# Prefixed router for unified gateway inclusion
router = APIRouter(prefix="/geo", tags=["Geo Agent"])

@router.post(
    "/analyze",
    response_model=GeoAnalysisResponse,
    summary="Analyze Location Risk (Prefixed)",
    description="Analyze geographical coordinates to detect crime density, hotspots, and patrol plans."
)
async def analyze_endpoint_prefixed(request: GeoAnalysisRequest) -> GeoAnalysisResponse:
    """Analyze Geographical Coordinate Risk."""
    return await analyze_location(request)


# Standalone router for microservice POST /analyze contract compliance
standalone_router = APIRouter(tags=["Geo Agent Standalone"])

@standalone_router.post(
    "/analyze",
    response_model=GeoAnalysisResponse,
    summary="Analyze Location Risk (Standard Contract)",
    description="Analyze geographical coordinates to detect crime density, hotspots, and patrol plans."
)
async def analyze_endpoint_standalone(request: GeoAnalysisRequest) -> GeoAnalysisResponse:
    """Analyze Geographical Coordinate Risk."""
    return await analyze_location(request)


# FastAPI standalone instance
app = FastAPI(
    title="SentinelAI Geo Agent",
    description="FastAPI spatial crime analytics and hotspot detection service.",
    version="0.1.0"
)

app.include_router(standalone_router)
app.include_router(router)
