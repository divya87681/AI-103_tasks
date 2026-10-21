# Day-03 — Azure Custom Vision Asset Classification

## 1. Objective

Prepare an office-asset classification workflow for three categories: laptop, keyboard, and mouse.

## 2. Implementation

- Created a Python classifier interface in `src/classifier.py`.
- Created a command-line interface in `src/cli.py`.
- Added automated tests in `tests/test_classifier.py`.
- Added an example configuration in `config.example.yaml`.
- Extended the shared Bicep template to support Custom Vision Training and Prediction resource configurations.

## 3. Test Results

- Automated workflow tests: 5 passed, 0 failed.
- CLI smoke test: passed for a filename containing `laptop`.
- Prediction evidence: saved in `results/prediction.json`.
- Evaluation report: saved in `results/evaluation.json`.

## 4. Important Limitations

The current adapter is a mock. It infers a label from the filename and does not inspect image pixels. The test file `results/laptop_01.jpg` contains dummy text and is not a valid JPEG image.

No real image dataset was evaluated, and no model accuracy, precision, recall, or F1 score has been measured.

## 5. Azure Verification Status

**NOT_VERIFIED**

Bicep compilation and Azure deployment validation succeeded for the Custom Vision Training and Prediction configurations. These checks validate the deployment template; they do not prove that Azure resources were created, that a Custom Vision project was trained, or that live predictions work.

No live Azure classification call has been verified.

## 6. Security Boundary

- Keep Azure keys out of source code and Git.
- Read credentials from environment variables or an approved identity mechanism.
- Do not enable live Azure calls or deploy resources without approval.
- Use synthetic test data during local testing.


## 7. Remaining Work

1. Confirm approval and Azure access before any resource deployment.
2. Verify whether any Azure resources were created for this exercise.
3. Implement and verify a real Custom Vision API workflow if approved and supported.
4. Prepare valid synthetic images for laptop, keyboard, and mouse.
5. Record actual prediction responses and model evaluation metrics only after testing a trained model.
6. Verify permissions, resource costs, and cleanup status before marking the exercise fully complete.

The local mock workflow, automated tests, Bicep validation, configuration validation, and CI workflow have been completed. Real Azure image classification remains NOT VERIFIED.


## 8. Cost Observations

- Local mock classification and Python tests were run locally.
- Bicep compilation and deployment validation were performed.
- Actual Azure resource deployment and live prediction costs have not been verified.
- No claim of zero Azure cost is made because the absence of deployed resources has not been independently confirmed through a resource inventory.
- Before deployment, review the selected SKU, region, pricing, and expected usage.

## 9. Permissions and Cleanup

### Permissions

- Confirm the active Azure subscription and target resource group before deployment.
- Verify that the approved identity has the required permissions for the intended operations.
- Keep credentials out of source code and evidence files.
- Do not enable live Azure calls or deploy resources without approval.

### Cleanup

- Check the Azure resource group for resources created specifically for this exercise.
- Record the resource names and resource IDs before cleanup.
- Obtain approval before deleting any resource.
- Delete only confirmed exercise resources using the approved cleanup procedure.
- Verify the resource inventory after cleanup.

**Current status:** Resource deployment, live API permissions, and cleanup have not been verified for Day-03.

## 10. Five Scenario Q&As


**Q1. Why was office asset classification selected?**

It provides three clear categories—laptop, keyboard, and mouse—for a manageable demonstration.


**Q2. Does the current classifier recognize objects inside an image?**

No. The mock implementation infers a label from the filename and does not inspect image pixels.

**Q3. What does NOT_VERIFIED mean?**

It means a live Azure Custom Vision classification call has not been demonstrated.

**Q4. Why are accuracy, precision, recall, and F1 score null?**

No real image dataset or trained model has been evaluated.

**Q5. What must happen before live Azure classification can be claimed?**

Approval, resource and permission verification, a real API implementation, valid image inputs, and recorded prediction evidence are required.

## 11. Use Cases and Shortlist

### Ten possible use cases

1. Office asset classification — identify laptops, keyboards, and mice.
2. Equipment label reading — extract asset IDs from printed labels.
3. Invoice text extraction — read invoice numbers and totals.
4. Identity document text extraction — read permitted fields from sample documents.
5. Shipping label reading — extract tracking numbers and destination text.
6. Product packaging OCR — read product names and batch codes.
7. Printed form digitization — extract text from paper forms.
8. Nameplate reading — capture equipment model and serial numbers.
9. Signboard text extraction — read text from signs.
10. Document archive indexing — extract text to support searching.

### Five shortlisted use cases

- **Office asset classification:** useful for identifying equipment categories, but requires image classification rather than OCR alone.
- **Equipment label OCR:** selected because it directly supports extracting fictional asset identifiers and validating them.
- **Shipping label reading:** useful for extracting tracking identifiers.
- **Product packaging OCR:** useful for extracting batch codes and product details.
- **Printed form digitization:** useful for converting printed text into structured records.

### Selected problem justification

Equipment-label OCR is the selected problem because it has a clear input (a synthetic label image), a measurable output (extracted text and asset identifier), and straightforward positive and negative test cases. Identifier validation helps detect missing or malformed asset IDs.

## 12. Architecture and Request/Response Schemas

### Architecture

1. The CLI receives an image path and configuration.
2. The input validator checks file existence and supported image format.
3. The OCR adapter processes the image. The mock adapter is used for local workflow tests; it does not perform OCR.
4. The extraction layer normalizes returned text and confidence values when available.
5. The identifier validator checks the extracted asset ID against the configured format.
6. The CLI returns structured JSON and records sanitized evidence.

**Current implementation limitation:** The Day-03 classifier is filename-based mock classification, not OCR or real image recognition. The architecture above describes the intended workflow; live Azure Custom Vision behavior has not been verified.

### Example request schema

```json
{
  "image_path": "synthetic/laptop_label_01.png",
  "adapter": "mock",
  "expected_identifier_pattern": "^ASSET-[0-9]{4}$"
}
```

### Example response schema

```json
{
  "image": "laptop_label_01.png",
  "extracted_text": null,
  "asset_id": null,
  "confidence": null,
  "adapter": "mock",
  "verification_status": "NOT_VERIFIED",
  "errors": []
}
```

These are proposed OCR schemas, not output from a verified OCR call. The current Day-03 classifier response uses a `label` field and does not extract text.

## 13. Security Boundary and Expected Errors

### Security boundary

- Read service credentials from environment variables or an approved managed identity.
- Never commit API keys, access tokens, or other secrets.
- Use synthetic images and fictional asset identifiers for testing.
- Validate file paths and reject unsupported or missing files.
- Sanitize logs and API evidence to avoid exposing credentials.
- Require approval before resource deployment or live service calls.

### Expected errors

| Condition | Expected behavior |
|---|---|
| Image file missing | Return a clear file-not-found error |
| Unsupported or invalid image | Reject the input before processing |
| Asset identifier absent | Return a validation failure |
| Identifier format invalid | Mark the extracted identifier as invalid |
| Missing service configuration | Return a configuration error |
| Authentication or permission failure | Record a sanitized error; do not claim success |
| Service timeout or network failure | Return an error and preserve diagnostic information without secrets |

**Verification status:** The proposed OCR request/response flow and error cases have not been demonstrated against a live Azure Vision API. The existing Day-03 mock classifier remains `NOT_VERIFIED`.