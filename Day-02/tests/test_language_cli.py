import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "language_cli.py"
SPEC = importlib.util.spec_from_file_location("language_cli", MODULE_PATH)
language_cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(language_cli)


def test_it_support_request_extracts_mock_phrases():
    result = language_cli.mock_analyze(
        "My laptop is broken and I cannot access the payroll system"
    )
    assert result["status"] == "MOCK_ONLY_NOT_AZURE"
    assert "laptop" in result["key_phrases"]
    assert result["heuristic_category"] == "IT_SUPPORT"


def test_employee_identifier_is_detected():
    result = language_cli.mock_analyze(
        "I need leave approval for EMP-104"
    )
    assert result["entities"] == [
        {"text": "EMP-104", "type": "SYNTHETIC_IDENTIFIER"}
    ]
    assert result["heuristic_category"] == "HR_LEAVE"


def test_invoice_text_is_classified_by_local_heuristic():
    result = language_cli.mock_analyze(
        "Please review invoice INV-205 and payment"
    )
    assert result["heuristic_category"] == "FINANCE"
    assert result["status"] == "MOCK_ONLY_NOT_AZURE"


def test_empty_input_is_rejected():
    with pytest.raises(language_cli.LanguageAnalysisError):
        language_cli.mock_analyze("   ")


def test_non_string_input_is_rejected():
    with pytest.raises(language_cli.LanguageAnalysisError):
        language_cli.mock_analyze(None)
