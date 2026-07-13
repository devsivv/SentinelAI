"""
currency.py — FastAPI router for the Currency Agent.
"""

from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile

from agents.currency_agent.predict import build_verdict, predict
from agents.currency_agent.schemas import CurrencyAnalysisResponse, CurrencyEvidence

router = APIRouter(prefix="/currency", tags=["Currency Agent"])


@router.post(
    "/analyze",
    response_model=CurrencyAnalysisResponse,
    summary="Analyze Currency Image",
    description="Upload a currency image to detect if it is counterfeit or genuine.",
)
async def analyze_currency(
    case_id: str = Form(...),
    image: UploadFile = File(...),
) -> CurrencyAnalysisResponse:
    """Analyze a currency image using the Currency Agent."""
    # Read the raw image bytes
    image_bytes = await image.read()

    # Run prediction (this is synchronous; in a real high-throughput scenario
    # we might use a threadpool, but for this refactor we call it directly)
    result = predict(image_bytes, case_id=case_id)

    # Build the verdict dictionary
    verdict_dict = build_verdict(result, case_id=case_id)

    # Assemble the evidence
    evidence = CurrencyEvidence(
        predicted_class=result.predicted_class,
        probabilities=result.probabilities,
        image_size=result.image_size,
    )

    # Assemble and return the standard contract response
    return CurrencyAnalysisResponse(
        case_id=case_id,
        verdict=verdict_dict["verdict"],
        confidence=verdict_dict["confidence"],
        risk_score=verdict_dict["risk_score"],
        category=verdict_dict["category"],
        explanation=verdict_dict["explanation"],
        evidence=evidence,
    )
