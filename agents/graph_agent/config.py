"""
config.py — Configuration for the Graph Intelligence Agent.

All paths and hyperparameters are read from environment variables or YAML
config files so nothing is hardcoded.
"""

from __future__ import annotations

from pydantic import Field
from core.config import AgentBaseConfig


class GraphAgentConfig(AgentBaseConfig):
    """Runtime configuration for the Graph Intelligence Agent.

    Values can be overridden using environment variables prefixed with `GRAPH_`.
    """

    confidence_threshold: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
        description="Minimum confidence required to emit a definitive verdict.",
    )

    risk_high_threshold: int = Field(
        default=70,
        ge=0,
        le=100,
        description="Threshold above which case is marked as fraud.",
    )

    risk_medium_threshold: int = Field(
        default=40,
        ge=0,
        le=100,
        description="Threshold above which case is marked as suspicious.",
    )

    model_config = {"env_prefix": "GRAPH_", **AgentBaseConfig.model_config}


# Module-level singleton
settings = GraphAgentConfig()
