"""
predict.py — High-level prediction interface for fraud detection.

This module is the single entry point for fraud inference.  It orchestrates:

    TransactionPayload
        → validate_transaction()        (schemas.py Pydantic validation)
        → prepare_features()            (here — matches training notebook exactly)
        → run_fraud_inference()         (model.py)
        → decode labels + verdict       (here)
        → build FraudPredictionResult   (schemas.py)

**No model loading logic is duplicated here.**

Feature engineering notes (from datasets/transactions/Paysim.ipynb)
---------------------------------------------------------------------
The 18 features fed to the XGBoost model (in exact column order):

  1.  step                  — simulation step (passed through)
  2.  type                  — LabelEncoded: CASH_IN=0, CASH_OUT=1, DEBIT=2,
                              PAYMENT=3, TRANSFER=4
  3.  amount                — transaction amount (passed through)
  4.  oldbalanceOrg         — origin balance before (passed through)
  5.  newbalanceOrig        — origin balance after (passed through)
  6.  oldbalanceDest        — destination balance before (passed through)
  7.  newbalanceDest        — destination balance after (passed through)
  8.  isFlaggedFraud        — legacy system flag (passed through)
  9.  log_amount            — log(amount + 1)  [math.log1p]
  10. orig_balance_diff     — oldbalanceOrg - newbalanceOrig
  11. large_transaction     — 1 if amount > 95th-pctile threshold, else 0
  12. receiver_balance_unchanged — 1 if oldbalanceDest == newbalanceDest, else 0
  13. high_risk_type        — ALWAYS 0 (training artefact: encoding was applied
                              before the isin check, so the string comparison
                              always returned False; we must replicate this
                              faithfully to remain consistent with what the
                              model was trained on)
  14. amount_balance_ratio  — amount / (oldbalanceOrg + 1)
  15. zero_balance          — 1 if newbalanceOrig == 0, else 0
  16. dest_balance_diff     — newbalanceDest - oldbalanceDest
  17. origin_balance_error  — oldbalanceOrg - amount - newbalanceOrig
  18. destination_balance_error — oldbalanceDest + amount - newbalanceDest
"""

from __future__ import annotations

import math
import time
from pathlib import Path
from typing import Any, Optional

import numpy as np

from .config import settings
from .logging import get_logger
from .model import run_fraud_inference
from .schemas import FraudPredictionResult, TransactionPayload

log = get_logger()

# ---------------------------------------------------------------------------
# Type → LabelEncoder integer mapping (sklearn alphabetical order)
# Matches: LabelEncoder().fit_transform on all PaySim types
# ---------------------------------------------------------------------------

_TYPE_ENCODING: dict[str, int] = {
    "CASH_IN": 0,
    "CASH_OUT": 1,
    "DEBIT": 2,
    "PAYMENT": 3,
    "TRANSFER": 4,
}

# ---------------------------------------------------------------------------
# Feature column order — must match model.feature_names_in_ exactly
# ---------------------------------------------------------------------------

_FEATURE_NAMES: list[str] = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "isFlaggedFraud",
    "log_amount",
    "orig_balance_diff",
    "large_transaction",
    "receiver_balance_unchanged",
    "high_risk_type",
    "amount_balance_ratio",
    "zero_balance",
    "dest_balance_diff",
    "origin_balance_error",
    "destination_balance_error",
]

# Label mapping: class index → human-readable string
# XGBoost classes_: [0 = safe, 1 = fraud]
_LABEL_MAP: dict[int, str] = {0: "safe", 1: "fraud"}


# ---------------------------------------------------------------------------
# Feature engineering (must match Paysim.ipynb exactly)
# ---------------------------------------------------------------------------


def prepare_features(
    payload: TransactionPayload,
    large_transaction_threshold: Optional[float] = None,
) -> tuple[dict[str, Any], np.ndarray]:
    """Build the 18-feature vector used during PaySim model training.

    Replicates every transformation applied in the training notebook
    (``datasets/transactions/Paysim.ipynb``) in the exact same order.

    Parameters
    ----------
    payload:
        Validated transaction fields from ``TransactionPayload``.
    large_transaction_threshold:
        Override the threshold from settings (used in tests).

    Returns
    -------
    features:
        Dict mapping feature name → value (for evidence logging / transparency).
    feature_vector:
        2-D ``np.ndarray`` of shape ``(1, 18)`` ready for the model.
    """
    threshold = large_transaction_threshold or settings.large_transaction_threshold

    # ------------------------------------------------------------------
    # Raw fields
    # ------------------------------------------------------------------
    step = payload.step
    type_str = payload.type  # already upper-cased by Pydantic validator
    amount = payload.amount
    old_balance_org = payload.oldbalanceOrg
    new_balance_orig = payload.newbalanceOrig
    old_balance_dest = payload.oldbalanceDest
    new_balance_dest = payload.newbalanceDest
    is_flagged = payload.isFlaggedFraud

    # ------------------------------------------------------------------
    # Feature engineering (notebook order)
    # ------------------------------------------------------------------
    type_encoded = _TYPE_ENCODING[type_str]  # LabelEncoder equivalent

    log_amount = math.log1p(amount)  # log(amount + 1) — verified: log(182)=5.204007

    orig_balance_diff = old_balance_org - new_balance_orig

    large_transaction = int(amount > threshold)

    receiver_balance_unchanged = int(old_balance_dest == new_balance_dest)

    # high_risk_type is ALWAYS 0 in training because the notebook applied
    # LabelEncoder BEFORE computing this feature, so isin(['TRANSFER','CASH_OUT'])
    # on integer-typed column always returned False.  We reproduce this faithfully.
    high_risk_type = 0

    amount_balance_ratio = amount / (old_balance_org + 1)

    zero_balance = int(new_balance_orig == 0)

    dest_balance_diff = new_balance_dest - old_balance_dest

    origin_balance_error = old_balance_org - amount - new_balance_orig

    destination_balance_error = old_balance_dest + amount - new_balance_dest

    # ------------------------------------------------------------------
    # Assemble dict (used for evidence) and vector (used for inference)
    # ------------------------------------------------------------------
    features: dict[str, Any] = {
        "step": step,
        "type": type_encoded,
        "amount": amount,
        "oldbalanceOrg": old_balance_org,
        "newbalanceOrig": new_balance_orig,
        "oldbalanceDest": old_balance_dest,
        "newbalanceDest": new_balance_dest,
        "isFlaggedFraud": is_flagged,
        "log_amount": log_amount,
        "orig_balance_diff": orig_balance_diff,
        "large_transaction": large_transaction,
        "receiver_balance_unchanged": receiver_balance_unchanged,
        "high_risk_type": high_risk_type,
        "amount_balance_ratio": amount_balance_ratio,
        "zero_balance": zero_balance,
        "dest_balance_diff": dest_balance_diff,
        "origin_balance_error": origin_balance_error,
        "destination_balance_error": destination_balance_error,
    }

    # Build 2-D float64 array in the exact column order the model expects
    feature_vector = np.array(
        [[features[name] for name in _FEATURE_NAMES]],
        dtype=np.float64,
    )

    return features, feature_vector


# ---------------------------------------------------------------------------
# Public prediction API
# ---------------------------------------------------------------------------


def predict_fraud(
    payload: TransactionPayload,
    *,
    case_id: str = "unknown",
    model_path: Optional[Path] = None,
    large_transaction_threshold: Optional[float] = None,
) -> FraudPredictionResult:
    """Run end-to-end fraud inference and return a structured result.

    Parameters
    ----------
    payload:
        Validated transaction payload.
    case_id:
        Case identifier used in log records.
    model_path:
        Override the model path from settings (used in integration tests).
    large_transaction_threshold:
        Override the large-transaction threshold (used in tests).

    Returns
    -------
    :class:`FraudPredictionResult`

    Raises
    ------
    FileNotFoundError
        If model artefacts are missing.
    RuntimeError
        If inference fails.
    """
    t_start = time.perf_counter()
    log.info(
        "[case_id=%s] Fraud prediction request — type=%s, amount=%.2f.",
        case_id,
        payload.type,
        payload.amount,
    )

    # ------------------------------------------------------------------
    # 1. Feature engineering
    # ------------------------------------------------------------------
    features, feature_vector = prepare_features(payload, large_transaction_threshold)

    # ------------------------------------------------------------------
    # 2. Model inference → probabilities
    # ------------------------------------------------------------------
    # probabilities shape: (1, 2) — [P(safe), P(fraud)]
    probabilities = run_fraud_inference(feature_vector, model_path)

    safe_prob = float(probabilities[0][0])
    fraud_prob = float(probabilities[0][1])

    # ------------------------------------------------------------------
    # 3. Determine predicted class and confidence
    # ------------------------------------------------------------------
    predicted_idx = int(probabilities[0].argmax())
    predicted_class = _LABEL_MAP[predicted_idx]
    confidence = round(float(probabilities[0][predicted_idx]), 6)

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] Fraud prediction complete — class='%s', confidence=%.4f, elapsed=%.1f ms.",
        case_id,
        predicted_class,
        confidence,
        elapsed_ms,
    )

    return FraudPredictionResult(
        predicted_class=predicted_class,
        confidence=confidence,
        fraud_probability=round(fraud_prob, 6),
        safe_probability=round(safe_prob, 6),
        type_encoded=features["type"],
        engineered_features={k: v for k, v in features.items() if k != "type"},
    )


# ---------------------------------------------------------------------------
# Verdict helper
# ---------------------------------------------------------------------------


def build_fraud_verdict(
    result: FraudPredictionResult,
    transaction_type: str,
    case_id: str = "unknown",
) -> dict:
    """Translate a ``FraudPredictionResult`` into Agent Contract response fields.

    Keeps verdict-mapping logic in one place so any caller (FastAPI route,
    test, CLI) stays thin.

    Parameters
    ----------
    result:
        The structured prediction result.
    transaction_type:
        The original (string) transaction type, e.g. ``"TRANSFER"``.
    case_id:
        Case identifier used in log records.

    Returns
    -------
    A **dict** (not a Pydantic model) so callers can embed it directly into
    ``FraudAnalysisResponse``.
    """
    confidence = result.confidence
    predicted_class = result.predicted_class.lower()

    if confidence < settings.confidence_threshold:
        verdict = "suspicious"
        category = "none"
        risk_score = 50
        explanation = (
            f"Model confidence ({confidence:.1%}) is below the threshold "
            f"({settings.confidence_threshold:.1%}). Manual review recommended."
        )
    elif predicted_class == "fraud":
        verdict = "fraud"
        category = "mule_transaction"
        risk_score = _confidence_to_risk(confidence)
        explanation = (
            f"{transaction_type} transaction flagged as fraudulent "
            f"with {confidence:.1%} confidence "
            f"(fraud probability: {result.fraud_probability:.4f})."
        )
    else:
        verdict = "safe"
        category = "none"
        risk_score = 100 - _confidence_to_risk(confidence)
        explanation = (
            f"{transaction_type} transaction classified as legitimate "
            f"with {confidence:.1%} confidence."
        )

    log.info(
        "[case_id=%s] Fraud verdict='%s', risk_score=%d, category='%s'.",
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
