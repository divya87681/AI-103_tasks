# Day 02 — Intent-related text analysis

**Service:** Azure AI Language

**Problem statement:** Extract key phrases/entities and compare classification heuristics against supported Language features.

**Required evidence:** Text analysis JSON, limitations report

## Implementation steps
1. List ten possible use cases for this service and shortlist five; justify the selected problem.
2. Design request/response schemas, architecture, security boundary and expected errors.
3. Update `../infra/main.bicep` and `../infra/main.bicepparam` for this service; validate with Azure CLI.
4. Update YAML configuration and CI checks; no manual Azure portal steps.
5. Implement Python client or CLI using official SDK/REST API; read secrets from environment/managed identity.
6. Record three passing and two negative tests, API responses, and cost observations.
7. If blocked, write `NOT VERIFIED` and supply a mock adapter plus documented real call; never label a mock as Azure success.

## Required files
- `src/` Python implementation
- `tests/` positive and negative tests
- `results/` sanitized JSON responses and test output
- `observations.md` architecture decisions, cost, blockers, cleanup, five scenario Q&A

## Acceptance checks
- [ ] Bicep compiled and deployment validation recorded
- [ ] YAML config validated and CI passing
- [ ] Python CLI runs
- [ ] Actual Azure call demonstrated OR objective marked NOT VERIFIED
- [ ] Three positive and two failure tests
- [ ] Permissions and cleanup documented

## Final Implementation Status

- Azure AI Language resource: Deployed successfully.
- Resource kind: TextAnalytics.
- SKU: F0.
- Region: centralindia.
- Bicep build and deployment validation: Passed.
- Live API integration: Verified; a real Azure response was received.
- Full automated test suite: 12 passed.
- Live response evidence: `results/live-language-response.json`.
- Test evidence: `results/full-test-results.txt`.

### Observed Limitation

Azure AI Language extracted key phrases and named entities from the
synthetic employee leave request. The identifier `EMP-104` was split
into `EMP` and `104`; entity recognition does not guarantee preservation
of application-specific identifiers.

### Final Acceptance Status

Core implementation and live API test completed. Review the limitations
report, CI validation, and cost observations before final submission.
