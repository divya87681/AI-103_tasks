
import os
import requests
from azure.identity import DefaultAzureCredential


API_VERSION = "2024-02-01"


class AzureOCRError(RuntimeError):
    """Raised when Azure OCR configuration or a request fails."""


def analyze_image(image_path: str) -> dict:
    """Submit an image to Azure AI Vision Read, using Entra ID."""
    endpoint = os.getenv("AZURE_VISION_ENDPOINT", "").strip().rstrip("/")

    if not endpoint:
        raise AzureOCRError(
            "Missing AZURE_VISION_ENDPOINT environment variable"
        )

    if os.getenv("LIVE_AZURE_CALLS_APPROVED", "false").lower() != "true":
        raise AzureOCRError(
            "Live Azure calls are disabled; approval is required"
        )

    if not os.path.isfile(image_path):
        raise AzureOCRError(f"Image file not found: {image_path}")

    url = (
        f"{endpoint}/computervision/imageanalysis:analyze"
        f"?api-version={API_VERSION}&features=read"
    )

    try:
        credential = DefaultAzureCredential()
        token = credential.get_token(
            "https://cognitiveservices.azure.com/.default"
        )

        with open(image_path, "rb") as image_file:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {token.token}",
                    "Content-Type": "application/octet-stream",
                },
                data=image_file,
                timeout=60,
            )

        if response.status_code >= 400:
            raise AzureOCRError(
                f"Azure OCR returned HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        return response.json()

    except AzureOCRError:
        raise
    except Exception as exc:
        raise AzureOCRError(
            f"Azure OCR request failed: {type(exc).__name__}: {exc}"
        ) from exc
