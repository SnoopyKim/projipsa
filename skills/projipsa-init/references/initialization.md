# Initialization

## Contents

1. Preflight
2. Inventory
3. Root selection
4. Mapping
5. Core creation
6. Migration
7. Repair and idempotency
8. Validation

## 1. Preflight

Before writing:

1. Read root and nested `AGENTS.md`, `CLAUDE.md`, README files, and established
   documentation instructions.
2. Inspect version-control status and note existing changes.
3. Find documentation directories and high-value context files.
4. Search for references to old documentation paths that a move may affect.
5. Separate the initialization surface from project implementation.

Do not initialize from a README summary alone when the repository contains
better evidence in code, configuration, tests, or existing docs.

## 2. Inventory

Record each relevant file's path, purpose, approximate freshness, and role:

```md
| Existing path | Current role | Destination | Action |
| --- | --- | --- | --- |
| docs/brief.md | project overview | docs/wiki/project/overview.md | move and refine |
| docs/decision-log.md | many decisions | docs/wiki/decisions/*.md | split |
| docs/handoff.md | state and chronology | current-state plus log | split |
| notes/research.md | source material | docs/raw/YYYY-MM/ | preserve and summarize |
```

Classify each item as:

- maintained current synthesis;
- raw or imported source;
- append-only chronology;
- decision;
- open question;
- assumption;
- risk;
- procedure;
- external dependency;
- area or workstream;
- milestone or snapshot;
- stale, superseded, or archived content.

Inventory is analysis, not permission to rewrite every file.

## 3. Root selection

Prefer `docs/` when no equivalent exists. Reuse an established equivalent when
it is durable, agent-readable, versioned with the project where appropriate,
and already treated as canonical.

Do not choose:

- a generated build directory;
- an installed plugin cache;
- a private global memory folder as the only project truth;
- a parallel root that competes with existing docs.

Record a non-default root in the project's memory instructions and index.

## 4. Mapping

Map to the universal core first:

- project or initiative brief -> `wiki/project/overview.md`;
- current status or handoff summary -> `wiki/project/current-state.md`;
- decision log -> individual `wiki/decisions/` pages;
- unresolved unknowns -> `wiki/questions/`;
- meetings, research, interviews, imported docs, and conversation outputs ->
  `raw/YYYY-MM/` plus affected maintained pages;
- chronology -> `logs/YYYY-MM.md`.

Add optional families only when the inventory justifies them:

- major workstream or responsibility -> `wiki/areas/`;
- unverified planning claim -> `wiki/assumptions/`;
- active threat needing mitigation -> `wiki/risks/`;
- repeatable operating steps -> `wiki/procedures/`;
- outside party, tool, system, contract, source, API, or dependency ->
  `wiki/external/`;
- launch, checkpoint, review, handoff, or pause -> `wiki/milestones/`.

## 5. Core creation

Use the templates in `../projipsa/assets/templates/` relative to the init
skill directory.

At minimum:

1. Make `index.md` the reading entry point.
2. Add project-specific memory rules in `AGENTS.md`.
3. Create verified project overview and current state pages.
4. Record the Projipsa adoption decision.
5. Capture real unknowns in open questions.
6. Start the current monthly log.

Do not leave generic sample text, placeholder dates, placeholder IDs, or TODOs
in the initialized project.

## 6. Migration

When existing docs need reorganization:

1. Preserve source artifacts before synthesizing them.
2. Move polished synthesis to its canonical maintained page.
3. Split mixed documents only where page responsibilities are meaningfully
   different.
4. Use short moved stubs only for important legacy paths.
5. Update internal links and known external path references.
6. Keep raw and historical content unchanged when its old wording is evidence.
7. Review the docs-only diff before claiming migration success.

Avoid two full copies of the same maintained truth.

## 7. Repair and idempotency

When a memory root already exists:

- keep its stable IDs and working paths;
- fill missing core responsibilities rather than replacing the tree;
- repair navigation and frontmatter in place;
- do not recreate the adoption decision if an equivalent decision exists;
- do not append duplicate init log entries;
- treat user customizations as intentional unless evidence shows otherwise;
- report divergence from the default instead of normalizing it automatically.

## 8. Validation

Run:

```bash
python3 <plugin-root>/skills/projipsa/scripts/validate_memory.py <memory-root>
```

Then review what deterministic checks cannot prove:

- current-state accuracy against project reality;
- raw-source preservation;
- claim provenance quality;
- whether optional page families are justified;
- whether old paths need stubs;
- whether the diff stayed docs-only;
- whether another source of truth still competes with the initialized root.

Initialization succeeds only when a future agent can enter through the index,
understand current state, distinguish facts from unknowns, and locate the
evidence needed to continue.
