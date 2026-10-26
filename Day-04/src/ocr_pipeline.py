
import re
from statistics import mean


ASSET_ID_PATTERN = re.compile(r"\bAST-\d{4}\b")


def parse_ocr_response(response: dict) -> dict:
    """Extract text lines and available word-confidence scores from OCR JSON."""
    lines = []
    confidences = []

    read_result = response.get("readResult", {})

    for block in read_result.get("blocks", []):
        for line in block.get("lines", []):
            text = line.get("text", "").strip()
            if text:
                lines.append(text)

            for word in line.get("words", []):
                confidence = word.get("confidence")
                if isinstance(confidence, (int, float)):
                    if 0 <= confidence <= 1:
                        confidences.append(float(confidence))

    full_text = "\n".join(lines)
    matches = ASSET_ID_PATTERN.findall(full_text)

    return {
        "text": full_text,
        "asset_id": matches[0] if matches else None,
        "asset_id_count": len(matches),
        "confidence_mean": (
            round(mean(confidences), 4) if confidences else None
        ),
        "confidence_word_count": len(confidences),
    }


def validate_identifier(parsed: dict, expected_asset_id: str) -> dict:
    """Validate the identifier format and compare it with the expected ID."""
    if not re.fullmatch(r"AST-\d{4}", expected_asset_id):
        raise ValueError("Expected asset ID must match AST-1234 format")

    extracted = parsed.get("asset_id")
    valid = bool(extracted and ASSET_ID_PATTERN.fullmatch(extracted))

    return {
        "identifier_valid": valid,
        "matched_expected": valid and extracted == expected_asset_id,
    }


def run_pipeline(response: dict, expected_asset_id: str) -> dict:
    """Combine OCR parsing and identifier validation."""
    parsed = parse_ocr_response(response)
    validation = validate_identifier(parsed, expected_asset_id)

    return {
        "status": "SUCCESS" if parsed["text"] else "NO_TEXT",
        **parsed,
        **validation,
    }
