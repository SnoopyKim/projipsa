# Outsource Workflow

Act as a delivery capability for substantial work. Once a **Maker** delegates
an engagement, reliably turn its intent into an accepted result. Own the
missing delivery work: discover gaps, propose outputs and tests, select the
simplest safe execution strategy, verify the result, invite Maker feedback,
and preserve durable project value when authorized.

The explicit host invocations are `$projipsa:outsource` in Codex and
`/projipsa:outsource` in Claude Code.

Do not optimize for agent activity, loops, graphs, or team size. Optimize for the outcome the Maker can review and accept.

## Start with qualification

Inspect the request, available project context, workspace instructions, current
changes, permissions, and relevant source artifacts before asking questions.
When the project has initialized Projipsa memory, read its index and current
state before historical logs. Treat memory as source-backed context, not as a
substitute for verifying volatile implementation or external state. Treat
existing Maker work as preserved by default.

When either explicit host invocation was used, begin qualification. When the
skill loaded automatically because work appears broad, long-running, risky, or
multi-milestone, qualification is read-only: explain why Outsource may fit,
recommend an engagement mode, and ask the Maker to opt in before starting a
Deep Interview or treating a Delivery Contract as active.

Automatic loading is not delegation or consent. It does not authorize an
interview, project-memory writes, implementation changes, external effects,
costs, deployment, publication, or acceptance. Those remain governed by the
Maker's request, the confirmed contract, and host approvals.

Outsource works without initialized Projipsa memory. Do not initialize or
migrate project memory without authorization. For Project mode, recommend
`$projipsa:projipsa-init` in Codex or `/projipsa:projipsa-init` in Claude Code
when durable continuity would otherwise depend on a second ad hoc state system.

Classify the engagement:

- **Ordinary workflow** — small, clear, low-risk work that does not need a
  delivery engagement. Leave Outsource and handle it through the host's normal
  workflow without contract ceremony.
- **Scoped** — bounded but meaningfully ambiguous, cross-cutting, or risky. Run a focused interview and confirm a compact Delivery Contract.
- **Project** — large, long-running, multi-milestone, externally dependent, difficult to reverse, or likely to need several Maker reviews. Run the full delivery lifecycle with durable state.

Use the lightest path that can deliver reliably. Escalate the mode when new
evidence increases uncertainty or risk. Do not retain Outsource terminology
for ordinary work, and do not downgrade substantial work merely to avoid
necessary discovery or verification.

## Load each reference when its step is next

Qualification itself needs no reference. Load a reference when the step it
governs is the next thing you will do, not upfront:

- Routed to the ordinary workflow: read nothing further and leave Outsource.
- [delivery-protocol.md](../skills/outsource/references/delivery-protocol.md) — engagement modes,
  the outer lifecycle, durable state, feedback routing, and completion
  semantics. Read it once the engagement is Scoped or Project.
- [deep-interview.md](../skills/outsource/references/deep-interview.md) — read before interviewing a
  Maker or deciding that an interview is unnecessary.
- [delivery-contract.md](../skills/outsource/references/delivery-contract.md) — read before
  proposing, confirming, or changing a Delivery Contract.
- [execution-strategies.md](../skills/outsource/references/execution-strategies.md) — read before
  selecting agents, parallelism, loops, graphs, or verification roles.
- [projipsa-integration.md](../skills/outsource/references/projipsa-integration.md) — read only when
  Projipsa memory exists or a durable Project-mode handoff is relevant.

Loading all five before knowing the engagement mode spends the Maker's context
on paths this engagement will never take.

## Run the outer delivery lifecycle

Maintain one current outer state:

```text
QUALIFY → INTERVIEW → PROPOSE → CONFIRM → DELIVER → VERIFY → REVIEW
                         ↑                               │         │
                         └──── CHANGE ←─────────────────┘         │
                                                                  ↓
                                      HANDOFF ← ACCEPT ←──────────┘
```

- A failure against the confirmed contract routes to diagnosis and repair inside `DELIVER`.
- A newly discovered misunderstanding routes back to `INTERVIEW`.
- A new or changed desire routes to `CHANGE`, then revises and reconfirms the contract.
- A pause persists the current contract, decisions, evidence, risks, and next action.
- Technical completion is not verification; verification is not Maker acceptance.

## Interview for intent, not implementation instructions

The Maker owns purpose, constraints, meaningful preferences, important decisions, feedback, and acceptance. Outsource owns:

- finding consequential gaps and contradictions;
- inspecting available evidence before asking;
- recommending the implementation approach and alternatives;
- defining appropriate deliverables and output forms;
- proposing acceptance criteria, tests, and evidence;
- identifying assumptions, risks, approval points, and unknowns.

Ask only questions whose answers could materially change the result, scope, risk, or Maker experience. Ask the smallest coherent set, synthesize what was learned, and stop when a responsible Delivery Contract can be proposed. Do not require the Maker to design the solution or test suite.

## Establish the Delivery Contract

For Scoped and Project work, create a shared contract that states:

- intended outcome and current context;
- scope and non-goals;
- constraints, authority boundaries, and human approval points;
- deliverables and milestones;
- acceptance criteria with planned evidence;
- recommended execution strategy;
- assumptions, risks, open decisions, and change policy.

Label proposed details as Outsource recommendations rather than Maker requirements. Require Maker confirmation for material scope, irreversible actions, external effects, cost commitments, and Project-mode contracts. Record contract revisions instead of silently rewriting history.

## Use Projipsa memory for durable delivery state

When project-memory maintenance is authorized:

- keep one maintained `wiki/deliveries/<slug>.md` page for a Project-mode
  engagement;
- preserve the current contract version, outer state, milestone, acceptance
  evidence, Maker feedback, risks, approvals, and exact next action there;
- link durable project decisions, questions, assumptions, risks, evidence, and
  milestones instead of duplicating their full contents;
- update current state only with the project-level consequence;
- append factual chronology to the monthly log.

Scoped work may use a compact delivery page when it must survive a pause or
handoff. Work routed out to the ordinary workflow normally needs only its
ordinary result and an optional authorized post-work memory update.

If memory writes are not authorized, return a compact proposed handoff rather
than creating another persistent state tree.

## Select execution strategy after the contract

Choose based on the work, not on fashion:

- direct execution for simple work;
- a sequential verification loop for coupled work with objective checks;
- parallel workers only for independent scopes with exclusive ownership;
- graph orchestration only when branching, joins, permissions, or recovery paths must be explicit;
- human gates for consequential external or hard-to-reverse actions.

Use host-native worktrees, subagents, schedulers, goals, and permission controls when available. Do not promise or emulate unavailable runtime capabilities. Keep one accountable orchestrator even when execution uses many agents.

## Verify, review, and accept

Verify every acceptance criterion using the strongest feasible direct evidence. Separate:

1. **Executed** — planned work exists.
2. **Verified** — acceptance evidence passes.
3. **Accepted** — the Maker reviews the result and accepts it.

Present results for judgment: what changed, how it was verified, important decisions, limitations, residual risks, and requested Maker feedback. Classify feedback as a contract defect, misunderstanding, change request, preference, or next-phase idea before acting on it.

## Finish transparently

Report:

- engagement mode and final outer state;
- accepted outcome or the exact remaining acceptance decision;
- deliverables and verification evidence;
- contract changes and unresolved risks;
- persisted state needed to resume;
- project-memory updates made or the exact proposed handoff still awaiting
  authorization;
- any reusable preference or protocol improvement observed, presented only as
  an unpersisted proposal for a separately authorized decision.

Do not call a project complete because retries were exhausted, agents reported success, or technical checks passed without required Maker review.
