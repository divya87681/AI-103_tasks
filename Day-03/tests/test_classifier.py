
import sys
from pathlib import Path

import pytest

# Add Day-03/src to Python's import path
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from classifier import classify_image


def test_laptop_filename_classified(tmp_path):
    image = tmp_path / "laptop_01.jpg"
    image.write_bytes(b"synthetic test data")

    result = classify_image(str(image))

    assert result["label"] == "laptop"
    assert result["adapter"] == "mock"
    assert result["verification_status"] == "NOT_VERIFIED"


def test_keyboard_filename_classified(tmp_path):
    image = tmp_path / "keyboard_01.jpg"
    image.write_bytes(b"synthetic test data")

    result = classify_image(str(image))

    assert result["label"] == "keyboard"


def test_mouse_filename_classified(tmp_path):
    image = tmp_path / "mouse_01.jpg"
    image.write_bytes(b"synthetic test data")

    result = classify_image(str(image))

    assert result["label"] == "mouse"


def test_missing_image_rejected(tmp_path):
    image = tmp_path / "missing_laptop.jpg"

    with pytest.raises(FileNotFoundError):
        classify_image(str(image))


def test_unknown_label_rejected(tmp_path):
    image = tmp_path / "printer_01.jpg"
    image.write_bytes(b"synthetic test data")

    with pytest.raises(ValueError):
        classify_image(str(image))
