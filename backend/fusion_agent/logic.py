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

    # 1. Base calculation: take the maximum risk score across all modalities
    # (A highly fraudulent transaction is still fraud, even if the SMS was safe)
    max_risk = max(res.risk_score for res in results)

    fraud_flags = 0
    scam_flags = 0

    for res in results:
        if res.verdict == "fraud":
            if res.agent == AgentType.FRAUD:
                fraud_flags += 1
            elif res.agent in (AgentType.SCAM_SMS, AgentType.SCAM_URL):
                scam_flags += 1

    # 2. Rule: Organized Digital Arrest Scam
    # If we detect a scam communication AND a fraudulent transaction in the same case
    if fraud_flags > 0 and scam_flags > 0:
        overall_risk = max(max_risk, 95)  # Escalate risk to at least 95
        return FusionVerdict(
            final_verdict="high_risk_fraud",
            overall_risk=overall_risk,
            narrative=(
                "CRITICAL: Correlated scam communication and fraudulent transaction detected. "
                "High probability of an organized Digital Arrest or Mule Account operation."
            ),
            recommended_action=[
                "Immediately freeze origin account",
                "Flag destination account for review",
                "Notify Cyber Cell",
                "Generate FIR draft",
            ],
        )

    # 3. Rule: Isolated Fraud Transaction
    if fraud_flags > 0:
        return FusionVerdict(
            final_verdict="fraud",
            overall_risk=max_risk,
            narrative="Fraudulent transaction detected without correlated scam communications.",
            recommended_action=[
                "Block transaction",
                "Trigger customer step-up authentication",
            ],
        )

    # 4. Rule: Scam Communication only (Phishing / Vishing attempt)
    if scam_flags > 0:
        return FusionVerdict(
            final_verdict="suspicious",
            overall_risk=max_risk,
            narrative="Scam communication detected. User may be under social engineering attack.",
            recommended_action=[
                "Send security warning SMS to customer",
                "Temporarily lower transaction limits",
            ],
        )

    # 5. Default Safe
    return FusionVerdict(
        final_verdict="safe",
        overall_risk=max_risk,
        narrative="All modalities classified as safe.",
        recommended_action=["Allow transaction"],
    )
