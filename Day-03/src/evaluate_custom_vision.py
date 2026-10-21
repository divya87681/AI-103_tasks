
import json
import os
from pathlib import Path

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials

root = Path(__file__).resolve().parents[2]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]
endpoint = os.environ["CUSTOM_VISION_PREDICTION_ENDPOINT"]
key = os.environ["CUSTOM_VISION_PREDICTION_KEY"]

client = CustomVisionPredictionClient(
    endpoint,
    ApiKeyCredentials(in_headers={"Prediction-key": key}),
)

results = []

for label in ("laptop", "keyboard", "mouse"):
    image_path = root / "data" / "training" / label / f"{label}_01.jpg"

    with image_path.open("rb") as image:
        prediction = client.classify_image(
            project_id,
            "office-asset-v1",
            image,
        )

    ranked = sorted(
        prediction.predictions,
        key=lambda item: item.probability,
        reverse=True,
    )

    results.append({
        "image": f"{label}/{image_path.name}",
        "expected_label": label,
        "predicted_label": ranked[0].tag_name if ranked else None,
        "probabilities": {
            item.tag_name: round(item.probability, 4)
            for item in ranked
        },
    })

output = root / "Day-03" / "results" / "class-predictions.json"
output.write_text(json.dumps(results, indent=2), encoding="utf-8")

print(json.dumps(results, indent=2))
print(f"Saved results to: {output}")
