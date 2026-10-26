# Observations

Status: NOT VERIFIED

## Architecture

## Bicep validation

## Python API/SDK evidence

## Positive tests (3)

## Negative tests (2)

## Free allowance / cost / cleanup

## Five scenario questions and answers

## Day 05 — Knowledge Repository

### 1. Objective
Build a knowledge repository with FAQ storage, role-based access control, and audit logging using PostgreSQL.

### 2. Architecture
- `schema.sql`: Defines `user_roles`, `faqs`, and `audit_logs`.
- `seed.sql`: Provides sample users and FAQs.
- `src/knowledge_repository.py`: Implements the in-memory reference implementation.
- `src/postgres_adapter.py`: Implements parameterized PostgreSQL queries and role checks.
- `src/cli.py`: Provides a command-line interface for FAQ lookup.
- `config.example.yaml`: Documents database and security configuration.
- `tests/test_knowledge_repository.py`: Tests successful and denied lookups.
- `results/test-output.txt`: Captures automated test output.
- `results/postgres-status.json`: Records live-connection verification status.

### 3. Security decisions
- Use parameterized SQL queries to reduce SQL injection risk.
- Read database credentials from the `DATABASE_URL` environment variable.
- Reject unknown and inactive users.
- Enforce role-based FAQ access.
- Record lookup outcomes in the audit table.
- Do not commit real credentials or connection strings.
- Production deployment should use a managed identity or a securely stored secret and least-privilege database permissions.

### 4. Test results
- Automated mock tests: 9 passed.
- YAML configuration validation: passed.
- Python syntax compilation: passed.
- Live PostgreSQL connection: NOT VERIFIED because `DATABASE_URL` is not configured.
- Azure deployment: NOT STARTED.

### 5. Cost observations
- Local Python development and mock tests use no Azure resources.
- A managed PostgreSQL service may incur compute, storage, backup, and networking charges.
- Actual Azure costs have not been measured because no Azure PostgreSQL resource was deployed.
- Review the selected Azure region, service tier, storage, and estimated monthly usage before provisioning.

### 6. Blockers
- No PostgreSQL connection string is configured.
- The schema and seed SQL have not been executed against a live PostgreSQL database.
- Live database behavior, database permissions, and audit persistence remain NOT VERIFIED.
- Azure infrastructure deployment and live service calls have not been performed.

### 7. Cleanup
- Remove temporary local environment variables when no longer needed.
- Never store database passwords in source files or commit them to Git.
- No Azure resources were created during this work, so no Azure resource cleanup is currently required.
- Before any future Azure deployment, use a dedicated resource group rather than `rg-ai103-poc`, unless explicitly approved otherwise.

### 8. Five scenario Q&As

**Scenario 1: Can an Employee read an Employee-level FAQ?**
Yes. The mock implementation permits the lookup when the user is active and the FAQ is active.

**Scenario 2: Can an Employee read a Manager-level FAQ?**
No. The lookup is denied and an audit status of `DENIED` is recorded by the mock implementation.

**Scenario 3: What happens when the user is inactive or unknown?**
The lookup is rejected. The mock implementation records a denied status.

**Scenario 4: What happens when an FAQ does not exist?**
The lookup raises a not-found error. The mock implementation records `NOT_FOUND`.

**Scenario 5: Has live PostgreSQL access been demonstrated?**
No. It is marked NOT VERIFIED until a database is configured and the schema, seed data, permissions, and queries are tested against it.
