# Projipsa Integration

Outsource is independently useful. Integrate it with Projipsa memory only when
the project has already adopted that memory system or the Maker authorizes
initialization separately.

## Detect existing memory

1. Look for `docs/index.md` or a memory root declared by project instructions.
2. Read the current-state page before historical logs.
3. Verify volatile implementation or external claims against their live source.
4. Do not auto-initialize memory. Suggest `$projipsa-init` when continuity would
   benefit from adoption, migration, or repair.

## Persist only authorized durable state

When project-memory maintenance is within scope:

- use one maintained `wiki/deliveries/<slug>.md` page for Project-mode state;
- use a compact delivery page for Scoped work only when it must survive a
  meaningful pause or handoff;
- preserve the current contract, outer state, milestone, evidence, feedback,
  approvals, risks, and exact next action;
- link durable decisions, questions, assumptions, risks, evidence, and
  milestones instead of duplicating them;
- keep current state about present project consequences and append chronology
  to the monthly log;
- never store the interview transcript as project truth.

If memory writes are not authorized, return a compact proposed handoff instead
of creating a second state tree. If no Projipsa memory exists, use the host's
simplest suitable temporary or task-local state and keep Outsource functional.
