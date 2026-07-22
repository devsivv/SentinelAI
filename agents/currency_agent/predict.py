"""
predict.py — High-level prediction interface for the Currency Agent.

This module is the single entry point for callers (a FastAPI route or a
script).  It orchestrates the full pipeline:

    raw image bytes / path
        → preprocess()             (preprocess.py)
        → run_inference()          (model.py)
        → softmax + decode labels  (here)
        → build PredictionResult   (schemas.py)

**No preprocessing or model-loading logic is duplicated here.**
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from .config import settings
from .logging import get_logger
from .model import load_class_names, run_inference
from .preprocess import ImageInput, preprocess
from .schemas import PredictionResult

log = get_logger()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def predict(
    source: ImageInput,
    *,
    case_id: str = "unknown",
    model_path: Optional[Path] = None,
    class_names_path: Optional[Path] = None,
) -> PredictionResult:
    """Run end-to-end inference on an image and return a structured result.

    Parameters
    ----------
    source:
        Raw image bytes, a ``pathlib.Path``, or a string path to an image file.
    case_id:
        Case identifier used in log records so every prediction can be
        correlated across logs and reports.
    model_path:
        Override the model path from settings (used in integration tests).
    class_names_path:
        Override the class-names path from settings (used in integration tests).

    Returns
    -------
    :class:`PredictionResult`
        Contains ``predicted_class``, ``confidence``, ``probabilities``, and
        ``image_size``.

    Raises
    ------
    ValueError
        If the image bytes are empty or cannot be decoded.
    FileNotFoundError
        If a path is given that does not exist, or if model artefacts are missing.
    RuntimeError
        If the model forward pass fails.
    """
    t_start = time.perf_counter()
    log.info("[case_id=%s] Prediction request received.", case_id)

    # ------------------------------------------------------------------
    # 1. Preprocessing
    # ------------------------------------------------------------------
    try:
        tensor, image_size = preprocess(source)
    except (ValueError, FileNotFoundError, TypeError) as exc:
        log.warning("[case_id=%s] Preprocessing failed: %s", case_id, exc)
        raise

    # ------------------------------------------------------------------
    # 2. Raw inference (logits)
    # ------------------------------------------------------------------
    logits = run_inference(tensor, model_path)  # shape: (1, num_classes)

    # ------------------------------------------------------------------
    # 3. Softmax → probabilities
    # ------------------------------------------------------------------
    import torch
    import torch.nn.functional as F

    probs: Any = F.softmax(logits, dim=1).squeeze(0)  # (num_classes,)

    # ------------------------------------------------------------------
    # 4. Decode class labels
    # ------------------------------------------------------------------
    class_map = load_class_names(class_names_path)
    # class_map keys are string integers; sort by key to align with tensor order.
    sorted_indices = sorted(class_map.keys(), key=int)
    labels: list[str] = [class_map[idx] for idx in sorted_indices]

    prob_values: list[float] = probs.tolist()

    if len(labels) != len(prob_values):
        raise RuntimeError(
            f"Class-name count ({len(labels)}) does not match model output "
            f"({len(prob_values)}).  Ensure class_names.json matches the "
            f"trained model."
        )

    probabilities: dict[str, float] = {
        label: round(float(p), 6) for label, p in zip(labels, prob_values)
    }

    # ------------------------------------------------------------------
    # 5. Determine predicted class and confidence
    # ------------------------------------------------------------------
    best_idx = int(probs.argmax().item())
    predicted_class = labels[best_idx]
    confidence = round(float(probs[best_idx].item()), 6)

    elapsed_ms = (time.perf_counter() - t_start) * 1000
    log.info(
        "[case_id=%s] Prediction complete — class='%s', confidence=%.4f, "
        "elapsed=%.1f ms.",
        case_id,
        predicted_class,
        confidence,
        elapsed_ms,
    )

    return PredictionResult(
        predicted_class=predicted_class,
        confidence=confidence,
        probabilities=probabilities,
        image_size=image_size,
    )


# ---------------------------------------------------------------------------
# Verdict helpers
# ---------------------------------------------------------------------------


def build_verdict(result: PredictionResult, case_id: str = "unknown") -> dict:
    """Translate a ``PredictionResult`` into Agent Contract response fields.

    This keeps verdict-mapping logic in one place so the FastAPI route and
    any other callers stay thin.

    Returns a **dict** (not a Pydantic model) so callers can embed it directly
    into ``CurrencyAnalysisResponse``.
    """
    confidence = result.confidence
    predicted_class = result.predicted_class.lower()

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    if confidence < settings.confidence_threshold:
        verdict = "suspicious"
        category = "none"
        risk_score = 50
        explanation = (
            f"Model confidence ({confidence:.1%}) is below the threshold "
            f"({settings.confidence_threshold:.1%}).  Manual review recommended."
        )
    elif predicted_class == "fake":
        verdict = "fraud"
        category = "counterfeit_note"
        risk_score = _confidence_to_risk(confidence)
        explanation = (
            f"MobileNetV2 classified the note as counterfeit with "
            f"{confidence:.1%} confidence."
        )
    else:
        verdict = "safe"
        category = "none"
        risk_score = 100 - _confidence_to_risk(confidence)
        explanation = (
            f"MobileNetV2 classified the note as genuine with "
            f"{confidence:.1%} confidence."
        )

    log.info(
        "[case_id=%s] Verdict='%s', risk_score=%d, category='%s'.",
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
    """Map model confidence in [0, 1] to an integer risk score in [0, 100].

    A ``fake`` class confidence of 1.0 maps to risk 100; 0.5 maps to risk 50.
    """
    return int(round(confidence * 100))
