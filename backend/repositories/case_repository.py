"""
backend/repositories/case_repository.py — Repository for Case entity.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.case import Case

log = logging.getLogger(__name__)


class CaseRepository:
    """Repository handling database operations for Case entities."""

    def create_case(
        self,
        db: Session,
        status: str = "processing",
        investigation_type: str = "multi_modal",
        source: str | None = None,
        metadata_json: dict[str, Any] | None = None,
        request_case_id: str | None = None,
    ) -> Case:
        """Create and persist a new investigation Case with a fresh unique UUID."""
        meta = dict(metadata_json) if metadata_json else {}
        if request_case_id and "request_case_id" not in meta:
            meta["request_case_id"] = str(request_case_id)

        case = Case(
            id=uuid.uuid4(),  # Always generate a fresh random UUID primary key
            status=status,
            investigation_type=investigation_type,
            source=source,
            metadata_json=meta if meta else None,
        )
        try:
            db.add(case)
            db.commit()
            db.refresh(case)
            return case
        except Exception as exc:
            db.rollback()
            log.error("Failed to create case: %s", exc)
            raise

    def get_case(self, db: Session, case_id: str | uuid.UUID) -> Case | None:
        """Retrieve a Case by primary key UUID or business request_case_id."""
        if isinstance(case_id, uuid.UUID):
            return db.scalar(select(Case).where(Case.id == case_id))

        try:
            parsed_id = uuid.UUID(str(case_id))
            c = db.scalar(select(Case).where(Case.id == parsed_id))
            if c:
                return c
        except ValueError:
            pass

        # Query by business request_case_id in metadata_json
        stmt = select(Case).order_by(Case.created_at.desc())
        for c in db.scalars(stmt).all():
            if c.metadata_json and c.metadata_json.get("request_case_id") == str(case_id):
                return c
        return None

    def list_cases(self, db: Session, limit: int = 100, offset: int = 0) -> list[Case]:
        """List Cases ordered by created_at descending."""
        stmt = select(Case).order_by(Case.created_at.desc()).limit(limit).offset(offset)
        return list(db.scalars(stmt).all())
