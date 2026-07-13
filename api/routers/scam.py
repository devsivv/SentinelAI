"""
scam.py — FastAPI router for the Scam Communication Agent.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from agents.scam_comm_agent.schemas import (ScamCommAnalysisRequest,
                                            ScamCommAnalysisResponse,
                                            SMSEvidence, SMSPayload,
                                            URLEvidence, URLPayload)
from agents.scam_comm_agent.sms_predict import build_sms_verdict, predict_sms
from agents.scam_comm_agent.url_predict import build_url_verdict, predict_url

router = APIRouter(prefix="/scam", tags=["Scam Communication Agent"])


@router.post(
    "/sms",
    response_model=ScamCommAnalysisResponse,
    summary="Analyze SMS Text",
    description="Detect whether an SMS message contains a scam attempt.",
)
async def analyze_sms(request: ScamCommAnalysisRequest) -> ScamCommAnalysisResponse:
    """Analyze an SMS message using the Scam Communication Agent."""
    if request.input_type != "sms":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input_type '{request.input_type}' for /scam/sms endpoint. Expected 'sms'.",
        )

    if not isinstance(request.payload, SMSPayload):
        raise HTTPException(
            status_code=400, detail="Payload must match SMSPayload schema."
        )

    # Run prediction
    result = predict_sms(request.payload.text, case_id=request.case_id)

    # Build verdict
    verdict_dict = build_sms_verdict(result, case_id=request.case_id)

    # Assemble evidence
    evidence = SMSEvidence(
        cleaned_text=result.cleaned_text,
        scam_probability=result.scam_probability,
        ham_probability=result.ham_probability,
    )

    # Return contract response
    return ScamCommAnalysisResponse(
        case_id=request.case_id,
        verdict=verdict_dict["verdict"],
        confidence=verdict_dict["confidence"],
        risk_score=verdict_dict["risk_score"],
        category=verdict_dict["category"],
        explanation=verdict_dict["explanation"],
        evidence=evidence,
    )


@router.post(
    "/url",
    response_model=ScamCommAnalysisResponse,
    summary="Analyze URL",
    description="Detect whether a URL is a phishing attempt.",
)
async def analyze_url(request: ScamCommAnalysisRequest) -> ScamCommAnalysisResponse:
    """Analyze a URL using the Scam Communication Agent."""
    if request.input_type != "url":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input_type '{request.input_type}' for /scam/url endpoint. Expected 'url'.",
        )

    if not isinstance(request.payload, URLPayload):
        raise HTTPException(
            status_code=400, detail="Payload must match URLPayload schema."
        )

    # Run prediction
    result = predict_url(request.payload.url, case_id=request.case_id)

    # Build verdict
    verdict_dict = build_url_verdict(result, case_id=request.case_id)

    # Assemble evidence
    evidence = URLEvidence(
        url=request.payload.url,
        features=result.features,
        phishing_probability=result.phishing_probability,
        safe_probability=result.safe_probability,
    )

    # Return contract response
    return ScamCommAnalysisResponse(
        case_id=request.case_id,
        verdict=verdict_dict["verdict"],
        confidence=verdict_dict["confidence"],
        risk_score=verdict_dict["risk_score"],
        category=verdict_dict["category"],
        explanation=verdict_dict["explanation"],
        evidence=evidence,
    )
