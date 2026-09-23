# Memory Contract

## What a rule must earn

Every rule here costs something on every project that adopts it: a field to
fill, a file to create, a shape to match. Grade one by the damage a future
reader takes when it is broken — six months on, with nobody left who remembers
the work.

| That reader | The rule is |
|---|---|
| reaches a wrong conclusion | an error |
| is slowed or misled, but recovers | a warning |
| is unaffected | not a rule; drop it |

The memory validator carries exactly those two channels, and its `warning:`
lines never change the exit code.

A rule satisfied by an empty value is the clearest case of the third row: it
spends load on every page and changes nothing. Grade a project's own
conventions the same way. A tree that enforces its shape harder than its
substance fills up with pages that match the shape and say nothing, which is
the failure this contract exists to prevent.

## Canonical roles

Projipsa uses four roles with distinct authority:

1. **Evidence** preserves or links the sources needed to verify claims.
2. **Events** preserve append-only chronology without becoming current truth.
3. **Synthesis** holds maintained current understanding, decisions, risks, and
   questions.
4. **Views** provide search, graph, dashboard, index, or generated summaries and
   must be rebuildable from the first three roles.

The default `raw/`, `logs/`, and `wiki/` layout implements the first three
roles, but role is more important than folder name. Record project-specific
mapping and visual-asset policy in `<memory-root>/AGENTS.md`. Do not make a View
the only place where a project fact or decision exists.

Optional `.projipsa/evidence-baseline.json` holds operational review state:
the local hashes last checkpointed for specific pages. It is not a rebuildable
View or primary factual evidence. Preserve it when freshness comparisons must
continue; loss means unknown freshness, never an implicit pass. See
[context and evidence](context-and-evidence.md).

Normal Ingest, Update, and Repair never overwrite or delete retained raw
evidence. The explicit Compact workflow may remove a whole artifact only after
an active-evidence check, an exact path plan, recoverability review, and user
approval. This is a lifecycle exception, not permission to rewrite history.

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
  wiki/project/current-state.md
  wiki/decisions/
  logs/YYYY-MM.md
```

`raw/YYYY-MM/`, `wiki/project/overview.md`, and `wiki/questions/` join it when
the project has real source material, a purpose worth stating apart from its
current state, or genuine unknowns.

Add `areas`, `assumptions`, `risks`, `procedures`, `external`, `milestones`, or
`deliveries` only when the project's real operating model needs them. Do not
create empty families for symmetry.

The dated paths in that tree carry different weight. `raw/YYYY-MM/` is a
convention for finding a source by the month it was captured; the memory
validator never inspects `raw/`, so a project may group sources differently as
long as it does so consistently. The chronology filename is a validated rule,
and it admits month, day, and per-session units. See
[page types](page-types.md) before choosing.

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
A handoff links the existing task artifact or a milestone snapshot, along
with durable decisions, questions, evidence, and the next action. Projipsa
records this state without managing execution, contracts, or acceptance.
Existing adopter `wiki/deliveries/` pages remain valid historical or active
project records; preserve their IDs, evidence, and links during upgrades.

Avoid hard runtime dependencies at first. If Projipsa is unavailable, another
agent may preserve a compact handoff, but it should not create a second
long-lived memory system beside the established root.
