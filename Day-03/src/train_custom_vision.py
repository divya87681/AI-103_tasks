
import os
import sys
import time

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials

endpoint = os.environ["CUSTOM_VISION_TRAINING_ENDPOINT"]
key = os.environ["CUSTOM_VISION_TRAINING_KEY"]
project_id = os.environ["CUSTOM_VISION_PROJECT_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": key})
trainer = CustomVisionTrainingClient(endpoint, credentials)

print("Starting Azure Custom Vision training...")
iteration = trainer.train_project(project_id)

print(f"Iteration ID: {iteration.id}")
print(f"Initial status: {iteration.status}")

deadline = time.time() + 900

while time.time() < deadline:
    current = trainer.get_iteration(project_id, iteration.id)
    print(f"Training status: {current.status}")

    if current.status == "Completed":
        print("TRAINING SUCCEEDED")
        sys.exit(0)

    if current.status in ("Failed", "Error"):
        print(f"TRAINING FAILED: {current.status}")
        sys.exit(1)

    time.sleep(10)

print("Training is still in progress after 15 minutes.")
print("Check the iteration status again before starting another training run.")
