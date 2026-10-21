
import os
from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials

endpoint = os.environ["CUSTOM_VISION_TRAINING_ENDPOINT"]
key = os.environ["CUSTOM_VISION_TRAINING_KEY"]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": key})
client = CustomVisionTrainingClient(endpoint, credentials)

iterations = client.get_iterations(project_id)

for iteration in iterations:
    print(
        f"Name: {iteration.name} | "
        f"ID: {iteration.id} | "
        f"Status: {iteration.status} | "
        f"Published name: {iteration.publish_name}"
    )
