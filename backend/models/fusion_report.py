"""
backend/models/fusion_report.py — SQLAlchemy ORM model for fusion reports.

Defines the FusionReport entity representing the synthesized intelligence report
for an investigation Case.
"""

from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.case import Case


class FusionReport(Base):
    """Represents the synthesized final fusion report for a case."""

    __tablename__ = "fusion_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    final_verdict: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    overall_risk: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    recommended_action: Mapped[Optional[Union[List[Any], Dict[str, Any]]]] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="fusion_report",
    )
