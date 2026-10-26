
def mock_ocr_response(asset_id="AST-1042", confidence=0.98):
    """Return a synthetic OCR response for offline testing."""
    return {
        "readResult": {
            "blocks": [
                {
                    "lines": [
                        {
                            "text": f"ASSET ID: {asset_id}",
                            "words": [
                                {
                                    "text": "ASSET",
                                    "confidence": confidence,
                                },
                                {
                                    "text": "ID:",
                                    "confidence": confidence,
                                },
                                {
                                    "text": asset_id,
                                    "confidence": confidence,
                                },
                            ],
                        }
                    ]
                }
            ]
        }
    }
