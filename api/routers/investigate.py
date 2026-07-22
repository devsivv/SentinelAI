"""
investigate.py — FastAPI router for the Orchestrator Agent.
"""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

import logging
import time

from backend.db.session import get_db
from backend.fusion_agent.schemas import AggregatedRiskResponse
from backend.orchestrator.schemas import InvestigateRequest
from backend.orchestrator.service import process_case

log = logging.getLogger("api.investigate")

router = APIRouter(prefix="/investigate", tags=["orchestrator"])


@router.post(
    "",
    response_model=AggregatedRiskResponse,
    summary="Process multi-modal evidence across all agents.",
    description="Accepts multi-modal payloads (SMS, URL, Transaction), fans them out to active agents, and aggregates the risk holistically.",
)
async def investigate_case(
    request: InvestigateRequest = Body(
        ...,
        description="The multi-modal case evidence.",
        openapi_examples={
            "full_case": {
                "summary": "Full Multi-Modal Case",
                "value": {
                    "case_id": "case-999",
                    "evidence": [
                        {
                            "input_type": "sms",
                            "payload": {
                                "text": "URGENT: Click here to verify your account."
                            },
                        },
                        {
                            "input_type": "url",
                            "payload": {"url": "http://verify-secure-login.com"},
                        },
                        {
                            "input_type": "transaction",
                            "payload": {
                                "step": 1,
                                "type": "TRANSFER",
                                "amount": 50000.0,
                                "oldbalanceOrg": 50000.0,
                                "newbalanceOrig": 0.0,
                                "oldbalanceDest": 0.0,
                                "newbalanceDest": 50000.0,
                                "isFlaggedFraud": 0,
                            },
                        },
                    ],
                },
            }
        },
    ),
    db: Session = Depends(get_db),
):
    """
    HTTP POST handler for holistic case analysis.
    """
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    evidence_types = [e.input_type for e in request.evidence]
    log.info(
        "[case_id=%s] Request received: %d evidence items %s",
        request.case_id,
        len(request.evidence),
        evidence_types,
    )
    # DEBUG LOGGING END

    try:
        # DEBUG LOGGING START
        log.info("[case_id=%s] Entering orchestrator...", request.case_id)
        # DEBUG LOGGING END
        result = await process_case(request, db=db)
        # DEBUG LOGGING START
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        log.info(
            "[case_id=%s] Orchestrator completed investigation in %.2f ms",
            request.case_id,
            elapsed_ms,
        )
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        log.exception(
            "[case_id=%s] Exception in investigate_case after %.2f ms: %s",
            request.case_id,
            elapsed_ms,
            exc,
        )
        # DEBUG LOGGING END
        raise


