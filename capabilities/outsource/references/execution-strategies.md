# Execution Strategies

Use this reference after the Delivery Contract is sufficiently clear. Choose the simplest topology that preserves accountability, safety, and verification.

## Strategy matrix

| Strategy | Use when | Avoid when |
|---|---|---|
| Single-agent direct | Contracted work can be performed by one accountable agent with an obvious check | Discovery or independent verification is material |
| Sequential verified | Work is coupled but benefits from a distinct implementation and verification pass | Several scopes can proceed independently |
| Parallel scoped | Independent work items have exclusive ownership and clear integration | Shared files or hidden dependencies dominate |
| Graph | Branches, joins, role permissions, recovery paths, or long-lived routing must be explicit | A sequence or small loop is sufficient |
| Human-gated | External, costly, sensitive, or hard-to-reverse actions | The action is safe, reversible, and already authorized |

Strategies can be composed. A graph node may contain a local verification loop; a parallel plan may end in one human-gated integration.

## Selection sequence

1. Start with single-agent direct execution.
2. Add a distinct verification pass if correctness cannot be judged from the artifact alone.
3. Add parallelism only for independently understandable and testable scopes.
4. Add a graph only when explicit routing is necessary for correctness, governance, or recovery.
5. Add human gates according to consequence and authority, regardless of topology.

Do not select a strategy to maximize agent count or demonstrate a concept.

## Accountable roles

Use roles dynamically:

- **Delivery Orchestrator** — owns the contract, plan, state transitions, authority, integration, review package, and final claims.
- **Investigator** — gathers facts, separates inference from evidence, and identifies uncertainty.
- **Implementer** — changes only the assigned scope and returns inspectable artifacts and checks.
- **Verifier** — judges criteria from raw artifacts and reproduced evidence, independent of the implementation narrative.
- **Integrator** — resolves convergence points and runs aggregate checks.

One agent may perform roles sequentially in single-agent or capacity-limited
work, but it must make a fresh verification pass from the contract rather than
self-approve from memory.

## Inner execution lifecycle

Inside outer `DELIVER`, use:

```text
DISCOVER → PLAN → ASSIGN → EXECUTE → VERIFY
                                      │
                     pass → INTEGRATE ┤
                                      │
                     fail → DIAGNOSE → REPAIR → VERIFY
```

If diagnosis shows the Delivery Contract is wrong or incomplete, leave the inner lifecycle and route to outer `INTERVIEW` or `CHANGE`.

## Work contracts and ownership

Every non-trivial assignment should state:

- observable objective;
- allowed read and write scope;
- forbidden changes and external actions;
- acceptance criteria and source evidence;
- dependencies and preserved Maker work;
- required checks;
- report format and failure behavior.

Assign exclusive write ownership before parallel work. Give shared manifests, schemas, lockfiles, and integration points one owner. Stop and replan when hidden coupling violates ownership.

## Evidence and repair

Prefer:

1. direct inspection of final artifacts;
2. executed tests, builds, static checks, or behavior checks;
3. edge, regression, permission, and integration checks;
4. reports that cite reproducible evidence.

Unsupported completion claims do not pass.

Classify failures before repair:

- implementation;
- test;
- environment;
- requirement or contract;
- integration;
- authorization;
- unknown.

Normally review strategy after three verify–diagnose–repair cycles. Repeated failure should reopen assumptions or discovery rather than trigger the same retry. Exhaustion is not success.

## Runtime portability

Discover host capabilities at runtime. Use native subagents, worktrees, goals, schedulers, and approval systems when available. The protocol should define meaning and evidence, not hard-code a model, concurrency count, directory, shell, or framework.

Do not emulate forbidden capabilities or claim background persistence, cost controls, or automatic permissions that the host does not provide.
