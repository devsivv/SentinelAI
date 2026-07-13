"""
core/exceptions.py — Shared exception hierarchy for SentinelAI.

All agents raise standard Python exceptions (FileNotFoundError, ValueError,
RuntimeError) at their call sites.  This module defines named subclasses so
callers can catch sentinel-specific errors independently of the built-in
hierarchy if needed in the future.

No existing raise-sites are modified in Phase 2.4; these classes are provided
for future use and as part of the shared infrastructure contract.
"""

from __future__ import annotations


class SentinelAIError(Exception):
    """Root exception for all SentinelAI application errors."""


class ModelNotFoundError(FileNotFoundError, SentinelAIError):
    """Raised when a required model artefact cannot be found on disk."""


class InvalidInputError(ValueError, SentinelAIError):
    """Raised when agent input fails validation (malformed, out-of-range, etc.)."""


class InferenceError(RuntimeError, SentinelAIError):
    """Raised when a model forward/predict pass fails at runtime."""


class ConfigurationError(ValueError, SentinelAIError):
    """Raised when agent configuration is invalid or incomplete."""
