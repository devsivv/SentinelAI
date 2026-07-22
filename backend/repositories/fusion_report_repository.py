"""
backend/repositories/fusion_report_repository.py — Repository for FusionReport entity.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.fusion_report import FusionReport

log = logging.getLogger(__name__)


def _resolve_case_id(db: Session, case_id: str | uuid.UUID) -> uuid.UUID:
    """Resolve a case_id (UUID or string) to a valid Case primary key UUID."""
    if isinstance(case_id, uuid.UUID):
        return case_id
    try:
        return uuid.UUID(str(case_id))
    except ValueError:
        from backend.repositories.case_repository import CaseRepository

        c = CaseRepository().get_case(db, case_id)
        if c:
            return c.id
        raise ValueError(f"Cannot resolve case_id '{case_id}' to a valid Case UUID.")


class FusionReportRepository:
    """Repository handling database operations for FusionReport entities."""

    def create_report(
        self,
        db: Session,
        case_id: str | uuid.UUID,
        final_verdict: str | None = None,
        overall_risk: int | None = None,
        confidence: float | None = None,
        explanation: str | None = None,
        recommended_action: list[Any] | dict[str, Any] | None = None,
    ) -> FusionReport:
        """Create and persist a FusionReport record for a case."""
        parsed_case_id = _resolve_case_id(db, case_id)
        report = FusionReport(
            id=uuid.uuid4(),
            case_id=parsed_case_id,
            final_verdict=final_verdict,
            overall_risk=overall_risk,
            confidence=confidence,
            explanation=explanation,
            recommended_action=recommended_action,
        )
        try:
            db.add(report)
            db.commit()
            db.refresh(report)
            return report
        except Exception as exc:
            db.rollback()
            log.error("Failed to save fusion report for case %s: %s", case_id, exc)
            raise

    def get_report_by_case(
        self, db: Session, case_id: str | uuid.UUID
    ) -> FusionReport | None:
        """Retrieve FusionReport for a given case."""
        try:
            parsed_case_id = _resolve_case_id(db, case_id)
        except ValueError:
            return None

        stmt = select(FusionReport).where(FusionReport.case_id == parsed_case_id)
        return db.scalar(stmt)
