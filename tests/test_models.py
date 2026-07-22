"""
tests/test_models.py — Unit tests for SentinelAI SQLAlchemy ORM models.
"""

import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.db.base import Base
from backend.models import AgentResult, Case, FusionReport


@pytest.fixture
def in_memory_db():
    """Create an in-memory SQLite database for ORM model testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


def test_models_metadata_registration():
    """Verify that all models are registered with Base.metadata."""
    tables = Base.metadata.tables
    assert "cases" in tables
    assert "agent_results" in tables
    assert "fusion_reports" in tables


def test_case_creation_and_relationships(in_memory_db: Session):
    """Test Case model instantiation, defaults, and relationships."""
    case = Case(
        investigation_type="scam",
        source="citizen_portal",
        metadata_json={"ip": "127.0.0.1", "device": "mobile"},
    )
    in_memory_db.add(case)
    in_memory_db.commit()
    in_memory_db.refresh(case)

    assert isinstance(case.id, uuid.UUID)
    assert case.status == "processing"
    assert case.investigation_type == "scam"
    assert case.source == "citizen_portal"
    assert case.metadata_json == {"ip": "127.0.0.1", "device": "mobile"}
    assert isinstance(case.created_at, datetime)
    assert isinstance(case.updated_at, datetime)

    # Add AgentResult
    agent_result = AgentResult(
        case_id=case.id,
        agent_name="ScamCommAgent",
        verdict="scam",
        confidence=0.95,
        risk_score=90,
        explanation="Phishing URL detected",
        raw_output={"url": "http://scam.example.com"},
    )
    in_memory_db.add(agent_result)

    # Add FusionReport
    fusion_report = FusionReport(
        case_id=case.id,
        final_verdict="HIGH_RISK_SCAM",
        overall_risk=92,
        confidence=0.94,
        explanation="High probability scam attack",
        recommended_action=["BLOCK_URL", "ALERT_VICTIM"],
    )
    in_memory_db.add(fusion_report)
    in_memory_db.commit()

    in_memory_db.refresh(case)
    assert len(case.agent_results) == 1
    assert case.agent_results[0].agent_name == "ScamCommAgent"
    assert case.agent_results[0].verdict == "scam"

    assert case.fusion_report is not None
    assert case.fusion_report.final_verdict == "HIGH_RISK_SCAM"
    assert case.fusion_report.overall_risk == 92
    assert case.fusion_report.recommended_action == ["BLOCK_URL", "ALERT_VICTIM"]


def test_cascade_delete(in_memory_db: Session):
    """Test that deleting a Case cascades and removes associated AgentResult and FusionReport."""
    case = Case(investigation_type="fraud", source="police_dashboard")
    in_memory_db.add(case)
    in_memory_db.commit()

    agent_res = AgentResult(case_id=case.id, agent_name="FraudAgent", verdict="fraud")
    fusion_rep = FusionReport(case_id=case.id, final_verdict="FRAUD_CONFIRMED", overall_risk=85)
    in_memory_db.add_all([agent_res, fusion_rep])
    in_memory_db.commit()

    case_id = case.id
    # Delete case
    in_memory_db.delete(case)
    in_memory_db.commit()

    # Confirm child rows deleted
    deleted_agent_res = in_memory_db.query(AgentResult).filter_by(case_id=case_id).first()
    deleted_fusion_rep = in_memory_db.query(FusionReport).filter_by(case_id=case_id).first()

    assert deleted_agent_res is None
    assert deleted_fusion_rep is None
