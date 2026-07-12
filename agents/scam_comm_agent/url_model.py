"""
url_model.py — Singleton model loader and raw inference for phishing URL detection.

Responsibilities
----------------
- Load the trained XGBoost phishing model from disk once (lazy).
- Thread-safe via double-checked locking.
- Expose ``run_url_inference`` which accepts a feature dict/DataFrame
  and returns class probabilities.

This module contains **no feature extraction logic** (that lives in url_predict.py)
and **no business-level scoring** (that lives in url_predict.py).
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

_url_lock = threading.Lock()
_url_model: Optional[Any] = None  # XGBoost classifier


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


def get_url_model(path: Optional[Path] = None) -> Any:
    """Return the singleton phishing URL model, loading it on first call.

    Thread-safe: concurrent callers block until the first load completes.

    Parameters
    ----------
    path:
        Override the default model path from settings (used in tests).

    Returns
    -------
    A fitted XGBoost classifier with ``predict_proba`` support.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist at the resolved path.
    """
    global _url_model  # noqa: PLW0603

    if _url_model is not None:
        return _url_model

    with _url_lock:
        # Double-checked locking: another thread may have loaded while waiting.
        if _url_model is None:
            resolved = path or settings.phishing_model_path
            if not resolved.exists():
                raise FileNotFoundError(
                    f"Phishing model file not found at '{resolved}'. "
                    "Verify the path in configs/models.yaml or set "
                    "SCAM_COMM_PHISHING_MODEL_PATH."
                )
            log.info("Loading phishing URL model from '%s' …", resolved)
            _url_model = joblib.load(str(resolved))
            log.info("Phishing URL model loaded successfully.")

    return _url_model


def reset_url_model_cache() -> None:
    """Clear the in-process singleton — used in tests only.

    Calling this in production would force a cold reload on the next request.
    """
    global _url_model  # noqa: PLW0603
    with _url_lock:
        _url_model = None
    log.debug("Phishing URL model cache cleared.")


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------


def run_url_inference(
    feature_vector: np.ndarray,
    model_path: Optional[Path] = None,
) -> np.ndarray:
    """Run the phishing URL model and return class probabilities.

    Parameters
    ----------
    feature_vector:
        2-D array of shape ``(1, n_features)`` built from ``extract_url_features``.
    model_path:
        Override the model path from settings (used in tests).

    Returns
    -------
    ``np.ndarray`` of shape ``(1, 2)`` — probability for [safe, phishing] classes.

    Raises
    ------
    FileNotFoundError
        If the model file is missing.
    RuntimeError
        If inference fails.
    """
    model = get_url_model(model_path)

    try:
        probabilities: np.ndarray = model.predict_proba(feature_vector)
    except Exception as exc:
        log.exception("URL inference failed: %s", exc)
        raise RuntimeError(f"Phishing URL model inference failed: {exc}") from exc

    log.debug("URL inference complete — probabilities shape: %s.", probabilities.shape)
    return probabilities
