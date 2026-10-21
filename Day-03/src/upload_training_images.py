
import os
from pathlib import Path

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials

ROOT = Path(__file__).resolve().parents[2]
TRAINING_DIR = ROOT / "data" / "training"
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

endpoint = os.environ["CUSTOM_VISION_TRAINING_ENDPOINT"]
key = os.environ["CUSTOM_VISION_TRAINING_KEY"]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]

credentials = ApiKeyCredentials(
    in_headers={"Training-key": key}
)
client = CustomVisionTrainingClient(endpoint, credentials)

# Reuse existing tags instead of creating duplicates.
existing_tags = client.get_tags(project_id)
tags = {tag.name.lower(): tag for tag in existing_tags}

required_labels = ("laptop", "keyboard", "mouse")
missing = [label for label in required_labels if label not in tags]
if missing:
    raise RuntimeError(f"Missing Azure tags: {missing}")

files = []
for label in required_labels:
    folder = TRAINING_DIR / label
    if not folder.is_dir():
        raise FileNotFoundError(f"Training folder not found: {folder}")

    images = [
        path for path in sorted(folder.iterdir())
        if path.is_file() and path.suffix.lower() in VALID_EXTENSIONS
    ]
    if len(images) < 5:
        raise ValueError(f"{label}: expected at least 5 images, found {len(images)}")

    for path in images:
        if path.stat().st_size == 0:
            raise ValueError(f"Empty image file: {path}")
        files.append((label, path))

print(f"Validated {len(files)} local image files.")

uploaded = 0
for label, path in files:
    with path.open("rb") as image_stream:
        result = client.create_images_from_data(
            project_id,
            image_stream.read(),
            tag_ids=[tags[label].id],
        )

    if result.is_batch_successful:
        uploaded += 1
        print(f"Uploaded: {label}/{path.name}")
    else:
        errors = [
            f"{item.source_url}: {item.status}"
            for item in result.images
            if item.status != "OK"
        ]
        raise RuntimeError(
            f"Upload failed for {label}/{path.name}: {errors}"
        )

print(f"Upload complete: {uploaded}/{len(files)} images.")
