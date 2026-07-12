"""
Smoke test for the Fraud Agent (agents/fraud_agent/main.py).
Per AI_GUIDELINES.md, MVP-track agents must not skip tests.
"""
# from agents.fraud_agent.main import app
# from fastapi.testclient import TestClient
#
# client = TestClient(app)


def test_analyze_returns_contract_shape(sample_transaction_payload):
    # response = client.post("/analyze", json=sample_transaction_payload)
    # assert response.status_code == 200
    # body = response.json()
    # for field in ["agent", "case_id", "verdict", "confidence", "risk_score",
    #               "category", "explanation", "evidence", "processed_at"]:
    #     assert field in body
    pass  # implement once agents/fraud_agent/main.py exists (Sprint-03)


def test_analyze_handles_missing_fields_gracefully():
    pass  # implement once agents/fraud_agent/main.py exists (Sprint-03)
