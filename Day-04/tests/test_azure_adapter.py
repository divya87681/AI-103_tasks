
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

import pytest

from azure_adapter import AzureOCRError, analyze_image


def test_live_calls_disabled_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "AZURE_VISION_ENDPOINT",
        "https://example.cognitiveservices.azure.com",
    )
    monkeypatch.delenv("LIVE_AZURE_CALLS_APPROVED", raising=False)

    image = tmp_path / "sample.jpg"
    image.write_bytes(b"synthetic-image")

    with pytest.raises(AzureOCRError, match="disabled"):
        analyze_image(str(image))


def test_missing_endpoint_is_rejected(monkeypatch):
    monkeypatch.delenv("AZURE_VISION_ENDPOINT", raising=False)
    monkeypatch.setenv("LIVE_AZURE_CALLS_APPROVED", "false")

    with pytest.raises(AzureOCRError, match="AZURE_VISION_ENDPOINT"):
        analyze_image("sample.jpg")


def test_missing_image_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "AZURE_VISION_ENDPOINT",
        "https://example.cognitiveservices.azure.com",
    )
    monkeypatch.setenv("LIVE_AZURE_CALLS_APPROVED", "true")

    missing_image = tmp_path / "missing.jpg"

    with pytest.raises(AzureOCRError, match="Image file not found"):
        analyze_image(str(missing_image))
