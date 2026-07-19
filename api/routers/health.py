"""
health.py — System health and status endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from core.config import API_VERSION

router = APIRouter(tags=["System"])



class StatusResponse(BaseModel):
    service: str
    version: str
    status: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@router.get(
    "/",
    response_model=StatusResponse,
    summary="Get API Status",
    description="Returns the service name, version, and general API status.",
)
async def get_status() -> StatusResponse:
    return StatusResponse(
        service="SentinelAI",
        version=API_VERSION,
        status="operational",
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Get Health Check",
    description="Returns the current health status and UTC timestamp.",
)
async def get_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
