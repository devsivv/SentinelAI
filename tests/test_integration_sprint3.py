"""
Integration tests for Sprint 03 Orchestrator and Fusion components.
"""

from fastapi.testclient import TestClient

from api.main import app
from backend.fusion_agent.schemas import AgentResult, AgentType

client = TestClient(app)


def test_investigate_case_empty():
    """Test orchestrator endpoint with no payloads."""
    payload = {"case_id": "c-integration-01", "evidence": []}
    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "c-integration-01"
    assert data["final_verdict"] == "safe"
    assert data["overall_risk"] == 0


def test_investigate_case_full(monkeypatch):
    """Test orchestrator endpoint with all payloads, mocked at the agent level."""

    # Mock the internal processing functions to avoid running ML inference in tests
    async def mock_process_sms(*args, **kwargs):
        return AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="c-integration-02",
            verdict="suspicious",
            confidence=0.6,
            risk_score=60,
            category="none",
            evidence={},
        )

    async def mock_process_url(*args, **kwargs):
        return AgentResult(
            agent=AgentType.SCAM_URL,
            case_id="c-integration-02",
            verdict="fraud",
            confidence=0.85,
            risk_score=85,
            category="phishing",
            evidence={},
        )

    async def mock_process_transaction(*args, **kwargs):
        return AgentResult(
            agent=AgentType.FRAUD,
            case_id="c-integration-02",
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

    payload = {
        "case_id": "c-integration-02",
        "evidence": [
            {"input_type": "sms", "payload": {"text": "URGENT: Verify your account."}},
            {"input_type": "url", "payload": {"url": "http://verify-account.com"}},
            {
                "input_type": "transaction",
                "payload": {
                    "step": 1,
                    "type": "TRANSFER",
                    "amount": 100.0,
                    "oldbalanceOrg": 100.0,
                    "newbalanceOrig": 0.0,
                    "oldbalanceDest": 0.0,
                    "newbalanceDest": 100.0,
                    "isFlaggedFraud": 0,
                },
            },
        ],
    }

    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == "c-integration-02"
    assert data["agent"] == "fusion_agent"
    assert "scam_comm_agent_sms" in data["evidence"]
    assert "scam_comm_agent_url" in data["evidence"]
    assert "fraud_agent" in data["evidence"]

    assert data["overall_risk"] == 85
    assert (
        data["final_verdict"] == "suspicious"
    )  # URL was fraud (scam flag), no fraud flag on transaction -> max risk is 85 -> "suspicious" because 1 scam flag, 0 fraud flag. Wait, logic says: fraud_flags > 0 and scam_flags > 0 -> high_risk_fraud. Otherwise if scam_flags > 0 -> suspicious.
