
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add Day-01/src to the Python import path.
DAY01_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(DAY01_SRC))

from translator_cli import (
    TranslatorError,
    protect_identifiers,
    restore_identifiers,
    translate,
)


@pytest.fixture
def azure_config(monkeypatch):
    """Provide fake configuration for local unit tests."""
    monkeypatch.setenv(
        "AZURE_TRANSLATOR_ENDPOINT",
        "https://example.invalid",
    )
    monkeypatch.setenv("AZURE_TRANSLATOR_KEY", "test-key")
    monkeypatch.setenv("AZURE_TRANSLATOR_REGION", "centralindia")
    monkeypatch.setenv("AZURE_TRANSLATOR_LIVE_APPROVED", "true")


def fake_session(translated_text):
    """Return a mocked HTTP session; no real Azure call is made."""
    session = Mock()
    response = Mock()
    response.json.return_value = [
        {
            "translations": [
                {
                    "text": translated_text,
                    "to": "ta",
                }
            ]
        }
    ]
    response.raise_for_status.return_value = None
    session.post.return_value = response
    return session


# Positive test 1: English-to-Tamil translation response.
def test_english_to_tamil_translation(azure_config):
    session = fake_session("விடுப்பு வேண்டும்")

    result = translate(
        "I need leave",
        source_language="en",
        target_language="ta",
        session=session,
    )

    assert result["status"] == "VERIFIED"
    assert result["translated_text"] == "விடுப்பு வேண்டும்"
    session.post.assert_called_once()


# Positive test 2: Employee and leave-request identifiers are preserved.
def test_identifiers_are_preserved(azure_config):
    session = fake_session(
        "Check ZXQID0QXZ and ZXQID1QXZ"
    )

    result = translate(
        "Check EMP-104 and LR-102",
        source_language="en",
        target_language="ta",
        session=session,
    )

    assert "EMP-104" in result["translated_text"]
    assert "LR-102" in result["translated_text"]
    assert result["identifiers_preserved"] is True

    sent_text = session.post.call_args.kwargs["json"][0]["Text"]
    assert "EMP-104" not in sent_text
    assert "LR-102" not in sent_text


# Positive test 3: Translation from Tamil to English.
def test_tamil_to_english_translation(azure_config):
    session = fake_session("I need leave approval")

    result = translate(
        "எனக்கு விடுப்பு ஒப்புதல் வேண்டும்",
        source_language="ta",
        target_language="en",
        session=session,
    )

    assert result["status"] == "VERIFIED"
    assert result["translated_text"] == "I need leave approval"


# Negative test 1: Blank input must be rejected.
def test_empty_input_is_rejected():
    with pytest.raises(
        TranslatorError,
        match="Input text cannot be empty",
    ):
        translate("   ")


# Negative test 2: Missing configuration must be rejected.
def test_missing_configuration_is_rejected(monkeypatch):
    monkeypatch.delenv("AZURE_TRANSLATOR_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_TRANSLATOR_KEY", raising=False)
    monkeypatch.delenv("AZURE_TRANSLATOR_REGION", raising=False)
    monkeypatch.setenv("AZURE_TRANSLATOR_LIVE_APPROVED", "true")

    with pytest.raises(
        TranslatorError,
        match="Missing Translator configuration",
    ):
        translate("I need leave approval")
