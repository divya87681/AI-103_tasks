
import json
import os
from pathlib import Path

from azure.cognitiveservices.vision.customvision.prediction import (
    CustomVisionPredictionClient,
)
from msrest.authentication import ApiKeyCredentials

endpoint = os.environ["CUSTOM_VISION_PREDICTION_ENDPOINT"]
key = os.environ["CUSTOM_VISION_PREDICTION_KEY"]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]
published_name = "office-asset-v1"

# Use an image that was uploaded to the training project.
image_path = (
    Path(__file__).resolve().parents[2]
    / "data" / "training" / "laptop" / "laptop_01.jpg"
)

if not image_path.is_file():
    raise FileNotFoundError(f"Test image not found: {image_path}")

credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})
client = CustomVisionPredictionClient(endpoint, credentials)

with image_path.open("rb") as image:
    result = client.classify_image(
        project_id,
        published_name,
        image,
    )

evidence = {
    "verification_status": "VERIFIED",
    "adapter": "azure_custom_vision",
    "image": image_path.name,
    "project_id": project_id,
    "published_model": published_name,
    "predictions": [
        {
            "tag": prediction.tag_name,
            "probability": round(prediction.probability, 4),
        }
        for prediction in result.predictions
    ],
}

output_path = (
    Path(__file__).resolve().parents[1]
    / "results" / "real-prediction.json"
)
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

print(json.dumps(evidence, indent=2))
print(f"Evidence saved to: {output_path}")
