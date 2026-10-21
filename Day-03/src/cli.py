
import argparse
import json
import sys

from classifier import classify_image


def main():
    parser = argparse.ArgumentParser(
        description="Day-03 office asset classifier (mock adapter)"
    )
    parser.add_argument("image", help="Path to an image file")
    parser.add_argument(
        "--adapter",
        default="mock",
        choices=["mock"],
        help="Classification adapter (mock only)"
    )
    args = parser.parse_args()

    try:
        result = classify_image(args.image, adapter=args.adapter)
        print(json.dumps(result, indent=2))
        return 0
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
