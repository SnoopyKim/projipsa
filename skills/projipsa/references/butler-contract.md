# Projipsa Butler Contract

## Purpose

Projipsa is one project-butler Plugin with one portable public Skill and focused
internal capabilities. The `projipsa` Skill routes and synthesizes; it does not
absorb every specialist procedure. A capability remains independently
specified and testable even though both supported hosts enter it through the
shared Skill.

## Shared authority model

Keep these concerns distinct:

1. **Project truth** — source-backed facts, decisions, state, evidence, risks,
   and open questions that belong to one project.
2. **Active delivery state** — a current contract, milestone, evidence matrix,
   review state, and exact next action for delegated work.
3. **Maker-level preferences** — confirmed reusable preferences that may apply
   across projects and require a Maker-controlled storage decision.
4. **Reusable protocol** — versioned Projipsa Skill instructions, references,
   scripts, templates, adapters, and evaluations.

Project truth and authorized active delivery state belong in the established
project-memory root. Do not place private Maker-level preferences, secrets, or
raw customer data there merely because a project uses Projipsa.

## Capability contract

Every sibling capability must:

- declare a narrow triggering boundary;
- inspect project instructions and preserve unrelated work;
- use the established memory root instead of creating competing project state;
- separate read authority from write authority;
- distinguish direct evidence, inference, recommendation, and Maker decision;
- use host-native tools and permission controls without promising unavailable
  capabilities;
- return an inspectable outcome, verification, residual risk, and next action;
- propose or perform a project-memory handoff only when authorized.

Keep capability-specific temporary state only as long as necessary. Project
mode delivery may persist a maintained `delivery` page because continuity is
part of its contract.

## Routing rules

- Route onboarding and repair to `init`.
- Route querying, ingesting, updating, linting, and snapshots to `memory`.
- Route substantial explicitly delegated work to `outsource`.
- Leave ordinary domain work in the host's normal workflow.

Recommend a capability when it would materially improve the result, but do not
treat a recommendation as consent. In particular, do not begin Outsource's
Deep Interview or Delivery Contract merely because a task is complex.

## Memory handoff

A capability handoff should contain only durable project value:

- verified current-state changes;
- meaningful decisions and rationale;
- active assumptions, risks, and open questions;
- evidence paths and residual validation gaps;
- accepted scope and explicit exclusions;
- the exact next useful action.

Do not store a transcript or duplicate stable source artifacts. Link stable
project evidence; preserve ephemeral source material under the raw layer when
authorized.

## Adding a future capability

Add an internal capability rather than a nested Plugin when the capability:

- belongs to the project-butler concept;
- can follow this shared authority and handoff contract;
- benefits from the same project memory;
- has a distinct trigger and procedure worth loading independently.

Update the main router, README, package validator, and representative tests
together. Add a separate public entry point only when both supported hosts can
enforce the same invocation boundary. Split into a separate Plugin only when
it needs a genuinely independent product boundary, installation lifecycle,
permissions model, or audience.
