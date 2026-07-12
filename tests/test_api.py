"""
Smoke tests for the Orchestrator (backend/orchestrator/main.py).
Verifies the contract shape, not model accuracy — accuracy is validated
per-agent in its own test file.
"""
# from backend.orchestrator.main import app
# from fastapi.testclient import TestClient
#
# client = TestClient(app)


def test_investigate_returns_fusion_report(sample_sms_payload):
    """POST /investigate should return a fusion_reports-shaped response."""
    # response = client.post("/investigate", json={
    #     "case_id": sample_sms_payload["case_id"],
    #     "evidence": [sample_sms_payload],
    # })
    # assert response.status_code == 200
    # body = response.json()
    # assert "final_verdict" in body
    # assert "overall_risk" in body
    # assert "recommended_action" in body
    pass  # implement once backend/orchestrator/main.py exists (Sprint-09)


def test_investigate_degrades_gracefully_on_agent_failure():
    """If one agent errors/times out, Orchestrator should still return a
    partial fusion result rather than a 500 — required by Sprint-09 scope."""
    pass  # implement once backend/orchestrator/main.py exists (Sprint-09)
