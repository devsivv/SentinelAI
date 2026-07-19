"""
logic.py — Core rule-based reasoning engine for the Intelligence Fusion Agent.

Responsibilities:
- Ingest strongly typed outputs (list[AgentResult]) from the Orchestrator.
- Aggregate risk scores across multiple modalities.
- Apply domain-specific business rules (e.g., Organized Digital Arrest).
- Return a final unified verdict and recommended actions.
- No ML models are loaded or invoked here.
"""

import logging

from backend.fusion_agent.schemas import AgentResult, AgentType, FusionVerdict

log = logging.getLogger("fusion_agent")


def aggregate_risk(results: list[AgentResult]) -> FusionVerdict:
    """Aggregate risk across all agent results using rule-based reasoning."""
    if not results:
        return FusionVerdict(
            final_verdict="safe",
            overall_risk=0,
            narrative="No agent results provided for fusion.",
            recommended_action=["No action required"],
        )

    # Separate Geo Agent result from core results to treat it as contextual evidence
    geo_res = next((res for res in results if res.agent == AgentType.GEO), None)
    core_results = [res for res in results if res.agent != AgentType.GEO]

    # Handle scenario where ONLY the Geo agent is present
    if not core_results:
        if geo_res:
            verdict = geo_res.verdict
            return FusionVerdict(
                final_verdict=verdict,
                overall_risk=geo_res.risk_score,
                narrative=f"Geographical risk context analyzed: {geo_res.explanation}",
                recommended_action=[
                    "Monitor activity at this location",
                    "Conduct secondary manual review",
                ] if verdict != "safe" else ["Allow transaction"],
            )
        return FusionVerdict(
            final_verdict="safe",
            overall_risk=0,
            narrative="No agent results provided for fusion.",
            recommended_action=["No action required"],
        )

    # 1. Base calculation: take the maximum risk score across all core modalities
    max_risk = max(res.risk_score for res in core_results)

    fraud_flags = 0
    scam_flags = 0

    for res in core_results:
        if res.verdict == "fraud":
            if res.agent in (AgentType.FRAUD, AgentType.GRAPH):
                fraud_flags += 1
            elif res.agent in (AgentType.SCAM_SMS, AgentType.SCAM_URL):
                scam_flags += 1

    # Initialize baseline verdict variables
    baseline_verdict = "safe"
    overall_risk = max_risk
    narrative = ""
    recommended_action = []

    # 2. Rule: Organized Digital Arrest Scam
    # If we detect a scam communication AND a fraudulent transaction in the same case
    if fraud_flags > 0 and scam_flags > 0:
        baseline_verdict = "high_risk_fraud"
        overall_risk = max(max_risk, 95)  # Escalate risk to at least 95
        narrative = (
            "CRITICAL: Correlated scam communication and fraudulent transaction/network linkages detected. "
            "High probability of an organized Digital Arrest or Mule Account operation."
        )
        recommended_action = [
            "Immediately freeze origin account",
            "Flag destination account for review",
            "Notify Cyber Cell",
            "Generate FIR draft",
        ]

    # 3. Rule: Isolated Fraud or Network Linkage
    elif fraud_flags > 0:
        baseline_verdict = "fraud"
        narrative = "Fraudulent transaction or suspicious network linkages detected without correlated scam communications."
        recommended_action = [
            "Block transaction or flag accounts",
            "Trigger customer step-up authentication",
        ]

    # 4. Rule: Scam Communication only (Phishing / Vishing attempt)
    elif scam_flags > 0:
        baseline_verdict = "suspicious"
        narrative = "Scam communication detected. User may be under social engineering attack."
        recommended_action = [
            "Send security warning SMS to customer",
            "Temporarily lower transaction limits",
        ]

    # 5. Default Safe
    else:
        baseline_verdict = "safe"
        narrative = "All modalities classified as safe."
        recommended_action = ["Allow transaction"]

    # Apply contextual Geo Agent modifier if present
    if geo_res:
        if geo_res.verdict == "fraud":
            overall_risk = min(overall_risk + 5, 100)
            narrative += f"\nContextual Geo Alert: High-risk crime hotspot detected at coordinates."
        elif geo_res.verdict == "safe":
            overall_risk = max(overall_risk - 5, 0)
            narrative += f"\nContextual Geo Info: Target coordinates are located in a historically low-crime zone."
        else:
            overall_risk = min(overall_risk + 2, 100)
            narrative += f"\nContextual Geo Alert: Elevated crime occurrences flagged near coordinates."

    return FusionVerdict(
        final_verdict=baseline_verdict,
        overall_risk=overall_risk,
        narrative=narrative,
        recommended_action=recommended_action,
    )
