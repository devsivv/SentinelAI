"""
model.py — Singleton model loader and raw inference for the Currency Agent.

Responsibilities
----------------
- Load ``class_names.json`` once and cache it.
- Load the exported MobileNetV2 model once (lazy, thread-safe via a lock).
- Expose a single ``run_inference`` function that accepts a preprocessed
  tensor and returns raw logits.

This module contains **no preprocessing logic** (that lives in preprocess.py)
and **no business-level scoring** (that lives in predict.py).
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn

from .config import settings
from .logging import get_logger

log = get_logger()

# ---------------------------------------------------------------------------
# Thread-safe lazy singleton state
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_model: Optional[nn.Module] = None
_class_names: Optional[dict[str, str]] = None  # {"0": "fake", "1": "real", ...}


# ---------------------------------------------------------------------------
# Class-name loading
# ---------------------------------------------------------------------------


def load_class_names(path: Optional[Path] = None) -> dict[str, str]:
    """Load and return the class-name mapping from ``class_names.json``.

    The result is cached after the first successful load.

    Parameters
    ----------
    path:
        Override the default path from settings (used in tests).

    Returns
    -------
    dict mapping index strings to label strings, e.g. ``{"0": "fake", "1": "real"}``.

    Raises
    ------
    FileNotFoundError
        If the JSON file does not exist at the resolved path.
    ValueError
        If the file cannot be parsed as JSON.
    """
    global _class_names  # noqa: PLW0603

    if _class_names is not None:
        return _class_names

    resolved = path or settings.class_names_path
    if not resolved.exists():
        raise FileNotFoundError(
            f"class_names.json not found at '{resolved}'. "
            "Ensure the models/currency/ directory contains the trained artefacts."
        )

    try:
        with resolved.open("r", encoding="utf-8") as fh:
            mapping: dict[str, str] = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Failed to parse '{resolved}': {exc}") from exc

    log.info("Loaded %d class names from '%s'.", len(mapping), resolved)
    _class_names = mapping
    return _class_names


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------


def _load_model(path: Optional[Path] = None) -> nn.Module:
    """Internal loader — always returns a new model instance (not cached here).

    The public API is ``get_model()`` which wraps this with a singleton lock.
    """
    resolved = path or settings.model_path
    if not resolved.exists():
        raise FileNotFoundError(
            f"Model file not found at '{resolved}'. "
            "Run scripts/download_models.py or verify the path in configs/models.yaml."
        )

    log.info("Loading MobileNetV2 model from '%s' …", resolved)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Attempt TorchScript load first (exported via torch.jit.save).
    # Fall back to state-dict load (exported via torch.save on the raw module).
    try:
        model = torch.jit.load(str(resolved), map_location=device)
        log.info("Loaded as TorchScript module.")
    except RuntimeError:
        log.debug("TorchScript load failed — attempting state-dict load.")
        model = _load_from_state_dict(resolved)

    model.to(device)
    model.eval()
    return model


def _load_from_state_dict(path: Path) -> nn.Module:
    """Load a MobileNetV2 model from a raw state-dict checkpoint.

    This handles the case where the notebook saved the model with
    ``torch.save(model.state_dict(), ...)``.
    """
    import torchvision.models as tv_models

    num_classes = len(load_class_names())
    backbone = tv_models.mobilenet_v2(weights=None)
    # Replace the classifier head to match training configuration.
    in_features = backbone.classifier[1].in_features
    backbone.classifier[1] = nn.Linear(in_features, num_classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    state = torch.load(str(path), map_location=device, weights_only=True)

    # The checkpoint may be a bare state-dict or wrapped as {"model_state_dict": ...}
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]

    backbone.load_state_dict(state)
    log.info("Loaded as state-dict checkpoint (MobileNetV2, %d classes).", num_classes)
    return backbone


def get_model(path: Optional[Path] = None) -> nn.Module:
    """Return the singleton model, loading it on first call.

    Thread-safe: concurrent callers block until the first load completes.

    Parameters
    ----------
    path:
        Override the default model path from settings (used in tests).

    Returns
    -------
    ``torch.nn.Module`` in eval mode on CPU.
    """
    global _model  # noqa: PLW0603

    if _model is not None:
        return _model

    with _lock:
        # Double-checked locking: another thread may have loaded while we waited.
        if _model is None:
            _model = _load_model(path)

    return _model


def reset_model_cache() -> None:
    """Clear the in-process singleton — used in tests only.

    Calling this in production would force a cold reload on the next request.
    """
    global _model, _class_names  # noqa: PLW0603
    with _lock:
        _model = None
        _class_names = None
    log.debug("Model and class-name cache cleared.")


# ---------------------------------------------------------------------------
# Raw inference
# ---------------------------------------------------------------------------


def run_inference(
    tensor: torch.Tensor,
    model_path: Optional[Path] = None,
) -> torch.Tensor:
    """Run a forward pass and return **raw logits**.

    Parameters
    ----------
    tensor:
        Preprocessed input tensor of shape ``(1, 3, H, W)``, float32, on CPU.
    model_path:
        Override the model path from settings (used in tests to force
        a specific file path, e.g. a non-existent path to test error handling).

    Returns
    -------
    ``torch.Tensor`` of shape ``(1, num_classes)`` — raw (un-normalised) logits.

    Raises
    ------
    FileNotFoundError
        If ``model_path`` does not exist on disk.
    RuntimeError
        If the forward pass fails (shape mismatch, CUDA OOM, etc.).
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tensor = tensor.to(device)
    model = get_model(model_path)

    with torch.no_grad():
        try:
            logits: torch.Tensor = model(tensor)
        except Exception as exc:
            log.exception("Forward pass failed: %s", exc)
            raise RuntimeError(f"Model inference failed: {exc}") from exc

    log.debug("Inference complete — logits shape: %s.", tuple(logits.shape))
    return logits
