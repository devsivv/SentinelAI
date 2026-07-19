"""
test_graph.py — Unit tests for the Graph Intelligence Agent and its FastAPI endpoint.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from agents.graph_agent.model import get_global_graph
from agents.graph_agent.entity_extractor import (
    normalize_phone,
    normalize_email,
    normalize_bank_account,
    normalize_upi,
    normalize_device,
    normalize_ip,
    normalize_url,
    extract_and_normalize,
)
from agents.graph_agent.schemas import (
    Entity,
    EntityType,
    GraphAnalysisRequest,
    GraphPayload,
    Relationship,
    RelationshipType,
)
from agents.graph_agent.service import analyze_graph

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_graph():
    """Ensure the global in-memory graph is cleared before each test."""
    model = get_global_graph()
    model.clear_graph()
    yield
    model.clear_graph()


def test_normalization():
    """Verify that normalization logic correctly formats identifiers."""
    assert normalize_phone(" +91 99999-88888 ") == "+919999988888"
    assert normalize_phone("09999988888") == "+919999988888"
    assert normalize_phone("9999988888") == "+919999988888"

    assert normalize_email(" User@Example.COM ") == "user@example.com"

    assert normalize_bank_account(" 1234 5678 9012 ") == "123456789012"
    assert normalize_bank_account("acc-1234-xyz") == "ACC-1234-XYZ"

    assert normalize_upi(" Payment@Okltd ") == "payment@okltd"

    assert normalize_device("  device-uuid-123  ") == "DEVICE-UUID-123"

    assert normalize_ip(" 192.168.1.1 ") == "192.168.1.1"

    assert normalize_url("https://www.google.com/search?q=query/") == "google.com/search"
    assert normalize_url("http://phishing-site.net/login.php") == "phishing-site.net/login.php"


def test_extract_and_normalize_explicit():
    """Verify explicit entities and relationships are extracted and normalized."""
    entities = [
        Entity(type=EntityType.PHONE, id="9999988888"),
        Entity(type=EntityType.EMAIL, id="TEST@EMAIL.COM"),
    ]
    relationships = [
        Relationship(
            source_type=EntityType.PHONE,
            source_id="9999988888",
            target_type=EntityType.EMAIL,
            target_id="TEST@EMAIL.COM",
            type=RelationshipType.LINKED_WITH,
        )
    ]

    norm_ents, norm_rels = extract_and_normalize(entities, relationships, None, "c-101")

    # Case node + 2 normalized explicit nodes = 3 nodes
    assert len(norm_ents) == 3
    assert any(e.id == "c-101" and e.type == EntityType.CASE for e in norm_ents)
    assert any(e.id == "+919999988888" and e.type == EntityType.PHONE for e in norm_ents)
    assert any(e.id == "test@email.com" and e.type == EntityType.EMAIL for e in norm_ents)

    # 1 explicit relationship + default LINKED_WITH to connect to the Case node
    # Since phone and email are connected to each other, but not case, we connect them
    assert len(norm_rels) >= 2


def test_extract_and_normalize_raw_evidence():
    """Test dynamic entity extraction from raw evidence schemas (SMS, Transaction, etc.)."""
    raw_evidence = [
        {
            "input_type": "sms",
            "payload": {
                "text": "Call me at +91-98765-43210 or visit https://www.secure-bank.in/login",
                "phone": "+91 99999 11111",
            },
        },
        {
            "input_type": "transaction",
            "payload": {
                "amount": 50000.0,
                "type": "TRANSFER",
                "origin_account": "acc123",
                "destination_account": "acc456",
                "device_id": "dev999",
                "upi_id": "mule@upi",
            },
        },
    ]

    norm_ents, norm_rels = extract_and_normalize([], [], raw_evidence, "c-202")

    # Verify nodes
    ent_ids = {e.id for e in norm_ents}
    assert "c-202" in ent_ids
    assert "+919876543210" in ent_ids
    assert "+919999911111" in ent_ids
    assert "secure-bank.in/login" in ent_ids
    assert "ACC123" in ent_ids
    assert "ACC456" in ent_ids
    assert "DEV999" in ent_ids
    assert "mule@upi" in ent_ids

    # Verify relationships
    rel_types = {r.type for r in norm_rels}
    assert RelationshipType.INVOLVES in rel_types
    assert RelationshipType.USED in rel_types
    assert RelationshipType.TRANSFERRED_TO in rel_types


@pytest.mark.asyncio
async def test_graph_service_verdicts():
    """Test Graph Agent service logic produces expected verdicts under different risk profiles."""
    # 1. Safe Scenario: No shared linkages
    payload_safe = GraphPayload(
        entities=[
            Entity(type=EntityType.VICTIM, id="victim-1"),
            Entity(type=EntityType.PHONE, id="9999900001"),
        ],
        relationships=[
            Relationship(
                source_type=EntityType.VICTIM,
                source_id="victim-1",
                target_type=EntityType.PHONE,
                target_id="9999900001",
                type=RelationshipType.USED,
            )
        ],
    )
    request_safe = GraphAnalysisRequest(case_id="case-safe", payload=payload_safe)
    response_safe = await analyze_graph(request_safe)
    
    assert response_safe.verdict == "safe"
    assert response_safe.risk_score < 40
    assert response_safe.category == "none"

    # 2. Fraud Ring Scenario: Shared phone number across different cases
    # Analyze case 1 with a phone number
    payload_ring1 = GraphPayload(
        entities=[
            Entity(type=EntityType.VICTIM, id="victim-a"),
            Entity(type=EntityType.PHONE, id="9999988888"),
        ],
        relationships=[
            Relationship(
                source_type=EntityType.VICTIM,
                source_id="victim-a",
                target_type=EntityType.PHONE,
                target_id="9999988888",
                type=RelationshipType.USED,
            )
        ],
    )
    await analyze_graph(GraphAnalysisRequest(case_id="case-ring-1", payload=payload_ring1))

    # Analyze case 2 sharing the SAME phone number + includes a suspect node
    payload_ring2 = GraphPayload(
        entities=[
            Entity(type=EntityType.SUSPECT, id="suspect-xyz"),
            Entity(type=EntityType.PHONE, id="9999988888"),
            Entity(type=EntityType.DEVICE, id="dev-shared-1"),
        ],
        relationships=[
            Relationship(
                source_type=EntityType.SUSPECT,
                source_id="suspect-xyz",
                target_type=EntityType.PHONE,
                target_id="9999988888",
                type=RelationshipType.USED,
            ),
            Relationship(
                source_type=EntityType.SUSPECT,
                source_id="suspect-xyz",
                target_type=EntityType.DEVICE,
                target_id="dev-shared-1",
                type=RelationshipType.USED,
            ),
        ],
    )
    
    # Also analyze case 3 sharing the same device to trigger extreme network linkage
    payload_ring3 = GraphPayload(
        entities=[
            Entity(type=EntityType.VICTIM, id="victim-b"),
            Entity(type=EntityType.DEVICE, id="dev-shared-1"),
        ],
        relationships=[
            Relationship(
                source_type=EntityType.VICTIM,
                source_id="victim-b",
                target_type=EntityType.DEVICE,
                target_id="dev-shared-1",
                type=RelationshipType.USED,
            )
        ],
    )
    await analyze_graph(GraphAnalysisRequest(case_id="case-ring-3", payload=payload_ring3))

    response_ring = await analyze_graph(GraphAnalysisRequest(case_id="case-ring-2", payload=payload_ring2))

    assert response_ring.verdict in ("suspicious", "fraud")
    assert response_ring.risk_score >= 40
    assert response_ring.evidence.num_nodes > 0


def test_api_endpoint():
    """Smoke test of the FastAPI endpoint using TestClient."""
    response = client.post(
        "/graph/analyze",
        json={
            "case_id": "c-api-test",
            "input_type": "graph_data",
            "payload": {
                "entities": [
                    {"type": "Victim", "id": "victim-api"},
                    {"type": "UPI ID", "id": "mule@upi"},
                ],
                "relationships": [
                    {
                        "source_type": "Victim",
                        "source_id": "victim-api",
                        "target_type": "UPI ID",
                        "target_id": "mule@upi",
                        "type": "USED",
                    }
                ],
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["agent"] == "graph_agent"
    assert data["case_id"] == "c-api-test"
    assert "verdict" in data
    assert "risk_score" in data
    assert "evidence" in data
    assert data["evidence"]["num_nodes"] >= 3


def test_empty_graph_behavior():
    """Verify analysis behavior when graph is completely empty."""
    from agents.graph_agent.analyzer import run_graph_analysis
    # fixture autouse clears the graph
    evidence = run_graph_analysis("case-empty-test")
    assert evidence.num_nodes == 0
    assert evidence.num_edges == 0
    assert not evidence.connected_components
    assert not evidence.repeated_entities
    assert evidence.network_risk_score == 0.0


@pytest.mark.asyncio
async def test_repeated_individual_detections():
    """Test detailed repeated entity and linkage detections of all supported types."""
    # Build case 1
    payload1 = GraphPayload(
        entities=[
            Entity(type=EntityType.PHONE, id="9999911111"),
            Entity(type=EntityType.URL, id="http://phish1.com"),
            Entity(type=EntityType.UPI, id="user1@upi"),
            Entity(type=EntityType.BANK_ACCOUNT, id="acc111"),
            Entity(type=EntityType.DEVICE, id="dev111"),
            Entity(type=EntityType.EMAIL, id="user1@email.com"),
            Entity(type=EntityType.IP, id="192.168.1.1"),
            Entity(type=EntityType.SUSPECT, id="suspect-john"),
            Entity(type=EntityType.VICTIM, id="victim-alice"),
        ],
        relationships=[]
    )
    await analyze_graph(GraphAnalysisRequest(case_id="case-a", payload=payload1))

    # Build case 2 sharing ALL entities to trigger detections
    payload2 = GraphPayload(
        entities=[
            Entity(type=EntityType.PHONE, id="9999911111"),
            Entity(type=EntityType.URL, id="http://phish1.com"),
            Entity(type=EntityType.UPI, id="user1@upi"),
            Entity(type=EntityType.BANK_ACCOUNT, id="acc111"),
            Entity(type=EntityType.DEVICE, id="dev111"),
            Entity(type=EntityType.EMAIL, id="user1@email.com"),
            Entity(type=EntityType.IP, id="192.168.1.1"),
            Entity(type=EntityType.SUSPECT, id="suspect-john"),
            Entity(type=EntityType.VICTIM, id="victim-alice"),
        ],
        relationships=[]
    )
    res = await analyze_graph(GraphAnalysisRequest(case_id="case-b", payload=payload2))
    evidence = res.evidence

    # Verify each specific repeated list
    assert len(evidence.shared_phones) > 0
    assert len(evidence.shared_urls) > 0
    assert len(evidence.shared_upis) > 0
    assert len(evidence.shared_accounts) > 0
    assert len(evidence.shared_devices) > 0
    assert len(evidence.repeated_identities) > 0

    # Verify connected component and degree centrality
    assert len(evidence.connected_components) > 0
    assert len(evidence.degree_centrality) > 0
    assert evidence.network_risk_score > 50.0


def test_invalid_requests_and_malformed_evidence():
    """Verify validation handles invalid or malformed data correctly."""
    resp_malformed = client.post(
        "/graph/analyze",
        json={
            "case_id": "c-invalid",
            "payload": {
                "entities": [{"type": "InvalidType", "id": "val"}],  # Invalid EntityType
            }
        }
    )
    assert resp_malformed.status_code == 422  # Pydantic validation error


def test_thread_safe_graph_operations():
    """Verify that multiple threads can safely populate the in-memory graph without corruption."""
    import threading
    model = get_global_graph()

    def worker(worker_id: int):
        for i in range(50):
            node_id = f"node_{worker_id}_{i}"
            model.add_entity_node(node_id, EntityType.PHONE.value, {"case_id": f"case_{worker_id}"})
            if i > 0:
                model.add_relationship_edge(f"node_{worker_id}_{i-1}", node_id, RelationshipType.LINKED_WITH.value)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # The graph should have exactly 250 nodes (5 * 50) and 245 edges (5 * 49)
    assert model.G.number_of_nodes() == 250
    assert model.G.number_of_edges() == 245

