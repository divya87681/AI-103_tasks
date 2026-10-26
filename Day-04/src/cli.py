
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from azure_adapter import analyze_image, AzureOCRError
from mock_adapter import mock_ocr_response
from ocr_pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Day-04 Azure AI Vision OCR pipeline"
    )
    parser.add_argument(
        "--mode",
        choices=["mock", "azure"],
        default="mock",
        help="Use synthetic OCR or the Azure OCR adapter",
    )
    parser.add_argument(
        "--image",
        help="Path to an image file (required in Azure mode)",
    )
    parser.add_argument(
        "--expected-id",
        default="AST-1042",
        help="Expected asset ID, for example AST-1042",
    )
    args = parser.parse_args()

    try:
        if args.mode == "mock":
            response = mock_ocr_response("AST-1042")
        else:
            if not args.image:
                parser.error("--image is required when --mode azure is used")
            response = analyze_image(args.image)

        result = run_pipeline(response, args.expected_id)
        print(json.dumps(result, indent=2))
        return 0 if result["matched_expected"] else 1

    except (AzureOCRError, ValueError) as exc:
        print(
            json.dumps({"status": "ERROR", "error": str(exc)}, indent=2),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
