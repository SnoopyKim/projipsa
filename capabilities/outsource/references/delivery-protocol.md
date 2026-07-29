# Delivery Protocol

Use this reference to choose engagement weight, run the outer lifecycle, persist state, route feedback, and decide whether delivery is actually complete.

## Contents

1. Engagement modes
2. Outer lifecycle
3. Durable state
4. Feedback and change routing
5. Completion semantics
6. Pausing and escalation

## 1. Engagement modes

Assess five dimensions. Do not expose a numeric score unless it helps the Maker understand a recommendation.

| Dimension | Low | Medium | High |
|---|---|---|---|
| Ambiguity | Outcome and boundaries are clear | Important details need discovery | The problem or desired change is still uncertain |
| Risk | Easy to reverse; local effect | Meaningful regression or operational risk | Security, money, data, customers, production, or hard-to-reverse effect |
| Continuity | One short working session | May pause or require a follow-up | Multiple milestones, long-running work, or handoffs |
| Breadth | One bounded component | Several coupled components | Multiple systems, external dependencies, or independently owned scopes |
| Governance | Final review is enough | One or two material decisions | Repeated Maker reviews, approvals, or change management |

Choose:

- **Ordinary workflow** when all dimensions are low and the result is
  straightforward to inspect. Exit Outsource instead of wrapping small work in
  engagement terminology.
- **Scoped** when at least one dimension is medium, no unmanaged high-risk effect exists, and one compact contract can bound the work.
- **Project** when any high dimension materially affects delivery, or when milestones, durable state, repeated review, or operational handoff are necessary.

Examples:

- Rename a label and run the existing test: ordinary workflow.
- Add a bounded feature across API and UI with a known user flow: Scoped.
- Build and launch a new service with payments, analytics, and operations: Project.

Reclassify when discovery changes the evidence. Record why the mode changed.

## 2. Outer lifecycle

| State | Purpose | Required output | Normal next state |
|---|---|---|---|
| `QUALIFY` | Inspect context and size the engagement | Ordinary-work route or mode, rationale, initial unknowns | Exit Outsource, `INTERVIEW`, or `PROPOSE` |
| `INTERVIEW` | Discover consequential intent, context, constraints, and risks | Interview synthesis, decisions, assumptions, open questions | `PROPOSE` |
| `PROPOSE` | Translate understanding into a responsible delivery offer | Draft Delivery Contract and alternatives | `CONFIRM` |
| `CONFIRM` | Resolve material choices and establish authority | Confirmed or revised contract | `DELIVER` |
| `DELIVER` | Produce the contracted deliverables | Inspectable artifacts, work log, implementation checks | `VERIFY` |
| `VERIFY` | Test each acceptance criterion with direct evidence | Evidence matrix and verdicts | `REVIEW` or inner repair |
| `REVIEW` | Present results for Maker judgment | Review package and feedback classification | `ACCEPT`, `CHANGE`, or repair |
| `CHANGE` | Evaluate a new desire or changed constraint | Impact analysis and contract revision | `CONFIRM` |
| `ACCEPT` | Record the Maker's acceptance decision | Accepted scope, exclusions, residual risks | `HANDOFF` |
| `HANDOFF` | Make operation, maintenance, and continuation clear | Handoff notes, next actions, persisted state, and any unpersisted improvement proposal | Terminal |

Maintain one outer state at a time. Inner execution may have its own state, but it never replaces the outer state.

Do not turn handoff into an automatic personal-profile or protocol write. A
reusable preference or improvement observed during delivery remains a proposal
in the review package until the Maker separately authorizes both its scope and
storage location.

## 3. Durable state

Project mode should preserve at least:

```text
project:
mode:
outer_state:
contract_version:
goal:
current_milestone:
decisions:
assumptions:
open_questions:
work_items:
approvals:
changes:
evidence:
risks:
maker_feedback:
next_action:
updated_at:
```

Use the established Projipsa project-memory root when it exists and memory
maintenance is authorized. For Project mode, keep the current contract and
fields above in one maintained `wiki/deliveries/<slug>.md` page using the
Projipsa Memory delivery template. Use normal decision, question, assumption,
risk, milestone, raw-source, and log pages for their respective durable
responsibilities, and link them from the delivery page.

Do not create a second `.outsource/`, `project-state/`, or transcript store
beside initialized Projipsa memory. If the project is not initialized, use the
simplest available state for the engagement and propose Projipsa initialization
when Project-mode continuity justifies it. Initialization remains a separately
authorized write.

Store public project facts separately from private Maker strategy or customer
material. Keep secrets in an approved secret store, never in project state.

State is not a transcript. Preserve decisions and evidence needed to resume, not every conversational token.

## 4. Feedback and change routing

Classify feedback before editing:

| Feedback class | Meaning | Route |
|---|---|---|
| Contract defect | The result fails a confirmed criterion | Diagnose and repair inside `DELIVER` |
| Misunderstanding | The contract encoded the Maker's intent incorrectly | Reopen `INTERVIEW`, then revise |
| Change request | The Maker now wants something outside or different from the contract | `CHANGE` with impact analysis |
| Preference | A reusable way the Maker may prefer to work or review | Present an unpersisted preference proposal for a separate decision |
| Next-phase idea | Valuable but unnecessary for current acceptance | Record separately; do not expand current scope |

Do not hide scope growth inside repair. Do not charge a contract defect against the Maker as a new request.

For a change request, report:

- requested change;
- affected deliverables and criteria;
- schedule, cost, risk, and dependency impact;
- preserved work;
- recommendation;
- revised contract version requiring confirmation.

## 5. Completion semantics

Keep three distinct statuses:

```text
EXECUTED  = the planned artifact or action exists
VERIFIED  = required evidence passes
ACCEPTED  = the Maker has reviewed and accepted the result
```

Do not infer `ACCEPTED` from silence, a passing test, or an agent report. Scoped
work may end with “verified and ready for your review” when an explicit
acceptance record is unnecessary, but it still must not claim the Maker's
subjective judgment.

An acceptance package should include:

- delivered outcome and scope;
- artifacts or changed behavior;
- acceptance criteria and evidence;
- important decisions and deviations;
- known limitations and residual risk;
- operating or rollback instructions when relevant;
- requested Maker decision.

## 6. Pausing and escalation

Before pausing, persist the current state, contract version, completed evidence,
unresolved decisions, risks, and exact next action. If project-memory writes
are not authorized, present that content as a proposed Projipsa handoff and
state that it has not been persisted.

Escalate only when progress requires:

- a material Maker decision;
- additional authority;
- access to essential external state;
- acceptance of a residual risk;
- resolution of contradictory requirements;
- a new strategy after repeated evidence-backed failure.

Give the Maker concrete choices and consequences. Do not use escalation as a substitute for investigation Outsource can safely perform.
