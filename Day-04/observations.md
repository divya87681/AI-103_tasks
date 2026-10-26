# Day 04 — Equipment-Label OCR: Observations

## Verification Status

- Live Azure AI Vision OCR API: VERIFIED
- Synthetic equipment-label OCR: VERIFIED
- Asset identifier extraction: VERIFIED
- Correct and incorrect identifier validation: VERIFIED
- Day-04 automated tests: 8 PASSED
- Live OCR response saved: YES
- Pipeline validation evidence saved: YES
- Dedicated resource group deployment: NOT VERIFIED
- Overall deployment status: NOT DEPLOYED

The live OCR request successfully recognized the synthetic equipment label.
The Python pipeline extracted AST-1042 and matched it against the expected
identifier. All eight Day-04 automated tests passed.

The dedicated resource group `rg-ai103-day04-vision` was created successfully
but remains empty. The existing F0 Vision resource in `rg-ai103-poc` was used
for the live OCR test. No additional Azure resource was deployed.

## 1. Problem Statement

Read fictional equipment labels using Azure AI Vision OCR and validate
the extracted asset identifiers against an expected identifier.

The synthetic label contained:

- Asset ID: AST-1042
- Equipment: Laptop
- Department: IT

The pipeline must extract readable text, identify asset IDs matching
`AST-####`, validate the identifier format, and compare the extracted
identifier with the expected value.

## 2. Architecture

Workflow:

1. Create a synthetic equipment-label image.
2. Authenticate using Azure CLI and Microsoft Entra ID.
3. Obtain a temporary access token for Azure Cognitive Services.
4. Submit the image to the Azure AI Vision Image Analysis API.
5. Request the Read feature to recognize text in the image.
6. Save the actual API response as JSON evidence.
7. Parse the response using `ocr_pipeline.py`.
8. Extract the asset identifier using the regular expression
   `\bAST-\d{4}\b`.
9. Calculate the mean of available word-confidence scores.
10. Validate the identifier format and compare it with the expected ID.
11. Save the pipeline output as JSON evidence.

### Main components

- `src/azure_adapter.py`: Azure OCR REST API integration and safeguards.
- `src/mock_adapter.py`: Synthetic OCR response for offline testing.
- `src/ocr_pipeline.py`: Text extraction, identifier detection,
  confidence calculation, and validation.
- `src/cli.py`: Command-line interface for mock and Azure modes.
- `tests/test_azure_adapter.py`: Azure adapter safety tests.
- `tests/test_ocr_pipeline.py`: OCR parsing and validation tests.
- `config.example.yaml`: Example configuration.
- `results/`: Images and JSON evidence.

### API details

- Service: Azure AI Vision
- Operation: Image Analysis with the Read feature
- API version: `2024-02-01`
- Authentication: Microsoft Entra ID bearer token
- Token audience: `https://cognitiveservices.azure.com/`
- Image content type: `application/octet-stream`

The live request used the existing resource endpoint. The endpoint and
temporary access token should not be committed as secrets or exposed in logs.

## 3. Azure Resource and Bicep Validation

### Existing resource

- Resource group: `rg-ai103-poc`
- Resource SKU: F0
- Resource kind: ComputerVision
- Local authentication: Disabled
- Live OCR API request: Successful

### Dedicated resource group

- Resource group: `rg-ai103-day04-vision`
- Location: `centralindia`
- Creation status: Succeeded
- Resource inventory: Empty

The dedicated resource group was created to separate Day-04 resources.
However, no Azure service was deployed into it.

### Validation findings

Bicep compilation succeeded previously.

Deployment validation using the F0 Computer Vision configuration failed
with the Azure error `CanNotCreateMultipleFreeAccounts`, because the
subscription allows only one free account for this account type.

Validation with the S1 SKU succeeded, but this was validation only.
No S1 resource was deployed.

Do not deploy S1 without reviewing the possible charges and obtaining
explicit approval.

The successful live OCR test used the existing F0 resource in
`rg-ai103-poc`. It does not prove that a new resource can be deployed
into the dedicated resource group.

## 4. Live OCR Evidence

### Equipment label

File: `results/equipment_label.png`

The synthetic image contains the following information:

- EQUIPMENT ASSET LABEL
- Asset ID: AST-1042
- Equipment: Laptop
- Department: IT

### Live API response

File: `results/equipment-label-ocr-response.json`

Azure AI Vision returned the following recognized text:

EQUIPMENT ASSET LABEL
Asset ID. AST-1042
Equipment Laptop
Department IT

The punctuation differs slightly from the original image, but the asset
identifier was recognized correctly.

The response contains `AST-1042` in both the full asset-label line and
the individual recognized word/line data.

### Python pipeline result

File: `results/equipment-label-validation.json`

Observed result:

- Status: SUCCESS
- Extracted asset ID: AST-1042
- Asset ID count: 1
- Mean available word confidence: 0.9645
- Available confidence scores: 10
- Identifier format valid: true
- Expected identifier matched: true

The confidence mean is the average of the available word-confidence
scores. It is not a guarantee of overall OCR accuracy.

The earlier `results/live-ocr-response.json` file contains the OCR response
from a presentation image and is separate from the equipment-label test.

## 5. Automated Tests

Command executed:

`python -m pytest .\Day-04\tests -v`

Result: 8 passed.

### Positive tests

1. `test_valid_asset_identifier_matches`
   - A correctly extracted identifier matches the expected identifier.

2. `test_text_and_confidence_are_extracted`
   - Recognized text and available confidence scores are extracted.

3. Live equipment-label OCR test
   - The actual Azure AI Vision response contained `AST-1042`.
   - The Python pipeline extracted and validated the identifier.
   - Evidence was saved to JSON.

### Negative tests

1. `test_different_valid_asset_id_does_not_match`
   - A valid but different expected ID does not match the extracted ID.

2. `test_invalid_expected_identifier_raises_error`
   - An expected identifier that does not follow the required format
     raises a ValueError.

### Additional safety and edge-case tests

- `test_live_calls_disabled_by_default`
- `test_missing_endpoint_is_rejected`
- `test_missing_image_is_rejected`
- `test_empty_response_returns_no_text`

The incorrect-ID integration check used expected ID `AST-9999`.
The extracted ID remained `AST-1042`, `identifier_valid` was true,
and `matched_expected` was false.

The eight pytest tests are automated tests. The live Azure request and
its pipeline validation are separate evidence of a successful live call.

## 6. Authentication and Security

- Authenticate with Azure CLI and Microsoft Entra ID.
- Obtain a short-lived access token for the Cognitive Services audience.
- Do not save bearer tokens in project files or JSON evidence.
- Do not commit access tokens, passwords, or API keys.
- Keep live Azure calls disabled by default in the configuration.
- Require explicit approval before enabling live calls through the
  Python adapter.
- Use synthetic equipment labels and fictional identifiers for testing.
- Keep the existing resource's local authentication disabled.
- Do not enable local authentication merely to bypass a permission error.
- Do not deploy resources or change SKU without approval.

## 7. Cost Considerations and Cleanup

### Cost considerations

The live test used the existing F0 Vision resource. No additional service
was deployed for the equipment-label test.

The subscription's F0 account limit blocked validation of another free
Computer Vision account.

S1 validation succeeded previously, but no S1 deployment was performed.
S1 may incur charges; confirm current pricing and deployment settings
before considering it.

Actual costs depend on the resource SKU, usage, region, and applicable
Azure pricing. No cost estimate or billing amount was verified during
this exercise.

### Cleanup

The following project evidence should be retained:

- `results/equipment_label.png`
- `results/equipment-label-ocr-response.json`
- `results/equipment-label-validation.json`
- `results/live-ocr-response.json`

These files contain the synthetic test evidence and OCR results.

The dedicated resource group `rg-ai103-day04-vision` is empty.
If it is no longer required, it can be deleted after confirming that
it contains no resources needed by other work.

Do not delete `rg-ai103-poc` or its existing Vision resource as part
of Day-04 cleanup without reviewing dependencies and obtaining approval.

Temporary access tokens should not be retained. Remove the token variable
from the PowerShell session after use.

## 8. Five Scenario Questions and Answers

### Q1. What happens if the OCR response contains no readable text?

The pipeline returns `NO_TEXT` when the parsed text is empty. The caller
should handle the missing text rather than assuming an asset identifier
was found.

### Q2. What happens if the extracted ID is AST-1042 but the expected ID
is AST-9999?

The extracted identifier remains format-valid, but `matched_expected`
is false. This distinguishes identifier format validation from matching
the expected asset.

### Q3. Why use Microsoft Entra ID instead of an API key?

Microsoft Entra ID provides token-based authentication and can use
Azure role assignments. In this project, the live REST request succeeded
with a bearer token obtained through Azure CLI. The resource's local
authentication remains disabled.

### Q4. Why keep a mock adapter if the live Azure call works?

The mock adapter supports repeatable tests without depending on network
availability, Azure permissions, quotas, or service charges. Mock results
must be identified as mock results and must never be reported as proof
of live Azure success.

### Q5. What should be done if a second F0 Vision account cannot be
validated in the dedicated resource group?

Keep the existing resource unchanged, document the
`CanNotCreateMultipleFreeAccounts` limitation, and avoid deploying S1
without approval. The existing F0 resource can be referenced for the
live test while the dedicated resource group remains empty.

## 9. Remaining Work

- [x] Live Azure AI Vision OCR request succeeded.
- [x] Synthetic equipment-label image created.
- [x] Asset ID AST-1042 extracted.
- [x] Correct identifier validation succeeded.
- [x] Incorrect expected identifier was rejected as a match.
- [x] All eight Day-04 automated tests passed.
- [x] Live response and validation evidence saved.
- [x] Dedicated resource group created.
- [ ] Dedicated resource deployment: blocked by the subscription's F0
      account limit; no deployment performed.
- [ ] Review the complete CI workflow result after the latest changes.
- [ ] Review Git status and commit the intended project changes.

### Full project test suite — final verification

Command: `python -m pytest -v`
Result: 25 passed in 0.87 seconds.

This includes the Day-04 OCR pipeline and Azure adapter tests,
as well as the existing project tests.
