"""
Tests for the Intelligence Fusion Agent.
"""

from backend.fusion_agent.logic import aggregate_risk
from backend.fusion_agent.schemas import AgentResult, AgentType, FusionVerdict


def test_aggregate_risk_empty():
    """Test that empty agent responses return safe verdict."""
    verdict = aggregate_risk([])
    assert isinstance(verdict, FusionVerdict)
    assert verdict.final_verdict == "safe"
    assert verdict.overall_risk == 0


def test_aggregate_risk_single_safe():
    """Test that a single safe response returns safe verdict."""
    results = [
        AgentResult(
            agent=AgentType.CURRENCY,
            case_id="case-1",
            verdict="safe",
            confidence=0.9,
            risk_score=10,
            category="none",
            evidence={},
        )
    ]
    verdict = aggregate_risk(results)
    assert verdict.final_verdict == "safe"
    assert verdict.overall_risk == 10


def test_aggregate_risk_suspicious():
    """Test that scam comm flag alone triggers suspicious verdict."""
    results = [
        AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="case-1",
            verdict="fraud",
            confidence=0.6,
            risk_score=50,
            category="scam",
            evidence={},
        ),
        AgentResult(
            agent=AgentType.FRAUD,
            case_id="case-1",
            verdict="safe",
            confidence=0.8,
            risk_score=20,
            category="none",
            evidence={},
        ),
    ]
    verdict = aggregate_risk(results)
    assert verdict.final_verdict == "suspicious"
    assert verdict.overall_risk == 50


def test_aggregate_risk_fraud():
    """Test that isolated fraud transaction triggers fraud verdict."""
    results = [
        AgentResult(
            agent=AgentType.FRAUD,
            case_id="case-1",
            verdict="fraud",
            confidence=0.9,
            risk_score=85,
            category="mule_transaction",
            evidence={},
        )
    ]
    verdict = aggregate_risk(results)
    assert verdict.final_verdict == "fraud"
    assert verdict.overall_risk == 85


def test_aggregate_risk_high_risk_fraud():
    """Test that both fraud and scam flags trigger high_risk_fraud verdict."""
    results = [
        AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="case-1",
            verdict="fraud",
            confidence=0.8,
            risk_score=70,
            category="scam",
            evidence={},
        ),
        AgentResult(
            agent=AgentType.FRAUD,
            case_id="case-1",
            verdict="fraud",
            confidence=0.8,
            risk_score=70,
            category="mule_transaction",
            evidence={},
        ),
    ]
    verdict = aggregate_risk(results)
    # Rule escalates to at least 95
    assert verdict.overall_risk == 95
    assert verdict.final_verdict == "high_risk_fraud"


def test_aggregate_risk_max_score_preserved():
    """Test that risk score above 95 is preserved in high risk scenario."""
    results = [
        AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="case-1",
            verdict="fraud",
            confidence=0.9,
            risk_score=90,
            category="scam",
            evidence={},
        ),
        AgentResult(
            agent=AgentType.FRAUD,
            case_id="case-1",
            verdict="fraud",
            confidence=0.98,
            risk_score=98,
            category="mule_transaction",
            evidence={},
        ),
    ]
    verdict = aggregate_risk(results)
    assert verdict.overall_risk == 98
