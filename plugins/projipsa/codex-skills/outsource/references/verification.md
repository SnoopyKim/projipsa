# Verification

Use this reference when `VERIFY` is next or when evidence must be judged. The
goal is not to confirm that the implementation behaves as its author intended.
The goal is to determine, from the service user, artifact consumer, or QA
reviewer's position, which contracted claims the final result actually proves.

## Contents

1. QA posture
2. Risk-shaped cases
3. Evidence suitability
4. Evidence matrix and verdicts
5. Verifier independence
6. Final-artifact adapters

## 1. QA posture

Begin from the confirmed contract and the final artifact, not from the
implementer's explanation, helper boundaries, or existing test names.

For each criterion:

1. Name the actor who depends on the outcome: service user, operator, API
   consumer, maintainer, reviewer, or another concrete role.
2. State the starting conditions and observable outcome in that actor's terms.
3. Trace the real path through every relevant boundary, such as input, UI or
   command, application state, payload, authorization, persistence or side
   effect, and returned result.
4. Reproduce the promised normal path.
5. Try to disprove the claim with the most consequential negative, regression,
   boundary, and failure cases.
6. Inspect the final artifact and existing-code interaction when tests alone do
   not expose hidden coupling.

The Maker still owns acceptance. "User or QA perspective" describes the
technical verification posture; it does not transfer the Maker's authority to
an imagined persona.

## 2. Risk-shaped cases

Choose cases in proportion to consequence and uncertainty. Do not require an
exhaustive matrix for every criterion. Common dimensions include:

- new and existing records;
- present values, nulls, blanks, and malformed values;
- select, reselect, clear, retry, and cancel behavior;
- normal, partial, prefixed, duplicate, and corrupted inputs;
- before and after approval or authorization;
- included fields and explicitly prohibited fields;
- permitted and denied users or tenants;
- configured, missing, and invalid operating environments.

Separate two kinds of non-goal:

- **Excluded scope** is work the delivery does not undertake and does not touch.
- **Preservation invariant** is behavior that must remain absent or unchanged
  while the delivery touches an adjacent path. Promote it to a negative
  acceptance criterion and verify it.

Before implementation, record the critical normal path, each preservation
invariant, and the highest-risk regression or failure cases. After
implementation, the verifier may add adversarial cases discovered from the
artifact or changed-surface review.

## 3. Evidence suitability

Use one evidence level for each observed result:

- `direct` — the final artifact or relevant user, data, permission, or operating
  boundary was exercised or inspected directly;
- `proxy` — a helper, mock, static analysis, or narrower path supports the claim
  without exercising its final boundary;
- `reported` — another actor reports the result but the verifier did not
  reproduce or inspect it;
- `not_run` — the path was not exercised.

Match evidence to the claim:

| Claim | Normally required evidence |
|---|---|
| User workflow or save behavior | The actual interaction and final save or side-effect path |
| Authorization or tenancy | The enforcing server or data boundary, including a denied case |
| Operational command | Documented invocation through the relevant preflight and happy path, without treating help or early exit as full proof |
| Data preservation | Before/after state or the final payload and persistence boundary, including null or existing-value cases |
| Negative invariant | Changed-surface inspection plus a runtime or payload case capable of exposing the prohibited behavior |
| Parser or import behavior | Representative normal, partial, malformed, and ignored inputs with reconciliation of outputs and omissions |

Use the strongest feasible direct evidence. When direct execution is unsafe,
unauthorized, unavailable, or disproportionate, keep the verdict `partial` or
`blocked`, record the proxy evidence and reason, and expose the residual risk.
Do not convert feasibility limits into a passing result.

## 4. Evidence matrix and verdicts

Use this matrix for Scoped or Project work when verification is not obvious:

| AC | Claim and risk | Actual user or data path | Cases executed | Observed evidence | Level | Verifier mode | Technical verdict | Residual risk |
|---|---|---|---|---|---|---|---|---|

Allowed technical verdicts:

- `passed` — suitable evidence passes every required case for the criterion;
- `partial` — some relevant evidence passes, but a required boundary or case is
  absent or proxy-only;
- `failed` — evidence contradicts the criterion;
- `blocked` — a required check cannot proceed because of an external,
  environmental, or authority boundary;
- `not_applicable` — the criterion does not apply, with a recorded reason.

The aggregate verification status is `passed` only when every required
criterion is `passed` or validly `not_applicable`. An early exit, a warning
gate, a helper test, a build, or a Maker walkthrough proves only the behavior
it actually covers.

`REVIEW` may present partial, failed, or blocked verification. It must label the
technical status accurately and request a disposition rather than silently
promote it. Maker acceptance does not change a technical verdict. If an
accepted result reaches terminal `HANDOFF` with exclusions or residual risk,
preserve those non-passing verdicts and narrow the completion claim.

## 5. Verifier independence

Prefer a verifier who did not implement the change when hidden logic or
consequential failure makes independent judgment material. Use a distinct pass
by default for data writes or migrations, authorization and tenancy, security,
historical-data preservation, operational commands, multi-layer changes,
preservation invariants, and workflows whose helper layer differs from the
final save or side-effect path.

When a separate verifier is unavailable, the same agent must:

1. set aside the implementation narrative;
2. reopen the contract and design cases from the actor's observable outcome;
3. inspect the complete final changed surface when one exists;
4. trace the actual user or data path across boundaries;
5. challenge tests that mirror implementation branches;
6. record unexecuted areas and residual risk before judging the verdict.

Independence means independence of judgment, not mandatory agent count.

## 6. Final-artifact adapters

Adapt the QA posture to the deliverable:

- **Version-controlled code** — inspect the full base-to-head changed surface,
  existing-code interaction, and the real runtime path; a pull-request review
  is one suitable final verifier when it is in scope.
- **Data or migration work** — use dry runs where possible, reconcile counts and
  omissions, inspect before/after state, and test rollback or recovery.
- **Operational workflows** — follow the documented invocation as an operator,
  cross the relevant preflight, and distinguish command acceptance from the
  downstream outcome.
- **Documents, designs, or research** — review the final artifact as its reader
  or decision-maker, check source traceability and omissions, and do not treat
  author self-review as independent evidence.
- **External or hard-to-reverse effects** — stop at the authority boundary when
  necessary, verify the strongest safe precursor, and leave the effect blocked
  or partial until authorized direct evidence exists.
