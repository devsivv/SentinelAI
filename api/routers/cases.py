"""
cases.py — FastAPI router for retrieving persisted investigation cases.
"""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.repositories.agent_result_repository import AgentResultRepository
from backend.repositories.case_repository import CaseRepository
from backend.repositories.fusion_report_repository import FusionReportRepository

router = APIRouter(prefix="/cases", tags=["cases"])

case_repo = CaseRepository()
agent_res_repo = AgentResultRepository()
fusion_rep_repo = FusionReportRepository()


@router.get("", summary="List investigation cases from PostgreSQL.")
def list_cases(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """Retrieves all persisted investigation cases from the database."""
    cases = case_repo.list_cases(db, limit=limit, offset=offset)
    result = []
    for c in cases:
        fusion_report = fusion_rep_repo.get_report_by_case(db, c.id)
        result.append(
            {
                "case_id": str(c.id),
                "status": c.status,
                "investigation_type": c.investigation_type,
                "source": c.source,
                "metadata": c.metadata_json or {},
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                "fusion_report": (
                    {
                        "final_verdict": fusion_report.final_verdict,
                        "overall_risk": fusion_report.overall_risk,
                        "confidence": fusion_report.confidence,
                        "explanation": fusion_report.explanation,
                        "recommended_action": fusion_report.recommended_action,
                    }
                    if fusion_report
                    else None
                ),
            }
        )
    return result


@router.get("/{case_id}", summary="Get detailed investigation case by ID.")
def get_case(
    case_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Retrieves a single investigation case with its agent results and fusion report."""
    case = case_repo.get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found.")

    agent_results = agent_res_repo.get_results_by_case(db, case.id)
    fusion_report = fusion_rep_repo.get_report_by_case(db, case.id)

    return {
        "case_id": str(case.id),
        "status": case.status,
        "investigation_type": case.investigation_type,
        "source": case.source,
        "metadata": case.metadata_json or {},
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "updated_at": case.updated_at.isoformat() if case.updated_at else None,
        "agent_results": [
            {
                "id": str(ar.id),
                "agent_name": ar.agent_name,
                "verdict": ar.verdict,
                "confidence": ar.confidence,
                "risk_score": ar.risk_score,
                "explanation": ar.explanation,
                "raw_output": ar.raw_output,
                "created_at": ar.created_at.isoformat() if ar.created_at else None,
            }
            for ar in agent_results
        ],
        "fusion_report": (
            {
                "final_verdict": fusion_report.final_verdict,
                "overall_risk": fusion_report.overall_risk,
                "confidence": fusion_report.confidence,
                "explanation": fusion_report.explanation,
                "recommended_action": fusion_report.recommended_action,
                "created_at": (
                    fusion_report.created_at.isoformat()
                    if fusion_report.created_at
                    else None
                ),
            }
            if fusion_report
            else None
        ),
    }
