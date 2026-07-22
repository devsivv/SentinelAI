"""
tests/test_repositories.py — Tests for repository layer and orchestrator persistence flow.
"""

import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.db.base import Base
from backend.models import AgentResult, Case, FusionReport
from backend.orchestrator.schemas import EvidenceItem, InvestigateRequest
from backend.orchestrator.service import process_case
from backend.repositories.agent_result_repository import AgentResultRepository
from backend.repositories.case_repository import CaseRepository
from backend.repositories.fusion_report_repository import FusionReportRepository


@pytest.fixture
def db():
    """Create a temporary in-memory database for testing repositories."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def test_create_and_retrieve_case(db: Session):
    """Test CaseRepository.create_case and get_case / list_cases."""
    repo = CaseRepository()
    c = repo.create_case(
        db,
        status="processing",
        investigation_type="sms",
        source="unit_test",
        metadata_json={"user": "test_user"},
    )
    assert c.id is not None
    assert c.status == "processing"
    assert c.investigation_type == "sms"

    retrieved = repo.get_case(db, c.id)
    assert retrieved is not None
    assert retrieved.id == c.id

    all_cases = repo.list_cases(db)
    assert len(all_cases) >= 1
    assert any(item.id == c.id for item in all_cases)


def test_save_and_retrieve_agent_results(db: Session):
    """Test AgentResultRepository.create_results and get_results_by_case."""
    case_repo = CaseRepository()
    c = case_repo.create_case(db, investigation_type="transaction")

    agent_repo = AgentResultRepository()
    results = agent_repo.create_results(
        db,
        case_id=c.id,
        results=[
            {
                "agent": "fraud_agent",
                "verdict": "fraud",
                "confidence": 0.98,
                "risk_score": 95,
                "category": "high_amount_transfer",
                "evidence": {"amount": 1000000},
            }
        ],
    )
    assert len(results) == 1
    assert results[0].agent_name == "fraud_agent"

    retrieved_results = agent_repo.get_results_by_case(db, c.id)
    assert len(retrieved_results) == 1
    assert retrieved_results[0].verdict == "fraud"


def test_save_and_retrieve_fusion_report(db: Session):
    """Test FusionReportRepository.create_report and get_report_by_case."""
    case_repo = CaseRepository()
    c = case_repo.create_case(db, investigation_type="url")

    fusion_repo = FusionReportRepository()
    report = fusion_repo.create_report(
        db,
        case_id=c.id,
        final_verdict="HIGH_RISK_PHISHING",
        overall_risk=88,
        confidence=0.91,
        explanation="Known phishing domain",
        recommended_action=["BLOCK_URL"],
    )
    assert report.id is not None
    assert report.final_verdict == "HIGH_RISK_PHISHING"

    retrieved_report = fusion_repo.get_report_by_case(db, c.id)
    assert retrieved_report is not None
    assert retrieved_report.overall_risk == 88


@pytest.mark.asyncio
async def test_orchestrator_persistence_flow(db: Session):
    """Test that process_case creates Case, AgentResults, and FusionReport in DB."""
    req = InvestigateRequest(
        case_id="test-case-persistence-101",
        evidence=[
            EvidenceItem(
                input_type="sms",
                payload={"text": "URGENT: Verify bank account now."},
            )
        ],
    )

    response = await process_case(req, db=db)
    assert response.case_id == "test-case-persistence-101"

    # Verify Case persisted
    case_repo = CaseRepository()
    db_case = case_repo.get_case(db, "test-case-persistence-101")
    assert db_case is not None
    assert db_case.status == "completed"

    # Verify AgentResult persisted
    agent_repo = AgentResultRepository()
    results = agent_repo.get_results_by_case(db, db_case.id)
    assert len(results) >= 1

    # Verify FusionReport persisted
    fusion_repo = FusionReportRepository()
    fusion_report = fusion_repo.get_report_by_case(db, db_case.id)
    assert fusion_report is not None
    assert fusion_report.final_verdict == response.final_verdict


@pytest.mark.asyncio
async def test_repeated_investigations_create_unique_case_uuids(db: Session):
    """Test running orchestrator twice with same case_id payload creates 2 distinct Case UUIDs."""
    req = InvestigateRequest(
        case_id="same-request-case-id",
        evidence=[
            EvidenceItem(
                input_type="sms",
                payload={"text": "URGENT: Verify account now."},
            )
        ],
    )

    resp1 = await process_case(req, db=db)
    resp2 = await process_case(req, db=db)

    assert resp1.case_id == "same-request-case-id"
    assert resp2.case_id == "same-request-case-id"

    case_repo = CaseRepository()
    all_cases = case_repo.list_cases(db)
    matching_cases = [
        c
        for c in all_cases
        if c.metadata_json and c.metadata_json.get("request_case_id") == "same-request-case-id"
    ]

    assert len(matching_cases) == 2
    assert matching_cases[0].id != matching_cases[1].id

