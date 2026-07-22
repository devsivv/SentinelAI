"""
preprocess.py — Image preprocessing for the Currency Agent.

Responsibilities
----------------
- Accept raw bytes **or** a file path as input.
- Load the image (handles JPEG, PNG, WebP, BMP, TIFF).
- Resize to the configured ``image_size``.
- Apply ImageNet normalisation (mean/std matching training).
- Return a 4-D float32 tensor ``(1, 3, H, W)`` ready for the model.

This module is intentionally free of inference logic.  The only
dependency on the rest of the agent is the ``settings`` singleton.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Union

import numpy as np
from PIL import Image, UnidentifiedImageError

from .config import settings
from .logging import get_logger

log = get_logger()

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------

ImageInput = Union[bytes, Path, str]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_image(source: ImageInput) -> Image.Image:
    """Load a PIL Image from raw bytes or a file-system path.

    Parameters
    ----------
    source:
        Raw image bytes, a ``pathlib.Path``, or a string path.

    Returns
    -------
    PIL.Image.Image
        The loaded image in RGB mode.

    Raises
    ------
    ValueError
        If ``source`` is empty bytes or the image cannot be decoded.
    FileNotFoundError
        If a path is given that does not exist.
    """
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")
        log.debug("Loading image from path: %s", path)
        try:
            img = Image.open(path).convert("RGB")
        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError(f"Cannot decode image at '{path}': {exc}") from exc
    elif isinstance(source, (bytes, bytearray)):
        if not source:
            raise ValueError("Image bytes are empty.")
        log.debug("Loading image from bytes (%d bytes).", len(source))
        try:
            img = Image.open(io.BytesIO(source)).convert("RGB")
        except (UnidentifiedImageError, OSError) as exc:
            raise ValueError(f"Cannot decode image from bytes: {exc}") from exc
    else:
        raise TypeError(f"Unsupported image source type: {type(source).__name__}")

    return img


def preprocess(source: ImageInput) -> tuple[torch.Tensor, tuple[int, int]]:
    """Full preprocessing pipeline: load → resize → normalise → tensorise.

    Parameters
    ----------
    source:
        Raw image bytes, a ``pathlib.Path``, or a string path.

    Returns
    -------
    tensor:
        Float32 tensor of shape ``(1, 3, H, W)`` ready for the model.
    image_size:
        ``(width, height)`` of the image **after** resizing (for audit logging).

    Raises
    ------
    ValueError
        If the image cannot be decoded or has unsupported dimensions.
    """
    img = load_image(source)

    target_h, target_w = settings.image_size
    img = img.resize((target_w, target_h), Image.BILINEAR)
    image_size: tuple[int, int] = img.size  # (width, height)

    # Convert to float32 array in [0, 1]
    arr = np.asarray(img, dtype=np.float32) / 255.0  # shape: (H, W, 3)

    # ImageNet normalisation: (x - mean) / std  per channel
    mean = np.array(settings.normalize_mean, dtype=np.float32)  # (3,)
    std = np.array(settings.normalize_std, dtype=np.float32)  # (3,)
    arr = (arr - mean) / std  # broadcast over (H, W, 3)

    # HWC → CHW → add batch dimension: (H, W, 3) → (3, H, W) → (1, 3, H, W)
    import torch

    tensor = torch.from_numpy(arr.transpose(2, 0, 1)).unsqueeze(0)

    log.debug(
        "Preprocessed image to tensor %s, size=%s.",
        tuple(tensor.shape),
        image_size,
    )
    return tensor, image_size
