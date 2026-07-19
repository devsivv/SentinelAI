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
    assert "graph_agent" in data["evidence"]  # Automatically executed on raw evidence

    assert data["overall_risk"] == 85
    assert data["final_verdict"] == "suspicious"


def test_investigate_case_with_currency_and_graph(monkeypatch):
    """Test orchestrator endpoint with currency and explicit graph data."""
    # Mock prediction call for currency to avoid ML loading
    from agents.currency_agent.schemas import PredictionResult
    def mock_predict(*args, **kwargs):
        return PredictionResult(
            predicted_class="fake",
            confidence=0.98,
            probabilities={"fake": 0.98, "real": 0.02},
            image_size=(224, 224),
        )
    import sys
    currency_predict_module = sys.modules["agents.currency_agent.predict"]
    monkeypatch.setattr(currency_predict_module, "predict", mock_predict)

    payload = {
        "case_id": "c-integration-03",
        "evidence": [
            {
                "input_type": "currency",
                "payload": {
                    "image_bytes": "ZmFrZV9pbWFnZV9ieXRlcw=="  # base64 for 'fake_image_bytes'
                }
            },
            {
                "input_type": "graph_data",
                "payload": {
                    "entities": [
                        {"type": "Victim", "id": "vic-99"},
                        {"type": "Phone Number", "id": "9999988888"}
                    ],
                    "relationships": [
                        {
                            "source_type": "Victim",
                            "source_id": "vic-99",
                            "target_type": "Phone Number",
                            "target_id": "9999988888",
                            "type": "USED"
                        }
                    ]
                }
            }
        ]
    }

    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == "c-integration-03"
    assert "currency_agent" in data["evidence"]
    assert "graph_agent" in data["evidence"]
    assert data["evidence"]["currency_agent"]["verdict"] == "fraud"
    assert data["evidence"]["graph_agent"]["verdict"] == "safe"


def test_orchestrator_partial_failure_graph(monkeypatch):
    """Verify that Orchestrator handles a crash in the Graph Agent service layer gracefully."""
    # Mock graph agent service to raise an exception
    async def mock_analyze_graph(*args, **kwargs):
        raise RuntimeError("In-memory NetworkX DB corrupted")

    import sys
    graph_service = sys.modules["agents.graph_agent.service"]
    monkeypatch.setattr(graph_service, "analyze_graph", mock_analyze_graph)

    payload = {
        "case_id": "c-integration-fail-graph",
        "evidence": [
            {"input_type": "sms", "payload": {"text": "Hello World"}}
        ]
    }
    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "c-integration-fail-graph"
    assert "graph_agent" not in data["evidence"]


def test_investigate_case_with_geo(monkeypatch):
    """Verify that Orchestrator maps 'location' input to Geo Agent and fuses results."""
    async def mock_process_sms(*args, **kwargs):
        return AgentResult(
            agent=AgentType.SCAM_SMS,
            case_id="c-integration-geo-01",
            verdict="fraud",
            confidence=0.9,
            risk_score=90,
            category="phishing",
            evidence={},
        )
    monkeypatch.setattr("backend.orchestrator.service._process_sms", mock_process_sms)

    payload = {
        "case_id": "c-integration-geo-01",
        "evidence": [
            {
                "input_type": "sms",
                "payload": {
                    "text": "WINNER! You won 1 Crore Cash. Claim now at http://win-scam.com"
                }
            },
            {
                "input_type": "location",
                "payload": {
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "radius_km": 5.0
                }
            }
        ]
    }
    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "c-integration-geo-01"
    
    # Both agents must exist in evidence
    assert "scam_comm_agent_sms" in data["evidence"]
    assert "geo_agent" in data["evidence"]

    # Verify verdict matching (scam sms is fraud -> suspicious verdict overall)
    assert data["final_verdict"] == "suspicious"
    # Core sms has risk 90. Geo has risk 100 (verdict: fraud). 
    # Fraud verdict on geo adds +5 to overall risk -> 90 + 5 = 95
    assert data["overall_risk"] == 95
    assert "Contextual Geo Alert" in data["narrative"]


def test_orchestrator_partial_failure_geo(monkeypatch):
    """Verify that Orchestrator handles a crash in the Geo Agent service layer gracefully."""
    async def mock_analyze_location(*args, **kwargs):
        raise RuntimeError("In-memory database lock timeout")

    import sys
    geo_service = sys.modules["agents.geo_agent.service"]
    monkeypatch.setattr(geo_service, "analyze_location", mock_analyze_location)

    payload = {
        "case_id": "c-integration-fail-geo",
        "evidence": [
            {
                "input_type": "sms",
                "payload": {
                    "text": "WINNER! You won 1 Crore Cash. Claim now at http://win-scam.com"
                }
            },
            {
                "input_type": "location",
                "payload": {
                    "latitude": 12.9716,
                    "longitude": 77.5946
                }
            }
        ]
    }
    response = client.post("/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "c-integration-fail-geo"
    # SMS agent ran successfully, Geo agent failed silently
    assert "scam_comm_agent_sms" in data["evidence"]
    assert "geo_agent" not in data["evidence"]


def test_fusion_geo_modifiers():
    """Verify directly that aggregate_risk uses Geo Agent results as contextual modifiers only."""
    from backend.fusion_agent.logic import aggregate_risk
    from backend.fusion_agent.schemas import AgentResult

    # Case A: SMS fraud (risk 80) + Geo fraud (risk 100) -> overall risk 85 (+5 boost)
    res_sms = AgentResult(
        agent="scam_comm_agent_sms",
        case_id="case-test",
        verdict="fraud",
        confidence=0.9,
        risk_score=80,
        category="phishing",
        evidence={}
    )
    res_geo_fraud = AgentResult(
        agent="geo_agent",
        case_id="case-test",
        verdict="fraud",
        confidence=0.9,
        risk_score=100,
        category="crime_hotspot",
        evidence={}
    )
    verdict_fraud = aggregate_risk([res_sms, res_geo_fraud])
    assert verdict_fraud.overall_risk == 85
    assert verdict_fraud.final_verdict == "suspicious"  # Core sms only -> suspicious

    # Case B: SMS fraud (risk 80) + Geo safe (risk 0) -> overall risk 75 (-5 reduction)
    res_geo_safe = AgentResult(
        agent="geo_agent",
        case_id="case-test",
        verdict="safe",
        confidence=0.9,
        risk_score=0,
        category="none",
        evidence={}
    )
    verdict_safe = aggregate_risk([res_sms, res_geo_safe])
    assert verdict_safe.overall_risk == 75
    assert verdict_safe.final_verdict == "suspicious"



