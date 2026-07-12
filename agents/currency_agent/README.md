# Currency Agent

MobileNetV2-based counterfeit Indian currency detector.

---

## Overview

The Currency Agent provides a production inference layer around the MobileNetV2 model trained in Sprint 01.  It accepts a raw currency-note image and returns a structured verdict — `safe`, `suspicious`, or `fraud` — together with a confidence score, risk score, and per-class probabilities.

The agent follows the standard **Agent Contract** defined in `docs/api.md` so it can be wired into the Orchestrator without any changes to the rest of the system.

---

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | All runtime settings (paths, thresholds, image size, log level). No hardcoded values. |
| `logging.py` | Shared rotating-file + stdout logger (`logs/agents/currency_agent.log`). |
| `preprocess.py` | Load image → resize to 224 × 224 → ImageNet normalise → (1, 3, H, W) tensor. |
| `model.py` | Singleton model loader (lazy, thread-safe). Raw logits only. |
| `predict.py` | Full pipeline: preprocess → infer → softmax → label decode → verdict. |
| `schemas.py` | Pydantic request / response models (Agent Contract compliant). |

---

## Required Model Files

Place these under `models/currency/` **before running the agent**:

| File | Description |
|---|---|
| `mobilenet_v2.pt` | Exported MobileNetV2 (TorchScript or state-dict, produced in Sprint 01). |
| `class_names.json` | Class-index-to-label mapping, e.g. `{"0": "fake", "1": "real"}`. |

> **Note:** Model files are git-ignored.  Download them via `scripts/download_models.py` or copy them from the Sprint 01 training output.

The agent tries `mobilenet_v2.pt` by default.  Override via the `CURRENCY_MODEL_PATH` environment variable or by editing `configs/models.yaml`.

---

## Configuration

All settings are read from environment variables prefixed `CURRENCY_`.  The defaults work out-of-the-box for a standard clone:

| Variable | Default | Description |
|---|---|---|
| `CURRENCY_MODEL_PATH` | `models/currency/mobilenet_v2.pt` | Path to the model file. |
| `CURRENCY_CLASS_NAMES_PATH` | `models/currency/class_names.json` | Path to the class-name mapping. |
| `CURRENCY_IMAGE_SIZE` | `(224, 224)` | Resize target (height, width). |
| `CURRENCY_CONFIDENCE_THRESHOLD` | `0.70` | Below this → `suspicious` verdict. |
| `CURRENCY_LOG_LEVEL` | `INFO` | Python logging level. |
| `CURRENCY_LOG_DIR` | `logs/agents` | Directory for rotating log files. |

---

## Usage (Python)

```python
from agents.currency_agent import predict, build_verdict

# From file path
result = predict("path/to/note.jpg", case_id="c-2026-0001")

# From raw bytes (e.g. FastAPI UploadFile)
with open("note.jpg", "rb") as f:
    image_bytes = f.read()
result = predict(image_bytes, case_id="c-2026-0001")

print(result.predicted_class)   # "fake" or "real"
print(result.confidence)        # 0.9847

verdict_fields = build_verdict(result, case_id="c-2026-0001")
print(verdict_fields["verdict"])     # "fraud" | "safe" | "suspicious"
print(verdict_fields["risk_score"])  # 0–100
```

---

## Dependencies

The agent requires the following packages (already listed in `requirements/ml.txt` and `requirements/base.txt`):

```
torch
torchvision
Pillow
numpy
pydantic
pydantic-settings
```

Install everything:

```bash
pip install -r requirements/base.txt -r requirements/ml.txt
```

---

## Testing

```bash
pytest tests/test_currency.py -v
```

Tests cover: model loading, preprocessing, successful prediction, invalid image handling, confidence range, and missing model file.

---

## Verdict Logic

| Condition | Verdict | Category |
|---|---|---|
| confidence ≥ threshold **and** class = `fake` | `fraud` | `counterfeit_note` |
| confidence ≥ threshold **and** class = `real` | `safe` | `none` |
| confidence < threshold (any class) | `suspicious` | `none` |

Default threshold: **0.70** (configurable via `CURRENCY_CONFIDENCE_THRESHOLD`).

---

## Sprint

Phase 2 — Currency Agent (Stretch) — Sprint 02.
