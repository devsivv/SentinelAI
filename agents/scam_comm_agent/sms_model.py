"""
sms_model.py — Singleton model loader and raw inference for SMS scam detection.

Responsibilities
----------------
- Load the trained CalibratedClassifierCV(LinearSVC) from disk once (lazy).
- Load the fitted TF-IDF vectorizer from disk once (lazy).
- Both loaders are thread-safe via double-checked locking.
- Expose ``run_sms_inference`` which accepts preprocessed text and returns
  class probabilities directly.

This module contains **no preprocessing logic** (that lives in sms_predict.py)
and **no business-level scoring** (that lives in sms_predict.py).
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Optional

import numpy as np

from core.loader import load_joblib_model

from .config import settings
from .logging import get_logger

log = get_logger()

# ---------------------------------------------------------------------------
# Thread-safe lazy singleton state
# ---------------------------------------------------------------------------

_sms_lock = threading.Lock()
_sms_model: Optional[Any] = None  # CalibratedClassifierCV

_tfidf_lock = threading.Lock()
_tfidf: Optional[Any] = None  # TfidfVectorizer


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


def get_sms_model(path: Optional[Path] = None) -> Any:
    """Return the singleton SMS model, loading it on first call.

    Thread-safe: concurrent callers block until the first load completes.

    Parameters
    ----------
    path:
        Override the default model path from settings (used in tests).

    Returns
    -------
    A fitted ``CalibratedClassifierCV`` (wrapping ``LinearSVC``).

    Raises
    ------
    FileNotFoundError
        If the model file does not exist at the resolved path.
    """
    return load_joblib_model(
        path or settings.sms_model_path,
        cache_dict=globals(),
        cache_key="_sms_model",
        lock=_sms_lock,
        label="SMS model file",
    )


def get_tfidf(path: Optional[Path] = None) -> Any:
    """Return the singleton TF-IDF vectorizer, loading it on first call.

    Thread-safe: concurrent callers block until the first load completes.

    Parameters
    ----------
    path:
        Override the default TF-IDF path from settings (used in tests).

    Returns
    -------
    A fitted ``TfidfVectorizer``.

    Raises
    ------
    FileNotFoundError
        If the vectorizer file does not exist at the resolved path.
    """
    return load_joblib_model(
        path or settings.tfidf_path,
        cache_dict=globals(),
        cache_key="_tfidf",
        lock=_tfidf_lock,
        label="TF-IDF vectorizer",
    )


def reset_sms_model_cache() -> None:
    """Clear the in-process singletons — used in tests only.

    Calling this in production would force a cold reload on the next request.
    """
    global _sms_model, _tfidf  # noqa: PLW0603
    with _sms_lock:
        _sms_model = None
    with _tfidf_lock:
        _tfidf = None
    log.debug("SMS model and TF-IDF cache cleared.")


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------


def run_sms_inference(
    cleaned_text: str,
    model_path: Optional[Path] = None,
    tfidf_path: Optional[Path] = None,
) -> np.ndarray:
    """Vectorize text and run the SMS model, returning class probabilities.

    Parameters
    ----------
    cleaned_text:
        Preprocessed text string (already tokenized, lemmatized, etc.).
    model_path:
        Override the SMS model path from settings (used in tests).
    tfidf_path:
        Override the TF-IDF path from settings (used in tests).

    Returns
    -------
    ``np.ndarray`` of shape ``(1, 2)`` — probability for [ham, scam] classes.

    Raises
    ------
    FileNotFoundError
        If model or vectorizer files are missing.
    RuntimeError
        If inference fails.
    """
    tfidf = get_tfidf(tfidf_path)
    model = get_sms_model(model_path)

    try:
        vector = tfidf.transform([cleaned_text])
        probabilities: np.ndarray = model.predict_proba(vector)
    except Exception as exc:
        log.exception("SMS inference failed: %s", exc)
        raise RuntimeError(f"SMS model inference failed: {exc}") from exc

    log.debug("SMS inference complete — probabilities shape: %s.", probabilities.shape)
    return probabilities
