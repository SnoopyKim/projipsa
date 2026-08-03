# Memory Contract

## Canonical layers

Projipsa uses four layers with distinct authority:

1. **Raw sources** preserve imported or captured evidence.
2. **Maintained wiki pages** hold current synthesized understanding.
3. **Append-only logs** preserve chronology without becoming current truth.
4. **Derived layers** provide search, graph, dashboard, or summary views and
   must be rebuildable from the first three layers.

Do not make a derived layer the only place where a project fact or decision
exists.

## Default memory root

Use `docs/` in repositories unless the project already has an established,
durable equivalent. Reuse that equivalent instead of creating a competing
tree.

Hosts discover that root through different files: Codex reads `AGENTS.md` and
Claude Code reads `CLAUDE.md`. A `projipsa:memory-pointer` block in the project's
root instruction files names the selected root for both, and takes precedence
over the `docs/` default when the two disagree.

The universal core is:

```text
docs/
  AGENTS.md
  index.md
  raw/YYYY-MM/
  wiki/project/
  wiki/decisions/
  wiki/questions/
  logs/YYYY-MM.md
```

Add `areas`, `assumptions`, `risks`, `procedures`, `external`, `milestones`, or
`deliveries` only when the project's real operating model needs them. Do not
create empty families for symmetry.

## Authority boundaries

Projipsa may:

- read current memory to prepare context;
- point out stale, contradictory, unsupported, or missing information;
- make documentation changes within an authorized memory-maintenance task;
- recommend decisions, questions, mitigations, and next work.

Projipsa may not:

- infer Maker acceptance or approval;
- silently turn a recommendation into a confirmed decision;
- modify implementation during docs-only work;
- promote a project fact into a reusable personal preference;
- store secrets or raw private customer data as general project memory;
- rewrite history to make a later outcome look inevitable.

## Host integration

Other agents, plugins, and Projipsa capabilities may consume project memory,
but the maintained wiki remains the project-level source of current truth.
Project-mode delegated work may keep its current Delivery Contract and outer
state in one maintained `wiki/deliveries/` page. It must still link durable
decisions, risks, questions, milestones, and evidence rather than silently
duplicating them.

Avoid hard runtime dependencies at first. If Projipsa is unavailable, another
agent may preserve a compact handoff, but it should not create a second
long-lived memory system beside the established root.
