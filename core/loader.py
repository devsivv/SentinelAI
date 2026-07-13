"""
core/loader.py — Generic thread-safe lazy joblib/pickle model loader.

The three joblib-based agents (scam_comm SMS, scam_comm URL, fraud) contained
structurally identical double-checked-locking singleton code.  This module
consolidates that pattern into a single reusable function.

The currency agent's PyTorch loader has unique TorchScript/state-dict logic
and is intentionally NOT covered here.

Usage
-----
Each agent model module keeps its own module-level ``_cache`` and
``_lock``, then delegates loading to ``load_joblib_model``::

    import threading
    from core.loader import load_joblib_model

    _lock: threading.Lock = threading.Lock()
    _cache: list = [None]   # mutable 1-element list — the cache slot

    def get_my_model(path=None):
        return load_joblib_model(
            path or settings.model_path,
            cache_dict=globals(),
            cache_key="_model",
            lock=_lock,
            label="My Model",
        )

    def reset_my_model_cache():
        with _lock:
            _cache[0] = None
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

import joblib


def load_joblib_model(
    path: Path,
    cache_dict: dict[str, Any],
    cache_key: str,
    lock: threading.Lock,
    *,
    label: str = "model",
) -> Any:
    """Load a serialized model from *path* using double-checked locking.

    The loaded object is stored in ``cache[0]``.  On subsequent calls the
    cached value is returned immediately without acquiring the lock.

    Parameters
    ----------
    path:
        Absolute path to the serialized model file.
    cache_dict:
        A dictionary used for storage (e.g. ``globals()`` of the calling module).
    cache_key:
        The string key in the dictionary where the model is stored (e.g. ``"_model"``).
    lock:
        The ``threading.Lock`` used for the critical section.
    label:
        Human-readable name used in log/error messages, e.g. ``"SMS model"``.


    Returns
    -------
    The deserialized model object.

    Raises
    ------
    FileNotFoundError
        If ``path`` does not exist on disk.
    RuntimeError
        If deserialization fails unexpectedly.
    """
    # Fast path — no lock needed once populated.
    if cache_dict.get(cache_key) is not None:
        return cache_dict[cache_key]

    with lock:
        # Double-checked locking: another thread may have loaded while waiting.
        if cache_dict.get(cache_key) is None:
            if not path.exists():
                raise FileNotFoundError(
                    f"{label} not found at '{path}'. "
                    "Verify the path in configs/models.yaml."
                )
            try:
                cache_dict[cache_key] = joblib.load(str(path))
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to load {label} from '{path}': {exc}"
                ) from exc

    return cache_dict[cache_key]
