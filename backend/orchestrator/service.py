"""
service.py — Implementation of the Orchestrator Agent.

Responsibilities:
- Receives multi-modal cases (InvestigateRequest).
- Fans out to individual AI agents concurrently (via asyncio).
- Enforces strong typing with Pydantic (no raw dicts).
- Transforms agent responses into canonical AgentResult.
- Calls the Fusion Agent to aggregate risk.
- Returns the final response.
"""

import asyncio
from typing import Any


from agents.fraud_agent.schemas import FraudAnalysisRequest, TransactionPayload
from agents.fraud_agent.service import analyze as analyze_fraud_service
from agents.scam_comm_agent.schemas import (
    ScamCommAnalysisRequest,
    SMSPayload,
    URLPayload,
)
from agents.scam_comm_agent.service import analyze_sms as analyze_sms_service
from agents.scam_comm_agent.service import analyze_url as analyze_url_service
from backend.fusion_agent.logic import aggregate_risk
from backend.fusion_agent.schemas import AgentResult, AgentType, AggregatedRiskResponse
import logging

from backend.orchestrator.schemas import InvestigateRequest

log = logging.getLogger("orchestrator")


async def process_case(request: InvestigateRequest) -> AggregatedRiskResponse:
    """Orchestrate the fan-out of a case and coordinate the Fusion Agent."""
    log.info("[case_id=%s] Orchestrator started investigation.", request.case_id)

    tasks = []

    # Map evidence items to appropriate agent public service methods
    for item in request.evidence:
        if item.input_type == "sms":
            tasks.append(_process_sms(request.case_id, item.payload))
        elif item.input_type == "url":
            tasks.append(_process_url(request.case_id, item.payload))
        elif item.input_type == "transaction":
            tasks.append(_process_transaction(request.case_id, item.payload))
        else:
            log.warning(
                "[case_id=%s] Unknown input_type '%s', skipping.",
                request.case_id,
                item.input_type,
            )

    # Fan out concurrently
    results = await asyncio.gather(*tasks)

    # Filter out None (failed/skipped tasks)
    valid_results = [r for r in results if r is not None]

    if not valid_results:
        log.warning("[case_id=%s] No valid agent results obtained.", request.case_id)
        # Return a default safe verdict if nothing was analyzed
        return AggregatedRiskResponse(
            case_id=request.case_id,
            final_verdict="safe",
            overall_risk=0,
            narrative="No actionable evidence was processed.",
            recommended_action=["No action required"],
            evidence={},
        )

    log.info(
        "[case_id=%s] Aggregating %d agent results via Fusion Agent.",
        request.case_id,
        len(valid_results),
    )

    # Execute fusion logic synchronously in threadpool (if it were CPU bound, but it's small rules)
    fusion_verdict = aggregate_risk(valid_results)

    # Assemble final response
    return AggregatedRiskResponse(
        case_id=request.case_id,
        final_verdict=fusion_verdict.final_verdict,
        overall_risk=fusion_verdict.overall_risk,
        narrative=fusion_verdict.narrative,
        recommended_action=fusion_verdict.recommended_action,
        evidence={r.agent: r.model_dump(mode="json") for r in valid_results},
    )


async def _process_sms(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    try:
        sms_payload = SMSPayload(**payload)
        req = ScamCommAnalysisRequest(
            case_id=case_id, input_type="sms", payload=sms_payload
        )
        res = await analyze_sms_service(req)

        return AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
    except Exception as exc:
        log.error("[case_id=%s] SMS Agent error: %s", case_id, exc)
        return None


async def _process_url(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    try:
        url_payload = URLPayload(**payload)
        req = ScamCommAnalysisRequest(
            case_id=case_id, input_type="url", payload=url_payload
        )
        res = await analyze_url_service(req)

        return AgentResult(
            agent=AgentType.SCAM_URL,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
    except Exception as exc:
        log.error("[case_id=%s] URL Agent error: %s", case_id, exc)
        return None


async def _process_transaction(
    case_id: str, payload: dict[str, Any]
) -> AgentResult | None:
    try:
        tx_payload = TransactionPayload(**payload)
        req = FraudAnalysisRequest(
            case_id=case_id, input_type="transaction", payload=tx_payload
        )
        res = await analyze_fraud_service(req)

        return AgentResult(
            agent=AgentType.FRAUD,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
    except Exception as exc:
        log.error("[case_id=%s] Fraud Agent error: %s", case_id, exc)
        return None
