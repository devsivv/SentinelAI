"""
fraud.py — FastAPI router for the Fraud Agent.
"""

from fastapi import APIRouter
from agents.fraud_agent.schemas import FraudAnalysisRequest, FraudAnalysisResponse
from agents.fraud_agent.service import analyze

router = APIRouter(prefix="/fraud", tags=["Fraud Agent"])


@router.post(
    "/analyze",
    response_model=FraudAnalysisResponse,
    summary="Analyze Financial Transaction",
    description="Detect fraudulent patterns in financial transactions.",
)
async def analyze_fraud(request: FraudAnalysisRequest) -> FraudAnalysisResponse:
    """Analyze a transaction using the Fraud Agent."""
    return await analyze(request)
