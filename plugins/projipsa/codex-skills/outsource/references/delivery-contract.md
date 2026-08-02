# Delivery Contract

Use this reference to translate interview evidence into a shared, versioned basis for delivery and acceptance. This is a working project agreement, not a legal contract.

## Contents

1. Contract rules
2. Canonical template
3. Compact contract
4. Confirmation
5. Contract changes

## Contract rules

- Write observable outcomes rather than vague effort commitments.
- Mark each statement as confirmed fact, Maker decision, Outsource recommendation, or assumption when ambiguity matters.
- Let Outsource propose deliverables, tests, and evidence; do not misrepresent them as Maker-authored requirements.
- Keep non-goals explicit to prevent silent scope growth.
- Give every acceptance criterion an evidence method or an explicit Maker-review method.
- Record material changes as new versions.
- Require confirmation for Project mode and for consequential scope, cost, external effect, or irreversible action.

## Canonical template

```markdown
# Delivery Contract: <project>

- Version: 0.1
- Status: draft | confirmed | changed | accepted | superseded
- Engagement mode: Scoped | Project
- Maker:
- Outsource host:
- Updated:
- Confirmed by:
- Confirmed at:

## 1. Intended outcome

What observable change will exist, for whom, and why it matters.

## 2. Current context

Relevant current behavior, source artifacts, users, constraints, and baseline.

## 3. Scope

- Included:
- Excluded:
- Explicit non-goals:

## 4. Constraints and authority

- Technical and operating constraints:
- Budget or schedule boundaries:
- Actions Outsource may take:
- Actions requiring Maker approval:
- Forbidden or unavailable actions:

## 5. Recommended approach

- Recommendation:
- Why:
- Material alternative:
- Trade-off:

## 6. Deliverables

| ID | Deliverable | Output form | Owner | Review point |
|---|---|---|---|---|

## 7. Acceptance and evidence

| ID | Acceptance criterion | Evidence or test | Reviewer | Status |
|---|---|---|---|---|

## 8. Milestones

| Milestone | Exit condition | Maker checkpoint | Dependencies |
|---|---|---|---|

## 9. Execution strategy

- Selected strategy:
- Why it is the simplest reliable option:
- Roles or ownership, if needed:
- Recovery and stopping rules:

## 10. Assumptions, risks, and unknowns

| Item | Type | Impact | Validation or mitigation | Owner |
|---|---|---|---|---|

## 11. Open decisions

| Decision | Recommendation | Maker choice needed by | Consequence |
|---|---|---|---|

## 12. Change policy

How new desires, misunderstandings, contract defects, and next-phase ideas will be classified.

## 13. Review and acceptance

- Review package:
- Known limitations:
- Residual risks:
- Maker decision: pending | accepted | accepted with exclusions | changes requested

## 14. Change log

| Version | Change | Reason | Confirmed by |
|---|---|---|---|
```

## Compact contract

Scoped work may use:

```markdown
## Compact Delivery Contract

- Outcome:
- Scope / non-goals:
- Deliverables:
- Acceptance criteria and evidence:
- Constraints / approvals:
- Assumptions / risks:
- Strategy:
- Maker review point:
```

Scoped work whose outcome and boundaries are already clear may skip a separate
interview and move from qualification to a compact proposal. Keep the contract
weight proportional, but do not make material authority, risk, or acceptance
boundaries implicit.

When a contract needs durable Project-mode state, maintain its current form in
the Projipsa Memory `delivery` page rather than copying it into current state or
creating a second state tree. Preserve prior versions through the delivery
page's change log and linked project chronology. Store a full previous contract
as raw evidence only when its exact wording materially matters.

## Confirmation

Ask for confirmation only when it is a meaningful boundary. State:

- what Outsource understood;
- what Outsource recommends;
- which choices remain the Maker's;
- what actions confirmation authorizes;
- what remains separately gated.

Confirmation does not authorize commits, pushes, deployments, purchases, outbound messages, production changes, or other external effects unless they are explicitly included and permitted.

## Contract changes

When evidence or feedback changes the contract:

1. Preserve the previous version.
2. Classify the trigger: misunderstanding, new requirement, constraint change, risk discovery, or infeasible assumption.
3. Explain impact on deliverables, criteria, milestones, cost, and risk.
4. Recommend a disposition.
5. Create a new version and reconfirm material changes.

Never silently edit acceptance criteria after implementation merely to make the result pass.
