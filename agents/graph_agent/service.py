"""
service.py — Public service layer for the Graph Intelligence Agent.
"""

from __future__ import annotations

import time
from .logging import get_logger
from .config import settings
from .entity_extractor import extract_and_normalize
from .graph_builder import build_case_graph
from .analyzer import run_graph_analysis
from .schemas import GraphAnalysisRequest, GraphAnalysisResponse

log = get_logger()


async def analyze_graph(request: GraphAnalysisRequest) -> GraphAnalysisResponse:
    """Analyze the network structure and entities of a case using the Graph Agent.

    This function coordinates entity extraction, normalization, graph building,
    network analysis, and verdict aggregation.
    """
    t_start = time.perf_counter()
    case_id = request.case_id

    log.info("[case_id=%s] Starting graph intelligence analysis.", case_id)

    # 1. Entity extraction and normalization
    entities, relationships = extract_and_normalize(
        entities=request.payload.entities,
        relationships=request.payload.relationships,
        raw_evidence=request.payload.raw_evidence,
        case_id=case_id
    )

    # 2. Graph construction (populate in-memory NetworkX model)
    build_case_graph(entities, relationships, case_id)

    # 3. Connected components, shared nodes, degree centrality, suspicious cluster detection
    evidence = run_graph_analysis(case_id)

    # 4. Determine final verdict based on network risk score
    risk_score = int(round(evidence.network_risk_score))
    
    if risk_score >= settings.risk_high_threshold:
        verdict = "fraud"
        category = "fraud_ring"
        explanation = (
            f"Organized fraud ring or suspicious cluster detected. "
            f"Case has connection to multiple shared entities or known suspects "
            f"(Network Risk: {risk_score}/100)."
        )
    elif risk_score >= settings.risk_medium_threshold:
        verdict = "suspicious"
        category = "none"
        explanation = (
            f"Suspicious network linkages detected. "
            f"Entities are shared across multiple cases or show elevated centralities "
            f"(Network Risk: {risk_score}/100)."
        )
    else:
        verdict = "safe"
        category = "none"
        explanation = (
            f"No significant suspicious network linkages or shared entities detected "
            f"(Network Risk: {risk_score}/100)."
        )

    # Calculate confidence based on whether we have shared findings or centrality values
    # If network has high centrality or shared findings, confidence is high.
    confidence = 0.90 if risk_score > 0 else 0.80

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] Graph analysis complete in %.2f ms — verdict=%s, risk_score=%d",
        case_id,
        elapsed_ms,
        verdict,
        risk_score
    )

    return GraphAnalysisResponse(
        case_id=case_id,
        verdict=verdict,
        confidence=confidence,
        risk_score=risk_score,
        category=category,
        explanation=explanation,
        evidence=evidence
    )
