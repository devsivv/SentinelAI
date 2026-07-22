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

from __future__ import annotations

import asyncio
import logging
import time
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
from sqlalchemy.orm import Session

from backend.fusion_agent.logic import aggregate_risk
from backend.fusion_agent.schemas import AgentResult, AgentType, AggregatedRiskResponse
from backend.orchestrator.schemas import InvestigateRequest
from backend.repositories.agent_result_repository import AgentResultRepository
from backend.repositories.case_repository import CaseRepository
from backend.repositories.fusion_report_repository import FusionReportRepository

log = logging.getLogger("orchestrator")


async def process_case(
    request: InvestigateRequest,
    db: Session | None = None,
) -> AggregatedRiskResponse:
    """Orchestrate the fan-out of a case, persist results to DB, and coordinate the Fusion Agent."""
    if db is None:
        from backend.db.session import SessionLocal

        with SessionLocal() as db_session:
            return await _process_case_internal(request, db_session)
    else:
        return await _process_case_internal(request, db)


async def _process_case_internal(
    request: InvestigateRequest,
    db: Session,
) -> AggregatedRiskResponse:
    # DEBUG LOGGING START
    t_case_start = time.perf_counter()
    evidence_types = [item.input_type for item in request.evidence]
    log.info("START process_case")
    log.info("[case_id=%s] Received case with evidence types: %s", request.case_id, evidence_types)
    # DEBUG LOGGING END

    try:
        # 1. Create Case record in PostgreSQL
        # DEBUG LOGGING START
        log.info("[case_id=%s] Persisting case record...", request.case_id)
        # DEBUG LOGGING END
        case_repo = CaseRepository()
        inv_type = request.evidence[0].input_type if request.evidence else "multi_modal"
        case_obj = case_repo.create_case(
            db,
            status="processing",
            investigation_type=inv_type,
            source="orchestrator",
            metadata_json={"evidence_count": len(request.evidence)},
            request_case_id=request.case_id,
        )

        tasks = []
        has_explicit_graph = False

        # DEBUG LOGGING START
        log.info("[case_id=%s] Scheduling tasks...", request.case_id)
        # DEBUG LOGGING END

        # Map evidence items to appropriate agent public service methods
        for item in request.evidence:
            if item.input_type == "sms":
                tasks.append(_process_sms(request.case_id, item.payload))
                # DEBUG LOGGING START
                log.info("[case_id=%s] SMS task created", request.case_id)
                # DEBUG LOGGING END
            elif item.input_type == "url":
                tasks.append(_process_url(request.case_id, item.payload))
                # DEBUG LOGGING START
                log.info("[case_id=%s] URL task created", request.case_id)
                # DEBUG LOGGING END
            elif item.input_type == "transaction":
                tasks.append(_process_transaction(request.case_id, item.payload))
                # DEBUG LOGGING START
                log.info("[case_id=%s] Fraud task created", request.case_id)
                # DEBUG LOGGING END
            elif item.input_type in ("image", "currency"):
                tasks.append(_process_currency(request.case_id, item.payload))
                # DEBUG LOGGING START
                log.info("[case_id=%s] Currency task created", request.case_id)
                # DEBUG LOGGING END
            elif item.input_type == "graph_data":
                tasks.append(_process_graph(request.case_id, item.payload))
                has_explicit_graph = True
                # DEBUG LOGGING START
                log.info("[case_id=%s] Graph task created", request.case_id)
                # DEBUG LOGGING END
            elif item.input_type == "location":
                tasks.append(_process_geo(request.case_id, item.payload))
                # DEBUG LOGGING START
                log.info("[case_id=%s] Geo task created", request.case_id)
                # DEBUG LOGGING END
            else:
                log.warning(
                    "[case_id=%s] Unknown input_type '%s', skipping.",
                    request.case_id,
                    item.input_type,
                )

        # Automatically trigger Graph Agent on raw evidence if not explicitly passed
        if not has_explicit_graph and request.evidence:
            raw_list = [item.model_dump(mode="json") for item in request.evidence]
            tasks.append(_process_graph(request.case_id, {"raw_evidence": raw_list}))
            # DEBUG LOGGING START
            log.info("[case_id=%s] Auto-triggered Graph task created", request.case_id)
            # DEBUG LOGGING END

        # DEBUG LOGGING START
        log.info("[case_id=%s] Awaiting asyncio.gather() across %d tasks...", request.case_id, len(tasks))
        t_gather_start = time.perf_counter()
        # DEBUG LOGGING END

        # Fan out concurrently
        results = await asyncio.gather(*tasks)

        # DEBUG LOGGING START
        log.info(
            "[case_id=%s] asyncio.gather() finished in %.2f ms",
            request.case_id,
            (time.perf_counter() - t_gather_start) * 1000,
        )
        # DEBUG LOGGING END

        # Filter out None (failed/skipped tasks)
        valid_results = [r for r in results if r is not None]

        # 2. Persist Agent Results
        if valid_results:
            # DEBUG LOGGING START
            log.info("[case_id=%s] Persisting %d agent results...", request.case_id, len(valid_results))
            # DEBUG LOGGING END
            agent_result_repo = AgentResultRepository()
            agent_result_repo.create_results(db, case_id=case_obj.id, results=valid_results)

        if not valid_results:
            log.warning("[case_id=%s] No valid agent results obtained.", request.case_id)
            fusion_repo = FusionReportRepository()
            fusion_repo.create_report(
                db,
                case_id=case_obj.id,
                final_verdict="safe",
                overall_risk=0,
                explanation="No actionable evidence was processed.",
                recommended_action=["No action required"],
            )
            case_obj.status = "completed"
            db.commit()

            # DEBUG LOGGING START
            log.info("END process_case [no valid results]")
            # DEBUG LOGGING END
            return AggregatedRiskResponse(
                case_id=request.case_id,
                final_verdict="safe",
                overall_risk=0,
                narrative="No actionable evidence was processed.",
                recommended_action=["No action required"],
                evidence={},
            )

        # DEBUG LOGGING START
        log.info("[case_id=%s] Fusion starting...", request.case_id)
        t_fusion_start = time.perf_counter()
        # DEBUG LOGGING END

        # 3. Generate Fusion Verdict & Persist Fusion Report
        fusion_verdict = aggregate_risk(valid_results)

        # DEBUG LOGGING START
        log.info(
            "[case_id=%s] Fusion completed in %.2f ms — verdict=%s",
            request.case_id,
            (time.perf_counter() - t_fusion_start) * 1000,
            fusion_verdict.final_verdict,
        )
        # DEBUG LOGGING END

        conf_values = [r.confidence for r in valid_results if r.confidence is not None]
        avg_confidence = (sum(conf_values) / len(conf_values)) if conf_values else None

        # DEBUG LOGGING START
        log.info("[case_id=%s] Persisting fusion report...", request.case_id)
        # DEBUG LOGGING END

        fusion_repo = FusionReportRepository()
        fusion_repo.create_report(
            db,
            case_id=case_obj.id,
            final_verdict=fusion_verdict.final_verdict,
            overall_risk=fusion_verdict.overall_risk,
            confidence=avg_confidence,
            explanation=fusion_verdict.narrative,
            recommended_action=fusion_verdict.recommended_action,
        )

        case_obj.status = "completed"
        db.commit()

        # DEBUG LOGGING START
        elapsed_case = (time.perf_counter() - t_case_start) * 1000
        log.info("Returning response — Entire investigate request took %.2f ms", elapsed_case)
        log.info("END process_case")
        # DEBUG LOGGING END

        # Assemble final response
        return AggregatedRiskResponse(
            case_id=request.case_id,
            final_verdict=fusion_verdict.final_verdict,
            overall_risk=fusion_verdict.overall_risk,
            narrative=fusion_verdict.narrative,
            recommended_action=fusion_verdict.recommended_action,
            evidence={r.agent: r.model_dump(mode="json") for r in valid_results},
        )

    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("Failure while processing case_id=%s: %s", request.case_id, exc)
        # DEBUG LOGGING END
        raise


async def _process_sms(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_sms", case_id)
    log.info("[case_id=%s] SMS input received: %s", case_id, payload)
    # DEBUG LOGGING END
    try:
        sms_payload = SMSPayload(**payload)
        req = ScamCommAnalysisRequest(
            case_id=case_id, input_type="sms", payload=sms_payload
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] SMS prediction started...", case_id)
        # DEBUG LOGGING END
        res = await analyze_sms_service(req)
        
        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] SMS prediction finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] SMS prediction took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        result = AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] SMS response generated, EXIT _process_sms", case_id)
        log.info("SMS completed")
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] SMS Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None


async def _process_url(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_url", case_id)
    log.info("[case_id=%s] URL input received: %s", case_id, payload)
    # DEBUG LOGGING END
    try:
        url_payload = URLPayload(**payload)
        req = ScamCommAnalysisRequest(
            case_id=case_id, input_type="url", payload=url_payload
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] URL prediction started...", case_id)
        # DEBUG LOGGING END
        res = await analyze_url_service(req)

        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] URL prediction finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] URL prediction took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        result = AgentResult(
            agent=AgentType.SCAM_URL,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] URL response generated, EXIT _process_url", case_id)
        log.info("URL completed")
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] URL Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None


async def _process_transaction(
    case_id: str, payload: dict[str, Any]
) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_transaction", case_id)
    log.info("[case_id=%s] Transaction input received", case_id)
    # DEBUG LOGGING END
    try:
        tx_payload = TransactionPayload(**payload)
        req = FraudAnalysisRequest(
            case_id=case_id, input_type="transaction", payload=tx_payload
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Fraud prediction started...", case_id)
        # DEBUG LOGGING END
        res = await analyze_fraud_service(req)

        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] Fraud prediction finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] Fraud prediction took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        result = AgentResult(
            agent=AgentType.FRAUD,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Fraud response generated, EXIT _process_transaction", case_id)
        log.info("Fraud completed")
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] Fraud Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None


async def _process_currency(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_currency", case_id)
    log.info("[case_id=%s] Currency input received", case_id)
    # DEBUG LOGGING END
    try:
        import base64
        from agents.currency_agent.predict import predict, build_verdict
        from agents.currency_agent.schemas import CurrencyEvidence
        
        # Resolve raw image bytes (may be base64-encoded or raw string in mock cases)
        image_data = payload.get("image_bytes", b"")
        if isinstance(image_data, str):
            try:
                raw_bytes = base64.b64decode(image_data)
            except Exception:
                raw_bytes = image_data.encode("utf-8")
        else:
            raw_bytes = image_data

        # DEBUG LOGGING START
        log.info("[case_id=%s] Currency prediction started...", case_id)
        # DEBUG LOGGING END
        result = predict(raw_bytes, case_id=case_id)
        verdict_dict = build_verdict(result, case_id=case_id)

        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] Currency prediction finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] Currency prediction took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        evidence = CurrencyEvidence(
            predicted_class=result.predicted_class,
            probabilities=result.probabilities,
            image_size=result.image_size,
        )

        res = AgentResult(
            agent=AgentType.CURRENCY,
            case_id=case_id,
            verdict=verdict_dict["verdict"],
            confidence=verdict_dict["confidence"],
            risk_score=verdict_dict["risk_score"],
            category=verdict_dict["category"],
            evidence=evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Currency response generated, EXIT _process_currency", case_id)
        log.info("Currency completed")
        # DEBUG LOGGING END
        return res
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] Currency Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None


async def _process_graph(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_graph", case_id)
    log.info("[case_id=%s] Graph input received", case_id)
    # DEBUG LOGGING END
    try:
        from agents.graph_agent.schemas import GraphAnalysisRequest, GraphPayload
        from agents.graph_agent.service import analyze_graph

        graph_payload = GraphPayload(**payload)
        req = GraphAnalysisRequest(
            case_id=case_id, input_type="graph_data", payload=graph_payload
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Graph analysis started...", case_id)
        # DEBUG LOGGING END
        res = await analyze_graph(req)

        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] Graph analysis finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] Graph analysis took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        result = AgentResult(
            agent=AgentType.GRAPH,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Graph response generated, EXIT _process_graph", case_id)
        log.info("Graph completed")
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] Graph Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None


async def _process_geo(case_id: str, payload: dict[str, Any]) -> AgentResult | None:
    # DEBUG LOGGING START
    t_start = time.perf_counter()
    log.info("[case_id=%s] ENTER _process_geo", case_id)
    log.info("[case_id=%s] Geo input received", case_id)
    # DEBUG LOGGING END
    try:
        from agents.geo_agent.schemas import GeoAnalysisRequest, GeoPayload
        from agents.geo_agent.service import analyze_location

        geo_payload = GeoPayload(**payload)
        req = GeoAnalysisRequest(
            case_id=case_id, input_type="location", payload=geo_payload
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Geo analysis started...", case_id)
        # DEBUG LOGGING END
        res = await analyze_location(req)

        # DEBUG LOGGING START
        elapsed = (time.perf_counter() - t_start) * 1000
        log.info("[case_id=%s] Geo analysis finished in %.2f ms", case_id, elapsed)
        log.info("[case_id=%s] Geo analysis took %.2f ms", case_id, elapsed)
        # DEBUG LOGGING END

        result = AgentResult(
            agent=AgentType.GEO,
            case_id=res.case_id,
            verdict=res.verdict,
            confidence=res.confidence,
            risk_score=res.risk_score,
            category=res.category,
            evidence=res.evidence,
        )
        # DEBUG LOGGING START
        log.info("[case_id=%s] Geo response generated, EXIT _process_geo", case_id)
        log.info("Geo completed")
        # DEBUG LOGGING END
        return result
    except Exception as exc:
        # DEBUG LOGGING START
        log.exception("[case_id=%s] Geo Agent exception: %s", case_id, exc)
        # DEBUG LOGGING END
        return None

