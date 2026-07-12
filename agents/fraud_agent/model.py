"""
model.py — Singleton model loader and raw inference for fraud detection.

Responsibilities
----------------
- Load the trained XGBoost model from disk once (lazy).
- Thread-safe via double-checked locking.
- Expose ``run_fraud_inference`` which accepts a prepared feature array and
  returns class probabilities directly.

This module contains **no feature engineering** (that lives in predict.py)
and **no business-level scoring** (that lives in predict.py).
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Optional

import joblib
import numpy as np

from .config import settings
from .logging import get_logger

log = get_logger()

# ---------------------------------------------------------------------------
# Thread-safe lazy singleton state
# ---------------------------------------------------------------------------

_model_lock = threading.Lock()
_model: Optional[Any] = None  # XGBClassifier


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


def get_fraud_model(path: Optional[Path] = None) -> Any:
    """Return the singleton XGBoost fraud model, loading it on first call.

    Thread-safe: concurrent callers block until the first load completes.

    Parameters
    ----------
    path:
        Override the default model path from settings (used in tests).

    Returns
    -------
    A fitted ``XGBClassifier`` with ``predict_proba`` support.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist at the resolved path.
    """
    global _model  # noqa: PLW0603

    if _model is not None:
        return _model

    with _model_lock:
        # Double-checked locking: another thread may have loaded while waiting.
        if _model is None:
            resolved = path or settings.model_path
            if not resolved.exists():
                raise FileNotFoundError(
                    f"Fraud model file not found at '{resolved}'. "
                    "Verify the path in configs/models.yaml or set FRAUD_MODEL_PATH."
                )
            log.info("Loading fraud detection model from '%s' …", resolved)
            _model = joblib.load(str(resolved))
            log.info("Fraud detection model loaded successfully.")

    return _model


def reset_model_cache() -> None:
    """Clear the in-process singleton — used in tests only.

    Calling this in production would force a cold reload on the next request.
    """
    global _model  # noqa: PLW0603
    with _model_lock:
        _model = None
    log.debug("Fraud model cache cleared.")


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------


def run_fraud_inference(
    feature_vector: np.ndarray,
    model_path: Optional[Path] = None,
) -> np.ndarray:
    """Run the fraud model and return class probabilities.

    Parameters
    ----------
    feature_vector:
        2-D array of shape ``(1, 18)`` built from ``prepare_features`` in
        predict.py, with columns in the exact order expected by the model.
    model_path:
        Override the model path from settings (used in tests).

    Returns
    -------
    ``np.ndarray`` of shape ``(1, 2)`` — probability for [safe, fraud] classes.
    Index 0 = P(safe), Index 1 = P(fraud).

    Raises
    ------
    FileNotFoundError
        If the model file is missing.
    RuntimeError
        If inference fails.
    """
    model = get_fraud_model(model_path)

    try:
        probabilities: np.ndarray = model.predict_proba(feature_vector)
    except Exception as exc:
        log.exception("Fraud inference failed: %s", exc)
        raise RuntimeError(f"Fraud model inference failed: {exc}") from exc

    log.debug("Fraud inference complete — probabilities shape: %s.", probabilities.shape)
    return probabilities
