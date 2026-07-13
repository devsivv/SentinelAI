"""
scam.py — FastAPI router for the Scam Communication Agent.
"""

from __future__ import annotations

from fastapi import APIRouter

from agents.scam_comm_agent.schemas import (
    ScamCommAnalysisRequest,
    ScamCommAnalysisResponse,
)
from agents.scam_comm_agent.service import analyze_sms, analyze_url

router = APIRouter(prefix="/scam", tags=["Scam Communication Agent"])


@router.post(
    "/sms",
    response_model=ScamCommAnalysisResponse,
    summary="Analyze SMS Text",
    description="Detect whether an SMS message contains a scam attempt.",
)
async def analyze_sms_route(
    request: ScamCommAnalysisRequest,
) -> ScamCommAnalysisResponse:
    """Analyze an SMS message using the Scam Communication Agent."""
    return await analyze_sms(request)


@router.post(
    "/url",
    response_model=ScamCommAnalysisResponse,
    summary="Analyze URL",
    description="Detect whether a URL is a phishing attempt.",
)
async def analyze_url_route(
    request: ScamCommAnalysisRequest,
) -> ScamCommAnalysisResponse:
    """Analyze a URL using the Scam Communication Agent."""
    return await analyze_url(request)
