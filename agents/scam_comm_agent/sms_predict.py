"""
sms_predict.py — High-level prediction interface for SMS scam detection.

This module is the single entry point for SMS inference.  It orchestrates:

    raw SMS text
        → preprocess_sms()           (here)
        → run_sms_inference()        (sms_model.py)
        → decode labels + verdict    (here)
        → build SMSPredictionResult  (schemas.py)

**No model loading or TF-IDF logic is duplicated here.**
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Optional

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from .config import settings
from .logging import get_logger
from .schemas import SMSPredictionResult
from .sms_model import run_sms_inference

log = get_logger()

# ---------------------------------------------------------------------------
# NLTK resource bootstrap — download silently if not already present
# ---------------------------------------------------------------------------

_NLTK_RESOURCES = [
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("tokenizers/punkt", "punkt"),
    ("corpora/wordnet", "wordnet"),
    ("corpora/omw-1.4", "omw-1.4"),
    ("corpora/stopwords", "stopwords"),
]


def _ensure_nltk_resources() -> None:
    """Download required NLTK data packages if they are missing."""
    for resource_path, resource_name in _NLTK_RESOURCES:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, quiet=True)


_ensure_nltk_resources()

# ---------------------------------------------------------------------------
# Preprocessing (must match training notebook exactly)
# ---------------------------------------------------------------------------

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))

# Label mapping: class index → human-readable string
# The notebook trains label=0 → ham, label=1 → scam
_LABEL_MAP: dict[int, str] = {0: "ham", 1: "scam"}


def _clean_text(text: str) -> str:
    """Apply the exact same cleaning steps used during training.

    Steps (matching ``SMS_Scam.ipynb`` cell ``clean_text``):
    1. Remove URLs (http/https and www-prefixed)
    2. Remove email addresses
    3. Remove phone numbers
    4. Remove non-word/non-space characters
    5. Remove underscores
    6. Remove digits
    7. Collapse whitespace and strip

    Parameters
    ----------
    text:
        Raw SMS message text.

    Returns
    -------
    Cleaned text string.
    """
    # 1. Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)
    # 2. Remove email addresses
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        " ",
        text,
    )
    # 3. Remove phone numbers
    text = re.sub(r"\+?\d[\d\s()-]{7,}\d", " ", text)
    # 4. Remove non-word / non-space characters
    text = re.sub(r"[^\w\s]", " ", text)
    # 5. Remove underscores
    text = re.sub(r"_", " ", text)
    # 6. Remove digits
    text = re.sub(r"\d+", " ", text)
    # 7. Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_sms(text: str) -> str:
    """Full SMS preprocessing pipeline: clean → tokenize → lemmatize → filter.

    Matches ``preprocess_text`` in ``SMS_Scam.ipynb`` exactly:
    - Apply ``_clean_text``
    - NLTK word tokenization
    - Keep only alphabetic tokens not in stop words and length > 1
    - Lemmatize with WordNetLemmatizer
    - Rejoin with spaces

    Parameters
    ----------
    text:
        Raw SMS message text.

    Returns
    -------
    Preprocessed string ready for TF-IDF transformation.

    Raises
    ------
    ValueError
        If the input text is empty or whitespace-only.
    """
    if not text or not text.strip():
        raise ValueError("SMS text must be a non-empty string.")

    cleaned = _clean_text(text)
    tokens = nltk.word_tokenize(cleaned)
    tokens = [
        _lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalpha() and token not in _stop_words and len(token) > 1
    ]
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Public prediction API
# ---------------------------------------------------------------------------


def predict_sms(
    text: str,
    *,
    case_id: str = "unknown",
    model_path: Optional[Path] = None,
    tfidf_path: Optional[Path] = None,
) -> SMSPredictionResult:
    """Run end-to-end SMS scam inference and return a structured result.

    Parameters
    ----------
    text:
        Raw SMS message text.
    case_id:
        Case identifier used in log records.
    model_path:
        Override the model path from settings (used in integration tests).
    tfidf_path:
        Override the TF-IDF path from settings (used in integration tests).

    Returns
    -------
    :class:`SMSPredictionResult`

    Raises
    ------
    ValueError
        If the text is empty or cannot be preprocessed.
    FileNotFoundError
        If model artefacts are missing.
    RuntimeError
        If inference fails.
    """
    t_start = time.perf_counter()
    log.info("[case_id=%s] SMS prediction request received.", case_id)

    # ------------------------------------------------------------------
    # 1. Preprocessing
    # ------------------------------------------------------------------
    try:
        cleaned_text = preprocess_sms(text)
    except ValueError as exc:
        log.warning("[case_id=%s] SMS preprocessing failed: %s", case_id, exc)
        raise

    # ------------------------------------------------------------------
    # 2. Vectorize + model inference → probabilities
    # ------------------------------------------------------------------
    # probabilities shape: (1, 2) — [P(ham), P(scam)]
    probabilities = run_sms_inference(cleaned_text, model_path, tfidf_path)

    ham_prob = float(probabilities[0][0])
    scam_prob = float(probabilities[0][1])

    # ------------------------------------------------------------------
    # 3. Determine predicted class and confidence
    # ------------------------------------------------------------------
    predicted_idx = int(probabilities[0].argmax())
    predicted_class = _LABEL_MAP[predicted_idx]
    confidence = round(float(probabilities[0][predicted_idx]), 6)

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] SMS prediction complete — class='%s', confidence=%.4f, elapsed=%.1f ms.",
        case_id,
        predicted_class,
        confidence,
        elapsed_ms,
    )

    return SMSPredictionResult(
        predicted_class=predicted_class,
        confidence=confidence,
        scam_probability=round(scam_prob, 6),
        ham_probability=round(ham_prob, 6),
        cleaned_text=cleaned_text,
    )


# ---------------------------------------------------------------------------
# Verdict helper
# ---------------------------------------------------------------------------


def build_sms_verdict(result: SMSPredictionResult, case_id: str = "unknown") -> dict:
    """Translate an ``SMSPredictionResult`` into Agent Contract response fields.

    This keeps verdict-mapping logic in one place so any caller (FastAPI route,
    test, CLI) stays thin.

    Returns a **dict** (not a Pydantic model) so callers can embed it directly
    into ``ScamCommAnalysisResponse``.
    """
    confidence = result.confidence
    predicted_class = result.predicted_class.lower()

    if confidence < settings.sms_confidence_threshold:
        verdict = "suspicious"
        category = "none"
        risk_score = 50
        explanation = (
            f"Model confidence ({confidence:.1%}) is below the threshold "
            f"({settings.sms_confidence_threshold:.1%}). Manual review recommended."
        )
    elif predicted_class == "scam":
        verdict = "fraud"
        category = "digital_arrest_scam"
        risk_score = _confidence_to_risk(confidence)
        explanation = f"SMS classified as scam with {confidence:.1%} confidence."
    else:
        verdict = "safe"
        category = "none"
        risk_score = 100 - _confidence_to_risk(confidence)
        explanation = f"SMS classified as legitimate with {confidence:.1%} confidence."

    log.info(
        "[case_id=%s] SMS verdict='%s', risk_score=%d, category='%s'.",
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
