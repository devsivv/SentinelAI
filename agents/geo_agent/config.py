"""
config.py — Configuration settings for the Geo Intelligence Agent.
"""

from __future__ import annotations

from pydantic import Field
from core.config import AgentBaseConfig


class GeoAgentConfig(AgentBaseConfig):
    """Runtime configuration for the Geo Intelligence Agent.

    All settings can be overridden via environment variables prefixed with `GEO_`.
    """

    confidence_threshold: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
        description="Minimum confidence required to emit a definitive verdict.",
    )

    risk_high_threshold: int = Field(
        default=75,
        ge=0,
        le=100,
        description="Threshold above which case is marked as fraud (crime hotspot).",
    )

    risk_medium_threshold: int = Field(
        default=40,
        ge=0,
        le=100,
        description="Threshold above which case is marked as suspicious.",
    )

    earth_radius_km: float = Field(
        default=6371.0,
        gt=0.0,
        description="Earth radius in kilometers used in Haversine distance.",
    )

    default_radius_km: float = Field(
        default=5.0,
        gt=0.0,
        description="Default radius in kilometers for incident search and density calculation.",
    )

    hotspot_threshold_cases: int = Field(
        default=3,
        gt=0,
        description="Minimum historical incidents within threshold radius to constitute a hotspot.",
    )

    hotspot_threshold_radius: float = Field(
        default=3.0,
        gt=0.0,
        description="Radius in kilometers to evaluate hotspot density.",
    )

    model_config = {"env_prefix": "GEO_", **AgentBaseConfig.model_config}


settings = GeoAgentConfig()
