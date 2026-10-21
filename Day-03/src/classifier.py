
from pathlib import Path

LABELS = {"laptop", "keyboard", "mouse"}


def classify_image(image_path: str, adapter: str = "mock") -> dict:
    """
    Mock classification for testing the workflow.
    This does not use a trained machine-learning model.
    """
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {path}")

    if adapter != "mock":
        raise ValueError(
            "Only the mock adapter is implemented. "
            "Real Azure classification is NOT_VERIFIED."
        )

    filename = path.stem.lower()
    matches = [label for label in LABELS if label in filename]

    if len(matches) != 1:
        raise ValueError(
            "Filename must contain exactly one label: "
            "laptop, keyboard, or mouse."
        )

    return {
        "image": path.name,
        "label": matches[0],
        "confidence": None,
        "adapter": "mock",
        "verification_status": "NOT_VERIFIED",
        "note": "Label inferred from filename; no image model was used."
    }
