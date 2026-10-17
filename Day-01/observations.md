
# Day 01 — Multilingual Query Handling

**Service:** Azure AI Translator  
**Status:** NOT VERIFIED — live Azure translation has not been demonstrated.

## 1. Problem Statement

Translate fictional employee questions between English and Tamil while preserving important identifiers such as employee IDs (`EMP-104`) and leave-request IDs (`LR-102`).

## 2. Ten Potential Use Cases

1. Employee leave and leave-balance questions
2. HR policy and benefits enquiries
3. IT helpdesk requests
4. Employee onboarding assistance
5. Payroll-related questions
6. Workplace safety instructions
7. Facilities and maintenance requests
8. Attendance and shift enquiries
9. Employee training information
10. Asset and equipment support

## 3. Shortlisted Use Cases

1. **Leave requests:** Translate employee questions while preserving employee and leave-request IDs.
2. **HR policies:** Help employees understand policy information in their preferred language.
3. **IT helpdesk:** Translate technical support requests without losing ticket identifiers.
4. **Onboarding:** Make employee instructions accessible across languages.
5. **Workplace safety:** Translate safety-related instructions for multilingual employees.

### Selected Problem and Justification

The selected problem is multilingual employee leave-query translation. It is narrow enough to test with synthetic examples and has measurable requirements: translation response handling, empty-input rejection, configuration validation and identifier preservation.

## 4. Architecture

Python CLI → Input validation → Identifier protection → Azure Translator REST API adapter → Response parsing → Identifier restoration → JSON output.

The implementation reads the endpoint, subscription key and region from environment variables. Live requests require explicit opt-in.

**Current limitation:** The REST client and mocked tests are implemented, but an actual Azure Translator request has not been verified.

## 5. Request and Response Schemas

### Example request

{
  "text": "I need leave approval for EMP-104",
  "source_language": "en",
  "target_language": "ta"
}

### Expected response shape

{
  "status": "NOT_VERIFIED",
  "source_language": "en",
  "target_language": "ta",
  "translated_text": null,
  "identifiers_preserved": null
}

The response above represents an unverified example, not an actual API response. The current CLI returns a different response shape when a successful mocked or real request is processed.

## 6. Security Boundary

- Use fictional employee data for testing.
- Keep subscription keys out of source code, Git commits and logs.
- Read configuration from environment variables.
- Do not enable live calls until the resource and configuration are ready.
- Protect employee and leave-request identifiers before translation.
- Validate API responses and avoid logging secrets.
- Review identifier preservation after translation; do not assume it is guaranteed by the service.

## 7. Expected Errors

- Empty or whitespace-only input
- Missing endpoint, key or region
- Live Azure calls not approved
- HTTP request or authentication failure
- Invalid JSON or unexpected API response
- Source and target languages are identical

## 8. Bicep Validation Evidence

- Resource group: `rg-ai103-poc`
- Location: `centralindia`
- Proposed service kind: `TextTranslation`
- Proposed SKU: `F0`
- Bicep build: completed without reported errors
- Deployment validation: `provisioningState: Succeeded`

Evidence files:
- `Day-01/results/bicep-validation.json`
- `Day-01/results/bicep-build.txt`

Validation does not prove that the resource was deployed or that the service is available for a real translation request.

## 9. Python Test Evidence

Command:

`python -m pytest .\Day-01\tests\test_translator_cli.py -v`

Result: 5 passed.

Positive tests:
1. English-to-Tamil response handling
2. Employee and leave-request identifier preservation
3. Tamil-to-English response handling

Negative tests:
1. Empty input rejection
2. Missing configuration rejection

The tests use mocked HTTP responses. They verify local program behaviour and do not prove Azure connectivity.

Saved output: `Day-01/results/pytest-results.txt`

## 10. Free Allowance, Cost and Cleanup

- The proposed F0 tier must be checked for actual availability and applicable pricing before deployment.
- Free allowances and eligibility are not guaranteed.
- No actual Translator usage or resulting charge has been verified.
- No Translator resource deployment has been confirmed in this task.
- Do not delete or modify shared resource groups.
- If a resource is later created specifically for this project, record its resource ID and obtain approval before deleting it.
- Record any quota, region, access or subscription restrictions as blockers.

## 11. Blockers and Current Status

**Status: NOT VERIFIED**

The local implementation, five unit tests, Bicep build and Bicep validation have been completed. The live Translator resource and API call remain unverified.

Next actions:
1. Validate YAML configuration and CI checks.
2. Save sanitized example request and response evidence.
3. Confirm deployment approval and pricing before creating resources.
4. If deployment is not approved or cannot be completed, retain NOT VERIFIED and document the reason.

## 12. Five Scenario Questions and Answers

**Q1. Why protect employee identifiers before translation?**  
A. To reduce the risk of IDs being altered by translation and restore the original identifiers afterward.

**Q2. Why reject empty input?**  
A. Empty text is not a useful translation request and should be rejected before making a network call.

**Q3. Why use environment variables for configuration?**  
A. They separate configuration and secrets from source code.

**Q4. Do five passing unit tests prove Azure Translator is working?**  
A. No. The tests use mocked responses. A real API call is required to verify live integration.

**Q5. What should be recorded if Azure deployment is blocked?**  
A. Record NOT VERIFIED, the observed blocker, validation and test evidence, and the steps required for a future real API call.
