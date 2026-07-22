"""
backend/repositories/agent_result_repository.py — Repository for AgentResult entity.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.agent_result import AgentResult

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


class AgentResultRepository:
    """Repository handling database operations for AgentResult entities."""

    def create_results(
        self,
        db: Session,
        case_id: str | uuid.UUID,
        results: list[dict[str, Any] | Any],
    ) -> list[AgentResult]:
        """Bulk create AgentResult records for a given case."""
        parsed_case_id = _resolve_case_id(db, case_id)
        created_records: list[AgentResult] = []

        for item in results:
            if hasattr(item, "model_dump"):
                data = item.model_dump(mode="json")
            elif isinstance(item, dict):
                data = item
            else:
                data = getattr(item, "__dict__", {})

            agent_name = str(data.get("agent") or data.get("agent_name") or "unknown")
            verdict = data.get("verdict")
            confidence = data.get("confidence")
            risk_score = data.get("risk_score")
            explanation = data.get("category") or data.get("explanation")
            raw_output = data.get("evidence") or data.get("raw_output")

            rec = AgentResult(
                id=uuid.uuid4(),
                case_id=parsed_case_id,
                agent_name=agent_name,
                verdict=verdict,
                confidence=confidence,
                risk_score=risk_score,
                explanation=explanation,
                raw_output=raw_output,
            )
            db.add(rec)
            created_records.append(rec)

        try:
            db.commit()
            for rec in created_records:
                db.refresh(rec)
            return created_records
        except Exception as exc:
            db.rollback()
            log.error("Failed to save agent results for case %s: %s", case_id, exc)
            raise

    def get_results_by_case(
        self, db: Session, case_id: str | uuid.UUID
    ) -> list[AgentResult]:
        """Retrieve all AgentResult records for a given case."""
        try:
            parsed_case_id = _resolve_case_id(db, case_id)
        except ValueError:
            return []

        stmt = (
            select(AgentResult)
            .where(AgentResult.case_id == parsed_case_id)
            .order_by(AgentResult.created_at.asc())
        )
        return list(db.scalars(stmt).all())
