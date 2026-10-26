
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

import pytest

from mock_adapter import mock_ocr_response
from ocr_pipeline import (
    parse_ocr_response,
    run_pipeline,
    validate_identifier,
)


# Positive test 1: Extract and validate a correct asset ID.
def test_valid_asset_identifier_matches():
    response = mock_ocr_response("AST-1042")

    result = run_pipeline(response, "AST-1042")

    assert result["status"] == "SUCCESS"
    assert result["asset_id"] == "AST-1042"
    assert result["identifier_valid"] is True
    assert result["matched_expected"] is True


# Positive test 2: Extract text and calculate confidence.
def test_text_and_confidence_are_extracted():
    response = mock_ocr_response("AST-2048", confidence=0.95)

    result = parse_ocr_response(response)

    assert "AST-2048" in result["text"]
    assert result["asset_id"] == "AST-2048"
    assert result["confidence_mean"] == 0.95
    assert result["confidence_word_count"] == 3


# Positive test 3: A valid but different ID does not match.
def test_different_valid_asset_id_does_not_match():
    response = mock_ocr_response("AST-2048")

    result = run_pipeline(response, "AST-1042")

    assert result["identifier_valid"] is True
    assert result["matched_expected"] is False


# Negative test 1: Reject an invalid expected-ID format.
def test_invalid_expected_identifier_raises_error():
    parsed = parse_ocr_response(mock_ocr_response("AST-1042"))

    with pytest.raises(ValueError):
        validate_identifier(parsed, "ASSET-1042")


# Negative test 2: Handle an empty OCR response.
def test_empty_response_returns_no_text():
    result = run_pipeline({}, "AST-1042")

    assert result["status"] == "NO_TEXT"
    assert result["asset_id"] is None
    assert result["identifier_valid"] is False
    assert result["matched_expected"] is False
