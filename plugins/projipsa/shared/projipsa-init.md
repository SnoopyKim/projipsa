# Projipsa Init Workflow

Onboard an existing project into Projipsa. Create one durable, repo-local
memory system around the project's real documentation and conventions. Treat
initialization as a docs-only operation unless the user explicitly expands the
scope.

This is an explicit, infrequent workflow. Do not load or run it merely because
project memory would be useful. Start only when the user invokes
`$projipsa:projipsa-init` in Codex, `/projipsa:projipsa-init` in Claude Code or
Grok Build, or clearly asks to initialize Projipsa or adopt existing general
documentation into it.

Each host adapter enforces that boundary mechanically using its own invocation
policy. Keep the Codex and Claude-compatible adapter policies aligned.

## Establish the boundary

1. Read repository instructions and the top-level project overview.
2. Inspect version-control status and preserve unrelated user work.
3. Inventory existing documentation before creating new files.
4. Choose `docs/` unless the project already has a durable equivalent.
5. Never create a parallel `pm-memory/`, `project-memory/`, or second `docs/`
   tree beside an established documentation root.
6. If the target root is materially ambiguous or moving it would break an
   external contract, stop and ask for that decision.

## Choose the initialization path

- **New memory**: the project has little or no durable documentation. Create
  the minimum useful core from verified repository context.
- **Adoption migration**: the project has useful but flat or mixed
  documentation. Reclassify it as maintained synthesis, raw source, decision,
  question, or chronology and preserve its meaning.

Initialization is idempotent while first adoption is incomplete: resume the
inventory and fill only the missing adoption pieces. Once an adoption decision
with `projipsa_adoption: true` exists, do not modify the adopted memory in Init.
Route structural repair or contract upgrade to `$projipsa:projipsa` in Codex or
`/projipsa:projipsa` in Claude Code, and route size or binary cleanup to the
explicit Compact workflow.

An installed plugin update never rewrites an adopting project's memory.

Read
[the initialization workflow](../codex-skills/projipsa-init/references/initialization.md)
for the
detailed inventory, mapping, and validation workflow. Read the sibling
canonical resources before writing:

- [memory contract](../codex-skills/projipsa/references/memory-contract.md)
- [page types](../codex-skills/projipsa/references/page-types.md)
- [templates](../codex-skills/projipsa/assets/templates/)

## Create the minimum useful core

Make the initialized project immediately readable:

```text
docs/
  AGENTS.md
  index.md
  wiki/project/current-state.md
  wiki/decisions/YYYY-MM-DD-projipsa-adoption.md
  logs/YYYY-MM.md
```

Add `wiki/project/overview.md` and `wiki/questions/open-questions.md` when the
project has something verified to put in them.

Create `raw/YYYY-MM/` content when real source material exists. Add optional
page families only when the inventory justifies them. In particular, do not
create `wiki/deliveries/` until a substantial delegated engagement needs
durable state. Do not create empty folders merely to match an example.

Monthly chronology is the default. When the inventory shows work already
running in parallel branches or worktrees, choose a per-writer log unit at
initialization instead, and record the choice in the adoption decision. The
[page types](../codex-skills/projipsa/references/page-types.md) reference lists
the supported units.

Replace all template placeholders with verified project facts. When something
is unknown, record it as an explicit open question rather than a TODO or an
invented answer.

## Preserve existing truth

- Move maintained synthesis rather than duplicating it.
- Preserve source artifacts without rewriting them.
- Split decision logs into stable decision pages when useful.
- Split mixed handoff files into current state, questions, risks, decisions,
  milestones, and chronology as applicable.
- Leave a short moved stub only for an old path that people or agents are
  likely to open.
- Keep current state about what is true now; keep chronology in the logs.
- Do not rewrite project reality to fit the template.

## Record adoption

Create an adoption decision that states:

- the selected memory root;
- the canonical raw/wiki/log relationship;
- any migrated or retained legacy paths;
- justified optional page families;
- known gaps and follow-up work.

For a new decision, use the canonical ID
`decision.projipsa-adoption.<yyyy-mm-dd>`, a filename ending in
`projipsa-adoption.md`, and `projipsa_adoption: true` frontmatter. If an
equivalent decision already exists, preserve its stable ID and path, add the
explicit adoption marker, and do not create a second decision.

Append the chronology log and make `index.md` the clear reading entry point.

## Make the memory root discoverable by every host

An initialized memory root is worthless if the next agent never opens it, and
each host discovers project instructions differently. Codex reads `AGENTS.md`.
Claude Code reads `CLAUDE.md` and does not read `AGENTS.md` at all. Grok Build
reads `AGENTS.md` and also supports Claude Code instruction compatibility. So
initialization maintains one marked pointer block in the project's root
instruction files:

1. Ensure the project root has `AGENTS.md` carrying the pointer block from
   [the root pointer template](../codex-skills/projipsa/assets/templates/root-pointer.md).
2. Ensure the project root has `CLAUDE.md`. When none exists, create it as an
   import of `AGENTS.md` so every host reads one maintained file. When one
   already exists, add the same pointer block instead of injecting an import
   that would duplicate curated instructions.
3. Delimit the block with `<!-- projipsa:memory-pointer -->` and
   `<!-- /projipsa:memory-pointer -->`. On a later run, replace that block in
   place; never append a second copy.
4. Keep the block short: the selected memory root, the reading entry point, the
   layer rules, and where the full rules live.
5. Preserve every surrounding line the Maker wrote.

Root instruction files are documentation, so maintaining this block stays inside
the docs-only boundary. Report the two paths explicitly anyway, because they sit
outside the memory root the Maker asked you to create.

## Validate and hand off

1. Run the sibling
   [memory validator](../codex-skills/projipsa/scripts/validate_memory.py) against
   the memory root.
2. Check that maintained pages are reachable from the index or related pages.
3. Inspect the diff for unintended non-documentation changes.
4. Confirm raw sources were preserved and old full copies were not left as a
   second source of truth.
5. Confirm root `AGENTS.md` carries exactly one pointer block naming the
   selected memory root, and root `CLAUDE.md` either imports `AGENTS.md` or
   carries the same single block. The memory validator checks both.
6. Report the selected root, files created or moved, the root instruction files
   touched, preserved sources, validation, unresolved questions, and the next
   useful Projipsa operation.

After successful initialization, use `$projipsa:projipsa` in Codex or
`/projipsa:projipsa` in Claude Code or Grok Build for ongoing Query, Ingest,
Update, Integrate, Lint, Repair, and Snapshot work.
