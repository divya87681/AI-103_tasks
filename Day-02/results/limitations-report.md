# Day 02 - Azure AI Language Text Analysis Limitations

## Verification status

NOT VERIFIED - No live Azure AI Language request has been demonstrated.

## Local mock behaviour

The local adapter uses predefined phrase matching, regular expressions for synthetic identifiers, and keyword-based classification heuristics. Its output is for testing program flow only.

## Limitations

1. Key phrases are selected by local rules, not by an AI language model.
2. Entity extraction recognises only synthetic identifiers such as EMP-104, LR-102, and INC-103.
3. The classification heuristic is a rule-based comparison, not an Azure Language classification result.
4. The local mock does not provide Azure confidence scores.
5. The current mock supports only a small set of English keywords and patterns.
6. The output must not be presented as a real Azure API response.

## Real Azure verification still required

A live integration requires an Azure AI Language resource, its endpoint, valid authentication, and a successful REST API response for key phrase extraction and entity recognition.

No resource deployment or live request has been performed for this Day-02 implementation.

## Cost and cleanup

Local tests and mock execution do not make Azure API calls. No Azure Language usage cost has been verified. Do not deploy a resource without explicit approval. Review current pricing and subscription eligibility before any future live test.
