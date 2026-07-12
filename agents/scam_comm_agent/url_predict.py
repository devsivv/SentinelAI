"""
url_predict.py — High-level prediction interface for phishing URL detection.

This module is the single entry point for URL inference.  It orchestrates:

    raw URL string
        → extract_url_features()     (here — matches training notebook exactly)
        → run_url_inference()        (url_model.py)
        → decode labels + verdict    (here)
        → build URLPredictionResult  (schemas.py)

**No model loading logic is duplicated here.**
"""

from __future__ import annotations

import math
import re
import time
from collections import Counter
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import numpy as np

from .config import settings
from .logging import get_logger
from .schemas import URLPredictionResult
from .url_model import run_url_inference

log = get_logger()

# ---------------------------------------------------------------------------
# Feature extraction constants (must match training notebook exactly)
# ---------------------------------------------------------------------------

# From phising.ipynb cell defining SUSPICIOUS_KEYWORDS
_SUSPICIOUS_KEYWORDS: list[str] = [
    "login", "verify", "update", "secure", "account",
    "bank", "confirm", "signin", "password", "paypal",
    "webscr", "ebayisapi", "wp", "admin", "auth",
    "token", "wallet", "invoice", "billing", "support",
]

# Ordered feature names — must match the column order used during training
_FEATURE_NAMES: list[str] = [
    "url_length",
    "domain_length",
    "path_length",
    "query_length",
    "fragment_length",
    "num_dots",
    "num_hyphens",
    "num_underscores",
    "num_slashes",
    "num_question_marks",
    "num_equal",
    "num_digits",
    "num_special_chars",
    "num_subdomains",
    "https",
    "has_ip",
    "entropy",
    "suspicious_keyword_count",
]

# Label mapping: class index → human-readable string
# Training notebook: label=0 → safe (not spam), label=1 → phishing (spam)
_LABEL_MAP: dict[int, str] = {0: "safe", 1: "phishing"}


# ---------------------------------------------------------------------------
# Feature extraction (matches phising.ipynb exactly)
# ---------------------------------------------------------------------------


def _shannon_entropy(text: str) -> float:
    """Compute Shannon entropy of a string.

    Matches ``shannon_entropy`` in ``phising.ipynb``.

    Parameters
    ----------
    text:
        Input string.

    Returns
    -------
    Float entropy value (0.0 for empty strings).
    """
    if not text:
        return 0.0
    counts = Counter(text)
    probabilities = [count / len(text) for count in counts.values()]
    return -sum(p * math.log2(p) for p in probabilities)


def extract_url_features(url: str) -> dict[str, Any]:
    """Extract the 18 hand-crafted features used during model training.

    Matches ``extract_features`` in ``phising.ipynb`` exactly.

    Parameters
    ----------
    url:
        URL string to analyse.

    Returns
    -------
    Dictionary mapping feature name → value.
    """
    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path
    query = parsed.query
    fragment = parsed.fragment

    features: dict[str, Any] = {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "query_length": len(query),
        "fragment_length": len(fragment),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_underscores": url.count("_"),
        "num_slashes": url.count("/"),
        "num_question_marks": url.count("?"),
        "num_equal": url.count("="),
        "num_digits": sum(c.isdigit() for c in url),
        "num_special_chars": len(re.findall(r"[^A-Za-z0-9]", url)),
        "num_subdomains": max(len(domain.split(".")) - 2, 0),
        "https": int(parsed.scheme == "https"),
        "has_ip": int(re.search(r"(\d{1,3}\.){3}\d{1,3}", domain) is not None),
        "entropy": _shannon_entropy(url),
        "suspicious_keyword_count": sum(
            keyword in url.lower() for keyword in _SUSPICIOUS_KEYWORDS
        ),
    }

    return features


def preprocess_url(url: str) -> tuple[dict[str, Any], np.ndarray]:
    """Validate the URL, extract features, and build the model input vector.

    Parameters
    ----------
    url:
        Raw URL string.

    Returns
    -------
    features:
        Dict of extracted features (for evidence logging).
    feature_vector:
        2-D ``np.ndarray`` of shape ``(1, 18)`` ready for the model.

    Raises
    ------
    ValueError
        If the URL is empty or has no parseable scheme+netloc.
    """
    if not url or not url.strip():
        raise ValueError("URL must be a non-empty string.")

    url = url.strip()
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(
            f"Malformed URL — missing scheme or host: '{url}'. "
            "Expected format: 'https://example.com/path'."
        )

    features = extract_url_features(url)

    # Build the feature vector in the exact column order used during training
    vector = np.array(
        [[features[name] for name in _FEATURE_NAMES]],
        dtype=np.float64,
    )

    return features, vector


# ---------------------------------------------------------------------------
# Public prediction API
# ---------------------------------------------------------------------------


def predict_url(
    url: str,
    *,
    case_id: str = "unknown",
    model_path: Optional[Path] = None,
) -> URLPredictionResult:
    """Run end-to-end phishing URL inference and return a structured result.

    Parameters
    ----------
    url:
        Raw URL string.
    case_id:
        Case identifier used in log records.
    model_path:
        Override the model path from settings (used in integration tests).

    Returns
    -------
    :class:`URLPredictionResult`

    Raises
    ------
    ValueError
        If the URL is empty or malformed.
    FileNotFoundError
        If model artefacts are missing.
    RuntimeError
        If inference fails.
    """
    t_start = time.perf_counter()
    log.info("[case_id=%s] URL prediction request received.", case_id)

    # ------------------------------------------------------------------
    # 1. Feature extraction
    # ------------------------------------------------------------------
    try:
        features, feature_vector = preprocess_url(url)
    except ValueError as exc:
        log.warning("[case_id=%s] URL preprocessing failed: %s", case_id, exc)
        raise

    # ------------------------------------------------------------------
    # 2. Model inference → probabilities
    # ------------------------------------------------------------------
    # probabilities shape: (1, 2) — [P(safe), P(phishing)]
    probabilities = run_url_inference(feature_vector, model_path)

    safe_prob = float(probabilities[0][0])
    phishing_prob = float(probabilities[0][1])

    # ------------------------------------------------------------------
    # 3. Determine predicted class and confidence
    # ------------------------------------------------------------------
    predicted_idx = int(probabilities[0].argmax())
    predicted_class = _LABEL_MAP[predicted_idx]
    confidence = round(float(probabilities[0][predicted_idx]), 6)

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] URL prediction complete — class='%s', confidence=%.4f, elapsed=%.1f ms.",
        case_id,
        predicted_class,
        confidence,
        elapsed_ms,
    )

    return URLPredictionResult(
        predicted_class=predicted_class,
        confidence=confidence,
        phishing_probability=round(phishing_prob, 6),
        safe_probability=round(safe_prob, 6),
        features=features,
    )


# ---------------------------------------------------------------------------
# Verdict helper
# ---------------------------------------------------------------------------


def build_url_verdict(result: URLPredictionResult, case_id: str = "unknown") -> dict:
    """Translate a ``URLPredictionResult`` into Agent Contract response fields.

    This keeps verdict-mapping logic in one place so any caller (FastAPI route,
    test, CLI) stays thin.

    Returns a **dict** (not a Pydantic model) so callers can embed it directly
    into ``ScamCommAnalysisResponse``.
    """
    confidence = result.confidence
    predicted_class = result.predicted_class.lower()

    if confidence < settings.url_confidence_threshold:
        verdict = "suspicious"
        category = "none"
        risk_score = 50
        explanation = (
            f"Model confidence ({confidence:.1%}) is below the threshold "
            f"({settings.url_confidence_threshold:.1%}). Manual review recommended."
        )
    elif predicted_class == "phishing":
        verdict = "fraud"
        category = "phishing"
        risk_score = _confidence_to_risk(confidence)
        explanation = (
            f"URL classified as phishing with {confidence:.1%} confidence."
        )
    else:
        verdict = "safe"
        category = "none"
        risk_score = 100 - _confidence_to_risk(confidence)
        explanation = (
            f"URL classified as safe with {confidence:.1%} confidence."
        )

    log.info(
        "[case_id=%s] URL verdict='%s', risk_score=%d, category='%s'.",
        case_id,
        verdict,
        risk_score,
        category,
    )

    return {
        "verdict": verdict,
        "confidence": confidence,
        "risk_score": risk_score,
        "category": category,
        "explanation": explanation,
    }


def _confidence_to_risk(confidence: float) -> int:
    """Map model confidence in [0, 1] to an integer risk score in [0, 100]."""
    return int(round(confidence * 100))
