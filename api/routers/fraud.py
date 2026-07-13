"""
fraud.py — FastAPI router for the Fraud Agent.
"""

from __future__ import annotations

from fastapi import APIRouter

from agents.fraud_agent.predict import build_fraud_verdict, predict_fraud
from agents.fraud_agent.schemas import (FraudAnalysisRequest,
                                        FraudAnalysisResponse, FraudEvidence)

router = APIRouter(prefix="/fraud", tags=["Fraud Agent"])


@router.post(
    "/analyze",
    response_model=FraudAnalysisResponse,
    summary="Analyze Financial Transaction",
    description="Detect fraudulent patterns in financial transactions.",
)
async def analyze_fraud(request: FraudAnalysisRequest) -> FraudAnalysisResponse:
    """Analyze a transaction using the Fraud Agent."""

    # Run prediction
    result = predict_fraud(request.payload, case_id=request.case_id)

    # Build verdict
    verdict_dict = build_fraud_verdict(
        result, transaction_type=request.payload.type, case_id=request.case_id
    )

    # Assemble evidence
    evidence = FraudEvidence(
        transaction_type=request.payload.type,
        type_encoded=result.type_encoded,
        engineered_features=result.engineered_features,
        fraud_probability=result.fraud_probability,
        safe_probability=result.safe_probability,
    )

    # Return contract response
    return FraudAnalysisResponse(
        case_id=request.case_id,
        verdict=verdict_dict["verdict"],
        confidence=verdict_dict["confidence"],
        risk_score=verdict_dict["risk_score"],
        category=verdict_dict["category"],
        explanation=verdict_dict["explanation"],
        evidence=evidence,
    )
