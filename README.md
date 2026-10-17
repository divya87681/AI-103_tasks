# Multilingual Enterprise Knowledge Assistant

## Mission
Build a fictional training project over seven working days using **Bicep + YAML + Python only** for implementation. No Azure Portal, Foundry portal, Azure UI, or other GUI cloud administration. Azure CLI is allowed for authentication, Bicep deployment, resource inspection, and cleanup.

## Timebox and guardrails
- Seven days; aim for 4–5 focused engineering hours per day.
- Python CLI first; no frontend. Synthetic or fictional data only.
- Engineers write Bicep for Azure resource definitions, YAML for configuration/CI, and Python for SDK/API calls, validation, and tests. No click-ops.
- Each engineer owns their own source and test evidence. Shared subscription quotas are **not per engineer**.
- Free allowance shown in Azure billing is **not** a guarantee of free provisioning; verify tier, region, offer eligibility, meter, and costs before deployment.
- Do not deploy without approval. Bicep validation is mandatory even if deployment is blocked. Never commit keys, passwords, connection strings, or PII. Prefer Entra ID / managed identity.
- If service cannot be provisioned, deliver a runnable local interface plus real SDK/API integration plan and mark objective **NOT VERIFIED**.
- Azure CLI and Python SDK can be used to retrieve endpoints and validate resources; do not manually configure resources in a portal.

## Daily plan

| Day | Service | Task | Required evidence |
|---|---|---|---|
| 1 | Azure AI Translator | Multilingual query handling: Translate fictional employee questions across two languages and preserve key identifiers. | Language-aware Python CLI and tests |
| 2 | Azure AI Language | Intent-related text analysis: Extract key phrases/entities and compare classification heuristics against supported Language features. | Text analysis JSON, limitations report |
| 3 | Azure Custom Vision | Asset image classification: If service provisioning is supported, train/test a tiny synthetic office-asset image classifier; otherwise use a local interface and mark NOT VERIFIED. | Model evaluation, prediction API evidence or blocked report |
| 4 | Azure AI Vision | Equipment-label OCR: Read fictional asset labels from sample images and validate extracted identifiers. | OCR pipeline and confidence/error observations |
| 5 | Azure Database for PostgreSQL | Knowledge repository: Create FAQ, role, and audit tables; enforce role-scoped lookup in Python. | Schema, seed data, query tests |
| 6 | Azure Virtual Machines + Blob Storage | CLI-based deployment: Provision an approved B1s Linux VM with Bicep if eligible; deploy Python CLI/API using scripts, store fixtures in Blob. | Deployment evidence, connectivity, least privilege, teardown |
| 7 | Integration | Multilingual employee assistant: Combine translation, FAQ lookup, text analysis, OCR, and optional classification; no LLM required. | Integrated Python CLI, architecture, cleanup, defense |

## Daily definition of done
1. `infra/main.bicep` and parameter file updated; `az bicep build` and `az deployment group validate` evidence where applicable.
2. YAML config updated and schema/values validated; CI YAML executes lint/tests and Bicep build.
3. Python SDK or REST client with an executable command and response JSON.
4. Three positive tests and two edge/failure tests, with recorded output.
5. Short architecture diagram, permissions/RBAC rationale, resource usage estimate, cleanup commands and evidence.
6. Five scenario-based review questions and answers; explicit **VERIFIED** or **NOT VERIFIED** service status.

## Day 7 acceptance
Run an end-to-end CLI workflow using actual permitted Azure services, show failure handling and 3 injected defects, and answer 10 technical questions. Deliver `docs/architecture.md`, `docs/coverage_matrix.md`, and cleanup evidence. No mock may be presented as a successful real Azure call.

## Evaluation / 100 points
- Service selection + architecture: 20
- Correct Python SDK/API integration: 25
- Bicep + YAML automation: 20
- Cross-service integration: 15
- Security, tests, reliability: 10
- Explanation / oral defense: 10

## Quick commands (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
az bicep build --file infra/main.bicep
# After subscription selection and explicit deployment approval:
# az deployment group validate --resource-group <approved-rg> --template-file infra/main.bicep --parameters infra/main.bicepparam
# az deployment group create --resource-group <approved-rg> --template-file infra/main.bicep --parameters infra/main.bicepparam
```

**Note:** `main.bicep` is deliberately a safe skeleton, not a pre-provisioned solution. Each engineer must author and review the service resource definitions on the assigned day. Azure Custom Vision and some legacy AI meters may have restrictions or retirement timelines; validate before provisioning.
