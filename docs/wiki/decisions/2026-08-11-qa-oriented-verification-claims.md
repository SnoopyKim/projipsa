---
id: decision.qa-oriented-verification-claims.2026-08-11
type: decision
status: active
confidence: confirmed
updated: 2026-08-11
sources:
  - plugins/projipsa/shared/outsource.md
  - plugins/projipsa/codex-skills/outsource/references/verification.md
  - plugins/projipsa/codex-skills/outsource/references/delivery-contract.md
  - plugins/projipsa/codex-skills/outsource/references/delivery-protocol.md
  - plugins/projipsa/codex-skills/projipsa/assets/templates/delivery.md
  - scripts/validate_package.py
  - tests/test_package_contract.py
related:
  - project.current-state
  - project.overview
supersedes: []
superseded_by: []
---

# Verify claims from the user or QA perspective

## Decision

Outsource verifies the final result from the position of the service user,
artifact consumer, operator, or QA reviewer who depends on it. Verification
starts from the confirmed contract and the actual user or data path, not from
the implementer's helpers, test names, or explanation.

The verification contract is fail-closed at the claim boundary:

- a preservation prohibition such as "must not change" or "must not overwrite"
  becomes a negative acceptance criterion when the delivery touches an
  adjacent path;
- planned evidence names the actual path, risk, and proportionate normal,
  negative, regression, boundary, or failure cases before implementation;
- observed evidence is `direct`, `proxy`, `reported`, or `not_run`;
- technical verdicts are `passed`, `partial`, `failed`, `blocked`, or
  `not_applicable`;
- aggregate verification is `passed` only when every required criterion has a
  suitable passing verdict;
- Maker acceptance and terminal handoff preserve rather than rewrite the
  technical verdict.

An incomplete result may still move to `REVIEW` so the Maker can judge the
evidence, request repair, change the contract, or explicitly accept an
exclusion or residual risk. It may not be described as fully verified.

Verifier independence is risk-based. Consequential data, authorization,
security, historical-record, operational, multi-layer, and negative-invariant
work should receive a distinct verifier pass. A separate agent is preferred
when available, but not mandatory; a single agent may perform a fresh
contract-first QA pass because independence of judgment, not agent count, is
the invariant.

## Context

Version 0.3.1 already distinguished technical completion, verification, and
Maker acceptance and instructed a verifier to start fresh from the contract.
Its delivery template, however, held only a criterion, one evidence-or-review
cell, and one status. It could not distinguish planned from observed evidence,
proxy evidence from an executed final path, or technical verification from
Maker acceptance.

Real Project-mode use exposed the consequence: implementation-authored helper
tests, a path that exited early, and tests following the implementation's own
branches were recorded as broader acceptance evidence even though adjacent
user and data paths remained unverified. The contract was substantially
correct, but the evidence claim was too broad.

## Alternatives Considered

- Require an independent agent for every Project-mode verification.
- Apply fail-closed verification only to Project mode.
- Convert every non-goal into a negative acceptance criterion.
- Prevent `VERIFY` from moving to `REVIEW` while any criterion is incomplete.
- Require pull-request review as the final verifier for every delivery.

## Reasoning

- A user or QA posture is portable across code, operations, data, documents,
  designs, and research; an implementation-centric test rule is not.
- Risk, hidden coupling, and consequence determine the need for independence
  more accurately than engagement mode alone.
- Mandatory agent count would couple the protocol to host capacity without
  guaranteeing independent judgment.
- Untouched excluded scope is different from a preservation invariant that an
  adjacent change could violate.
- `REVIEW` is where incomplete evidence must become visible. Blocking review
  would hide rather than solve the gap; blocking an unsupported passing claim
  is the useful invariant.
- Pull-request review is one code-specific final-artifact adapter. Other
  deliverables need reconciliation, operator preflight, source review, or an
  equivalent consumer-facing check.

## Consequences

- Outsource loads a dedicated `verification.md` reference only when `VERIFY`
  or evidence judgment is next.
- Delivery contracts and maintained delivery pages record preservation
  invariants, actual paths, planned cases, observed evidence levels, verifier
  mode, technical verdict, and residual risk.
- Execution status, verification status, and Maker decision remain independent
  durable fields.
- The package validator and unit tests preserve the new reference and delivery
  template surface.
- Static validation preserves the required contract and template structure,
  but it cannot judge whether evidence truly exercises a runtime path or
  whether a model follows the protocol. A future model-behavior evaluation
  harness remains necessary for those semantic checks.
