"""
backend/models/case.py — SQLAlchemy ORM model for investigation cases.

Defines the core Case entity representing an investigation request submitted
to SentinelAI.
"""

from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.agent_result import AgentResult
    from backend.models.fusion_report import FusionReport


class Case(Base):
    """Represents an investigation case submitted to SentinelAI."""

    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="processing",
        index=True,
    )
    investigation_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    source: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(
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
    agent_results: Mapped[List["AgentResult"]] = relationship(
        "AgentResult",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    fusion_report: Mapped[Optional["FusionReport"]] = relationship(
        "FusionReport",
        back_populates="case",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
