"""Day 02: Azure AI Language text-analysis CLI.

Mock mode is the default. Live calls require explicit opt-in.
Mock results are never presented as Azure results.
"""

import argparse
import json
import os
import re
import sys

import requests


class LanguageAnalysisError(Exception):
    """Raised when text analysis cannot be completed safely."""


def mock_analyze(text):
    """Return deterministic local examples, not real AI analysis."""
    if not isinstance(text, str) or not text.strip():
        raise LanguageAnalysisError("Input text cannot be empty.")

    words = re.findall(r"\b[\w-]+\b", text.lower())
    keywords = [
        phrase
        for phrase in ("payroll system", "laptop", "leave approval",
                       "password", "invoice", "network")
        if phrase in text.lower()
    ]

    entities = re.findall(r"\b(?:EMP-\d+|LR-\d+|INC-\d+)\b", text)

    if not keywords:
        keywords = list(dict.fromkeys(words[:5]))

    lower = text.lower()
    if any(word in lower for word in ("broken", "error", "cannot", "failed")):
        heuristic_category = "IT_SUPPORT"
    elif any(word in lower for word in ("leave", "vacation", "absence")):
        heuristic_category = "HR_LEAVE"
    elif "invoice" in lower or "payment" in lower:
        heuristic_category = "FINANCE"
    else:
        heuristic_category = "UNCLASSIFIED"

    return {
        "status": "MOCK_ONLY_NOT_AZURE",
        "service": "Azure AI Language",
        "input_text": text,
        "key_phrases": keywords,
        "entities": [
            {"text": entity, "type": "SYNTHETIC_IDENTIFIER"}
            for entity in entities
        ],
        "heuristic_category": heuristic_category,
        "limitations": [
            "Key phrases are selected by local rules, not an AI model.",
            "Entities are limited to synthetic identifier patterns.",
            "The heuristic category is not an Azure classification result."
        ]
    }


def live_analyze(text, session=requests):
    """Call Azure AI Language key phrase and entity recognition APIs."""
    if not isinstance(text, str) or not text.strip():
        raise LanguageAnalysisError("Input text cannot be empty.")

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT", "").rstrip("/")
    key = os.getenv("AZURE_LANGUAGE_KEY", "")
    approved = os.getenv("AZURE_LANGUAGE_LIVE_APPROVED", "").lower()

    if not endpoint or not key:
        raise LanguageAnalysisError(
            "Missing AZURE_LANGUAGE_ENDPOINT or AZURE_LANGUAGE_KEY."
        )

    if approved != "true":
        raise LanguageAnalysisError(
            "Live Azure calls are disabled; explicit approval is required."
        )

    url = f"{endpoint}/language/:analyze-text"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    def request_analysis(kind):
        body = {
            "kind": kind,
            "analysisInput": {
                "documents": [
                    {"id": "1", "language": "en", "text": text}
                ]
            },
            "parameters": {"modelVersion": "latest"}
        }
        try:
            response = session.post(
                url,
                params={"api-version": "2022-05-01"},
                headers=headers,
                json=body,
                timeout=20
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            raise LanguageAnalysisError(
                f"Azure Language request failed: {type(exc).__name__}"
            ) from exc

    phrases_result = request_analysis("KeyPhraseExtraction")
    entities_result = request_analysis("EntityRecognition")

    try:
        phrases = phrases_result["results"]["documents"][0]["keyPhrases"]
        entities = entities_result["results"]["documents"][0]["entities"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LanguageAnalysisError(
            "Azure returned an unexpected response structure."
        ) from exc

    return {
        "status": "LIVE_AZURE_RESPONSE_RECEIVED",
        "service": "Azure AI Language",
        "key_phrases": phrases,
        "entities": entities,
        "heuristic_category": "NOT_PROVIDED_BY_THIS_HEURISTIC",
        "note": "Classification heuristic is separate from Azure analysis."
    }


def main():
    parser = argparse.ArgumentParser(
        description="Day 02 Azure AI Language text analysis"
    )
    parser.add_argument("--text", required=True)
    parser.add_argument(
        "--mode", choices=("mock", "live"), default="mock"
    )
    args = parser.parse_args()

    try:
        result = (
            mock_analyze(args.text)
            if args.mode == "mock"
            else live_analyze(args.text)
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except LanguageAnalysisError as exc:
        print(json.dumps({
            "status": "NOT_VERIFIED",
            "error": str(exc)
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
