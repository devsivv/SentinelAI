"""
Tests for the Orchestrator Agent.
"""

import pytest

from backend.orchestrator.schemas import InvestigateRequest, EvidenceItem
from backend.orchestrator.service import process_case
from backend.fusion_agent.schemas import AgentResult, AgentType


@pytest.mark.asyncio
async def test_process_case_no_evidence():
    """Test that Orchestrator handles requests with no evidence payload."""
    request = InvestigateRequest(case_id="c-no-evidence", evidence=[])

    response = await process_case(request)

    assert response.case_id == "c-no-evidence"
    assert response.final_verdict == "safe"
    assert response.overall_risk == 0
    assert not response.evidence


@pytest.mark.asyncio
async def test_process_case_with_evidence(monkeypatch):
    """Test that Orchestrator successfully fans out to agents and aggregates risk."""

    # Mock the internal processing functions to avoid running ML inference in tests
    async def mock_process_sms(*args, **kwargs):
        return AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="c-test-all",
            verdict="suspicious",
            confidence=0.6,
            risk_score=60,
            category="none",
            evidence={},
        )

    async def mock_process_url(*args, **kwargs):
        return AgentResult(
            agent=AgentType.SCAM_URL,
            case_id="c-test-all",
            verdict="fraud",
            confidence=0.85,
            risk_score=85,
            category="phishing",
            evidence={},
        )

    async def mock_process_transaction(*args, **kwargs):
        return AgentResult(
            agent=AgentType.FRAUD,
            case_id="c-test-all",
            verdict="safe",
            confidence=0.9,
            risk_score=10,
            category="none",
            evidence={},
        )

    monkeypatch.setattr("backend.orchestrator.service._process_sms", mock_process_sms)
    monkeypatch.setattr("backend.orchestrator.service._process_url", mock_process_url)
    monkeypatch.setattr(
        "backend.orchestrator.service._process_transaction", mock_process_transaction
    )

    request = InvestigateRequest(
        case_id="c-test-all",
        evidence=[
            EvidenceItem(input_type="sms", payload={"text": "Test SMS"}),
            EvidenceItem(input_type="url", payload={"url": "http://test.com"}),
            EvidenceItem(
                input_type="transaction",
                payload={
                    "step": 1,
                    "type": "TRANSFER",
                    "amount": 100.0,
                    "oldbalanceOrg": 100.0,
                    "newbalanceOrig": 0.0,
                    "oldbalanceDest": 0.0,
                    "newbalanceDest": 100.0,
                    "isFlaggedFraud": 0,
                },
            ),
        ],
    )

    response = await process_case(request)

    assert response.case_id == "c-test-all"
    assert "scam_comm_agent_sms" in response.evidence
    assert "scam_comm_agent_url" in response.evidence
    assert "fraud_agent" in response.evidence

    assert response.overall_risk == 85
    assert response.final_verdict == "suspicious"
