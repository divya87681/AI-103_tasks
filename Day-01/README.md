# Day 01 — Multilingual query handling

**Service:** Azure AI Translator

**Problem statement:** Translate fictional employee questions across two languages and preserve key identifiers.

**Required evidence:** Language-aware Python CLI and tests

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
