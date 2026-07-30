---
name: projipsa-init
description: Initialize, migrate, audit, or repair Projipsa project memory in an existing project. Use when the user explicitly invokes $projipsa-init or /projipsa:projipsa-init, or explicitly asks to adopt, install, migrate, or repair Projipsa documentation. Treat initialization as docs-only unless the user expands the scope. Do not invoke merely because project memory would be useful.
disable-model-invocation: true
---

# Projipsa Init

Onboard an existing project into Projipsa. Create one durable, repo-local
memory system around the project's real documentation and conventions. Treat
initialization as a docs-only operation unless the user explicitly expands the
scope.

This is an explicit, infrequent workflow. Do not load or run it merely because
project memory would be useful. Start only when the user invokes
`$projipsa-init` in Codex, `/projipsa:projipsa-init` in Claude Code, or clearly
asks to initialize, adopt, migrate, audit, or repair Projipsa memory.

Both hosts enforce that boundary mechanically rather than by prose alone:
`allow_implicit_invocation: false` in `agents/openai.yaml` for Codex, and
`disable-model-invocation: true` in this file's frontmatter for Claude Code.
Keep the two declarations in sync.

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
- **Migration**: the project has useful but flat or mixed documentation.
  Reclassify it as maintained synthesis, raw source, decision, question, or
  chronology and preserve its meaning.
- **Repair**: Projipsa is partly initialized. Reconcile missing files,
  navigation, frontmatter, IDs, and logs without duplicating the tree.

Initialization is idempotent. A second run audits and repairs the existing
structure rather than starting over.

Read [the initialization workflow](references/initialization.md) for the
detailed inventory, mapping, and validation workflow. Read the sibling
canonical resources before writing:

- [memory contract](../projipsa/references/memory-contract.md)
- [page types](../projipsa/references/page-types.md)
- [templates](../projipsa/assets/templates/)

## Create the minimum useful core

Make the initialized project immediately readable:

```text
docs/
  AGENTS.md
  index.md
  wiki/project/overview.md
  wiki/project/current-state.md
  wiki/decisions/YYYY-MM-DD-projipsa-adoption.md
  wiki/questions/open-questions.md
  logs/YYYY-MM.md
```

Create `raw/YYYY-MM/` content when real source material exists. Add optional
page families only when the inventory justifies them. In particular, do not
create `wiki/deliveries/` until a substantial delegated engagement needs
durable state. Do not create empty folders merely to match an example.

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
- Keep current state about what is true now; keep chronology in monthly logs.
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

Append the monthly log and make `index.md` the clear reading entry point.

## Make the memory root discoverable by every host

An initialized memory root is worthless if the next agent never opens it, and
each host discovers project instructions differently. Codex reads `AGENTS.md`.
Claude Code reads `CLAUDE.md` and does not read `AGENTS.md` at all. So
initialization maintains one marked pointer block in the project's root
instruction files:

1. Ensure the project root has `AGENTS.md` carrying the pointer block from
   [the root pointer template](../projipsa/assets/templates/root-pointer.md).
2. Ensure the project root has `CLAUDE.md`. When none exists, create it as an
   import of `AGENTS.md` so both hosts read one maintained file. When one
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
   [memory validator](../projipsa/scripts/validate_memory.py) against
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

After successful initialization, use `$projipsa` for ongoing Query, Ingest,
Update, Lint, and Snapshot work.
