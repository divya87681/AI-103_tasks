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
