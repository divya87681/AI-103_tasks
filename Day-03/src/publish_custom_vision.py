
import os

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials

endpoint = os.environ["CUSTOM_VISION_TRAINING_ENDPOINT"]
key = os.environ["CUSTOM_VISION_TRAINING_KEY"]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]
prediction_resource_id = os.environ[
    "CUSTOM_VISION_PREDICTION_RESOURCE_ID"
]

iteration_id = "6a5eeabc-bbb7-4efc-a1db-9f320c7b1a1d"
publish_name = "office-asset-v1"

credentials = ApiKeyCredentials(in_headers={"Training-key": key})
client = CustomVisionTrainingClient(endpoint, credentials)

iteration = client.get_iteration(project_id, iteration_id)
if iteration.status != "Completed":
    raise RuntimeError(f"Iteration is not completed: {iteration.status}")

if iteration.publish_name:
    print(f"Iteration is already published as: {iteration.publish_name}")
else:
    client.publish_iteration(
        project_id,
        iteration_id,
        publish_name,
        prediction_resource_id,
    )
    print(f"Published iteration as: {publish_name}")

print(f"Iteration ID: {iteration_id}")
