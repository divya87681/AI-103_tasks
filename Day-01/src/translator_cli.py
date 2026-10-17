
"""Day 01: Azure AI Translator CLI.

Live Azure calls require explicit approval and environment configuration.
"""

import argparse
import json
import os
import re
import sys

import requests


IDENTIFIER_PATTERN = re.compile(r"\b(?:EMP-\d+|LR-\d+)\b")


class TranslatorError(Exception):
    """Raised when translation cannot be completed safely."""


def protect_identifiers(text):
    """Replace employee and leave-request IDs before translation."""
    identifiers = []

    def replace(match):
        token = f"ZXQID{len(identifiers)}QXZ"
        identifiers.append((token, match.group(0)))
        return token

    return IDENTIFIER_PATTERN.sub(replace, text), identifiers


def restore_identifiers(text, identifiers):
    """Restore identifiers after translation."""
    for token, original in identifiers:
        text = text.replace(token, original)
    return text


def translate(
    text,
    source_language="en",
    target_language="ta",
    session=requests,
):
    """Translate text using Azure AI Translator REST API."""
    if not isinstance(text, str) or not text.strip():
        raise TranslatorError("Input text cannot be empty.")

    if source_language == target_language:
        raise TranslatorError(
            "Source and target languages must be different."
        )

    # Check required configuration before making any network request.
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "").rstrip("/")
    key = os.getenv("AZURE_TRANSLATOR_KEY", "")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "")

    if not endpoint or not key or not region:
        raise TranslatorError(
            "Missing Translator configuration in environment variables."
        )

    # Explicit opt-in prevents accidental live Azure calls.
    if os.getenv("AZURE_TRANSLATOR_LIVE_APPROVED", "").lower() != "true":
        raise TranslatorError(
            "Live Azure calls are disabled. Explicit approval is required."
        )

    protected_text, identifiers = protect_identifiers(text)

    try:
        response = session.post(
            f"{endpoint}/translate",
            params={
                "api-version": "3.0",
                "from": source_language,
                "to": target_language,
            },
            headers={
                "Ocp-Apim-Subscription-Key": key,
                "Ocp-Apim-Subscription-Region": region,
                "Content-Type": "application/json",
            },
            json=[{"Text": protected_text}],
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()

        translated_text = payload[0]["translations"][0]["text"]
        translated_text = restore_identifiers(
            translated_text, identifiers
        )

        identifiers_preserved = all(
            identifier in translated_text
            for _, identifier in identifiers
        )

        return {
            "status": "VERIFIED",
            "service": "Azure AI Translator",
            "source_language": source_language,
            "target_language": target_language,
            "translated_text": translated_text,
            "identifiers_preserved": identifiers_preserved,
        }

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        raise TranslatorError(
            f"Translation failed: {type(exc).__name__}"
        ) from exc


def main():
    parser = argparse.ArgumentParser(
        description="Day 01 multilingual translation CLI"
    )
    parser.add_argument("--text", required=True)
    parser.add_argument("--from-lang", default="en")
    parser.add_argument("--to-lang", default="ta")
    args = parser.parse_args()

    try:
        result = translate(
            args.text,
            source_language=args.from_lang,
            target_language=args.to_lang,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except TranslatorError as exc:
        print(
            json.dumps(
                {
                    "status": "NOT_VERIFIED",
                    "error": str(exc),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
