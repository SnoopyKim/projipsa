---
name: projipsa-init
description: Initialize Projipsa in an existing project and make its current documentation usable as source-backed project memory. Use when asked to init, initialize, set up, adopt, onboard, migrate, or repair a project's project-memory structure, especially when existing docs, handoffs, decision logs, research notes, or status files must be preserved and reorganized. Do not use for routine updates after initialization; use projipsa instead.
---

# Projipsa Init

Onboard an existing project into Projipsa. Create one durable, repo-local
memory system around the project's real documentation and conventions. Treat
initialization as a docs-only operation unless the user explicitly expands the
scope.

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

Read `references/initialization.md` for the detailed inventory, mapping, and
validation workflow. Read the sibling canonical resources before writing:

- `../projipsa/references/memory-contract.md`
- `../projipsa/references/page-types.md`
- `../projipsa/assets/templates/`

Resolve these paths relative to this skill directory.

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
page families only when the inventory justifies them. Do not create empty
folders merely to match an example.

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

Append the monthly log and make `index.md` the clear reading entry point.

## Validate and hand off

1. Run the sibling `../projipsa/scripts/validate_memory.py` against the memory
   root.
2. Check that maintained pages are reachable from the index or related pages.
3. Inspect the diff for unintended non-documentation changes.
4. Confirm raw sources were preserved and old full copies were not left as a
   second source of truth.
5. Report the selected root, files created or moved, preserved sources,
   validation, unresolved questions, and the next useful Projipsa operation.

After successful initialization, use `projipsa` for ongoing Query, Ingest,
Update, Lint, and Snapshot work.
