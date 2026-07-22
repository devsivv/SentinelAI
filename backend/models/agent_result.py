"""
backend/models/agent_result.py — SQLAlchemy ORM model for agent evaluation results.

Defines the AgentResult entity representing an individual AI agent's analysis
output associated with an investigation Case.
"""

from datetime import datetime, timezone
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.case import Case


class AgentResult(Base):
    """Represents an individual AI agent's analysis result for a case."""

    __tablename__ = "agent_results"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    agent_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    verdict: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    risk_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    raw_output: Mapped[Optional[Dict[str, Any]]] = mapped_column(
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
        back_populates="agent_results",
    )
