"""
tests/test_currency.py — Unit and integration tests for the Currency Agent.

Covers
------
- Model loading (success path and missing-file failure)
- Class-name loading
- Preprocessing (valid image, empty bytes, corrupt bytes)
- End-to-end prediction (mocked inference)
- Confidence range enforcement (0 ≤ confidence ≤ 1)
- Invalid image handling (graceful ValueError)
- Verdict logic (fake → fraud, real → safe, low-confidence → suspicious)

Design notes
------------
- Tests do **not** require the real model file on disk.
- ``torch.nn.Module`` inference is mocked so the test suite runs in CI
  without GPU or large model downloads.
- Fixtures create minimal in-memory artefacts (a tiny PNG and a temp
  class_names.json) so every path through the code is exercised.
"""

from __future__ import annotations

import io
import json
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
import torch
from PIL import Image

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_png_bytes(width: int = 64, height: int = 64, color: tuple = (128, 64, 32)) -> bytes:
    """Return raw bytes of a solid-colour PNG image."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_class_names_json(tmp_path: Path, mapping: dict | None = None) -> Path:
    """Write a class_names.json to a temp directory and return its path."""
    mapping = mapping or {"0": "fake", "1": "real"}
    p = tmp_path / "class_names.json"
    p.write_text(json.dumps(mapping), encoding="utf-8")
    return p


def _make_mock_model(num_classes: int = 2, fake_logits: list[float] | None = None) -> MagicMock:
    """Return a MagicMock that behaves like a torch.nn.Module for inference."""
    if fake_logits is None:
        fake_logits = [5.0, -3.0]  # Strong preference for class 0 ("fake")
    mock = MagicMock(spec=torch.nn.Module)
    mock.return_value = torch.tensor([fake_logits], dtype=torch.float32)
    return mock


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_model_cache():
    """Reset the singleton cache before and after every test."""
    from agents.currency_agent.model import reset_model_cache

    reset_model_cache()
    yield
    reset_model_cache()


@pytest.fixture
def valid_png_bytes() -> bytes:
    return _make_png_bytes()


@pytest.fixture
def class_names_file(tmp_path: Path) -> Path:
    return _make_class_names_json(tmp_path)


@pytest.fixture
def fake_model() -> MagicMock:
    """Model that returns logits strongly favouring class 0 ('fake')."""
    return _make_mock_model(fake_logits=[8.0, -5.0])


@pytest.fixture
def real_model() -> MagicMock:
    """Model that returns logits strongly favouring class 1 ('real')."""
    return _make_mock_model(fake_logits=[-5.0, 8.0])


@pytest.fixture
def low_confidence_model() -> MagicMock:
    """Model that returns nearly equal logits → confidence ≈ 0.5."""
    return _make_mock_model(fake_logits=[0.01, -0.01])


# ---------------------------------------------------------------------------
# 1. Class-name loading
# ---------------------------------------------------------------------------


class TestLoadClassNames:
    def test_loads_valid_json(self, tmp_path: Path):
        from agents.currency_agent.model import load_class_names

        path = _make_class_names_json(tmp_path)
        names = load_class_names(path)
        assert names == {"0": "fake", "1": "real"}

    def test_caches_on_second_call(self, tmp_path: Path):
        from agents.currency_agent.model import load_class_names

        path = _make_class_names_json(tmp_path)
        first = load_class_names(path)
        second = load_class_names(path)
        assert first is second  # same object → cached

    def test_raises_file_not_found(self, tmp_path: Path):
        from agents.currency_agent.model import load_class_names

        missing = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError, match="class_names.json not found"):
            load_class_names(missing)

    def test_raises_on_invalid_json(self, tmp_path: Path):
        from agents.currency_agent.model import load_class_names

        bad = tmp_path / "class_names.json"
        bad.write_text("{this is not json", encoding="utf-8")
        with pytest.raises(ValueError, match="Failed to parse"):
            load_class_names(bad)


# ---------------------------------------------------------------------------
# 2. Model loading
# ---------------------------------------------------------------------------


class TestModelLoading:
    def test_raises_file_not_found_for_missing_model(self, tmp_path: Path):
        from agents.currency_agent.model import get_model

        missing = tmp_path / "no_model.pt"
        with pytest.raises(FileNotFoundError, match="Model file not found"):
            get_model(missing)

    def test_singleton_returns_same_object(self, tmp_path: Path, fake_model: MagicMock):
        from agents.currency_agent import model as model_module

        # Patch _load_model so no real file is needed.
        with patch.object(model_module, "_load_model", return_value=fake_model):
            m1 = model_module.get_model()
            m2 = model_module.get_model()
        assert m1 is m2

    def test_thread_safe_singleton(self, fake_model: MagicMock):
        """Concurrent get_model() calls must all receive the same instance."""
        from agents.currency_agent import model as model_module

        results: list[object] = []
        errors: list[Exception] = []

        def worker():
            try:
                with patch.object(model_module, "_load_model", return_value=fake_model):
                    results.append(model_module.get_model())
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Thread errors: {errors}"
        assert len(results) == 10
        # All threads should return the same singleton.
        assert all(r is results[0] for r in results)


# ---------------------------------------------------------------------------
# 3. Preprocessing
# ---------------------------------------------------------------------------


class TestPreprocess:
    def test_valid_bytes_returns_correct_tensor_shape(self, valid_png_bytes: bytes):
        from agents.currency_agent.preprocess import preprocess

        tensor, image_size = preprocess(valid_png_bytes)
        assert tensor.shape == (1, 3, 224, 224)
        assert tensor.dtype == torch.float32

    def test_valid_bytes_returns_correct_image_size(self, valid_png_bytes: bytes):
        from agents.currency_agent.preprocess import preprocess

        _, image_size = preprocess(valid_png_bytes)
        assert image_size == (224, 224)

    def test_valid_file_path(self, tmp_path: Path, valid_png_bytes: bytes):
        from agents.currency_agent.preprocess import preprocess

        img_file = tmp_path / "test.png"
        img_file.write_bytes(valid_png_bytes)
        tensor, _ = preprocess(img_file)
        assert tensor.shape == (1, 3, 224, 224)

    def test_empty_bytes_raises_value_error(self):
        from agents.currency_agent.preprocess import preprocess

        with pytest.raises(ValueError, match="Image bytes are empty"):
            preprocess(b"")

    def test_corrupt_bytes_raises_value_error(self):
        from agents.currency_agent.preprocess import preprocess

        with pytest.raises(ValueError, match="Cannot decode image"):
            preprocess(b"\x00\x01\x02\x03")

    def test_missing_file_raises_file_not_found(self, tmp_path: Path):
        from agents.currency_agent.preprocess import preprocess

        with pytest.raises(FileNotFoundError):
            preprocess(tmp_path / "ghost.jpg")

    def test_tensor_values_are_normalised(self, valid_png_bytes: bytes):
        """After ImageNet normalisation the tensor should have values outside [0, 1]."""
        from agents.currency_agent.preprocess import preprocess

        tensor, _ = preprocess(valid_png_bytes)
        # At least some values should be outside raw [0, 1] range after normalisation.
        arr = tensor.numpy()
        # A solid (128, 64, 32) image normalised should have values in roughly [-3, 3].
        assert arr.min() < 0 or arr.max() > 1, (
            "Tensor appears un-normalised; expected values outside [0, 1]."
        )

    def test_load_image_invalid_type_raises_type_error(self):
        from agents.currency_agent.preprocess import load_image

        with pytest.raises(TypeError, match="Unsupported image source type"):
            load_image(12345)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 4. End-to-end prediction (mocked inference)
# ---------------------------------------------------------------------------


class TestPredict:
    def _run_predict(self, mock_model, class_names_file, png_bytes):
        """Helper: patch model singleton + class names, then call predict()."""
        from agents.currency_agent import model as model_module
        from agents.currency_agent.predict import predict

        with (
            patch.object(model_module, "get_model", return_value=mock_model),
            patch("agents.currency_agent.model._class_names", None),
        ):
            return predict(
                png_bytes,
                case_id="test-001",
                class_names_path=class_names_file,
            )

    def test_successful_prediction_returns_result(
        self, fake_model, class_names_file, valid_png_bytes
    ):
        result = self._run_predict(fake_model, class_names_file, valid_png_bytes)
        assert result.predicted_class in ("fake", "real")
        assert 0.0 <= result.confidence <= 1.0

    def test_confidence_range(self, fake_model, class_names_file, valid_png_bytes):
        result = self._run_predict(fake_model, class_names_file, valid_png_bytes)
        assert 0.0 <= result.confidence <= 1.0

    def test_probabilities_sum_to_one(self, fake_model, class_names_file, valid_png_bytes):
        result = self._run_predict(fake_model, class_names_file, valid_png_bytes)
        total = sum(result.probabilities.values())
        assert abs(total - 1.0) < 1e-5, f"Probabilities sum to {total}, expected ~1.0"

    def test_probabilities_keys_match_class_names(
        self, fake_model, class_names_file, valid_png_bytes
    ):
        result = self._run_predict(fake_model, class_names_file, valid_png_bytes)
        assert set(result.probabilities.keys()) == {"fake", "real"}

    def test_fake_class_prediction(self, fake_model, class_names_file, valid_png_bytes):
        result = self._run_predict(fake_model, class_names_file, valid_png_bytes)
        assert result.predicted_class == "fake"
        assert result.confidence > 0.9  # logits [8, -5] → strong fake signal

    def test_real_class_prediction(self, real_model, class_names_file, valid_png_bytes):
        result = self._run_predict(real_model, class_names_file, valid_png_bytes)
        assert result.predicted_class == "real"
        assert result.confidence > 0.9

    def test_invalid_image_raises_value_error(
        self, fake_model, class_names_file
    ):
        from agents.currency_agent import model as model_module
        from agents.currency_agent.predict import predict

        with (
            patch.object(model_module, "get_model", return_value=fake_model),
        ):
            with pytest.raises(ValueError):
                predict(b"not-an-image", case_id="test-err", class_names_path=class_names_file)

    def test_empty_bytes_raises_value_error(self, fake_model, class_names_file):
        from agents.currency_agent import model as model_module
        from agents.currency_agent.predict import predict

        with patch.object(model_module, "get_model", return_value=fake_model):
            with pytest.raises(ValueError, match="Image bytes are empty"):
                predict(b"", case_id="test-empty", class_names_path=class_names_file)


# ---------------------------------------------------------------------------
# 5. Verdict logic
# ---------------------------------------------------------------------------


class TestBuildVerdict:
    """Verify that build_verdict() maps predictions to correct Agent Contract fields."""

    def _make_result(self, predicted_class: str, confidence: float):
        from agents.currency_agent.schemas import PredictionResult

        return PredictionResult(
            predicted_class=predicted_class,
            confidence=confidence,
            probabilities={predicted_class: confidence, "other": round(1 - confidence, 6)},
            image_size=(224, 224),
        )

    def test_fake_high_confidence_gives_fraud_verdict(self):
        from agents.currency_agent.predict import build_verdict

        result = self._make_result("fake", 0.95)
        verdict = build_verdict(result)
        assert verdict["verdict"] == "fraud"
        assert verdict["category"] == "counterfeit_note"
        assert 0 <= verdict["risk_score"] <= 100

    def test_real_high_confidence_gives_safe_verdict(self):
        from agents.currency_agent.predict import build_verdict

        result = self._make_result("real", 0.92)
        verdict = build_verdict(result)
        assert verdict["verdict"] == "safe"
        assert verdict["category"] == "none"

    def test_low_confidence_gives_suspicious_verdict(self):
        from agents.currency_agent.predict import build_verdict

        # Confidence below default threshold (0.70)
        result = self._make_result("fake", 0.55)
        verdict = build_verdict(result)
        assert verdict["verdict"] == "suspicious"

    def test_risk_score_in_valid_range(self):
        from agents.currency_agent.predict import build_verdict

        for confidence in [0.51, 0.70, 0.85, 0.99]:
            result = self._make_result("fake", confidence)
            verdict = build_verdict(result)
            assert 0 <= verdict["risk_score"] <= 100, (
                f"risk_score out of range for confidence={confidence}"
            )

    def test_explanation_is_non_empty_string(self):
        from agents.currency_agent.predict import build_verdict

        result = self._make_result("fake", 0.90)
        verdict = build_verdict(result)
        assert isinstance(verdict["explanation"], str)
        assert len(verdict["explanation"]) > 0


# ---------------------------------------------------------------------------
# 6. Missing model file
# ---------------------------------------------------------------------------


class TestMissingModelFile:
    def test_get_model_raises_file_not_found(self, tmp_path: Path):
        from agents.currency_agent.model import get_model

        missing_path = tmp_path / "nonexistent_model.pt"
        with pytest.raises(FileNotFoundError):
            get_model(missing_path)

    def test_predict_propagates_file_not_found(self, tmp_path: Path, valid_png_bytes: bytes):
        """predict() must surface FileNotFoundError when the model is absent."""
        from agents.currency_agent.predict import predict

        missing = tmp_path / "no_model.pt"
        with pytest.raises(FileNotFoundError):
            predict(valid_png_bytes, case_id="test-missing", model_path=missing)
