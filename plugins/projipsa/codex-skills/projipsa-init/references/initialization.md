# Initialization

## Contents

1. Preflight
2. Inventory
3. Root selection
4. Mapping
5. Core creation
6. Migration
7. Upgrade, repair, and idempotency
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
- chronology -> `logs/YYYY-MM.md`, or the finer unit this project needs.

Add optional families only when the inventory justifies them:

- major workstream or responsibility -> `wiki/areas/`;
- unverified planning claim -> `wiki/assumptions/`;
- active threat needing mitigation -> `wiki/risks/`;
- repeatable operating steps -> `wiki/procedures/`;
- outside party, tool, system, contract, source, API, or dependency ->
  `wiki/external/`;
- launch, checkpoint, review, handoff, or pause -> `wiki/milestones/`.

## 5. Core creation

Use the templates in `../../projipsa/assets/templates/` relative to this
reference file.

At minimum:

1. Make `index.md` the reading entry point.
2. Add project-specific memory rules in `<memory-root>/AGENTS.md`.
3. Create a verified current state page.
4. Record the Projipsa adoption decision.
5. Start the current chronology log.

Add an overview page when the project's purpose and scope are worth stating
apart from its current state, and an open-questions page when real unknowns
exist. Neither is required, because a page created before the project has
anything to put in it fills up with template text instead.
6. Maintain the pointer block from `root-pointer.md` in the project root's
   `AGENTS.md` and `CLAUDE.md`. These are the project root's instruction files,
   not the memory root's, and they are how Codex and Claude Code respectively
   discover the memory root at all.

Pages created from a template start below `confirmed` — `inferred` for most
types, `assumed` for `assumption`, `question`, `risk`, and `delivery`. Raise a
page to `confirmed` only in the same edit that lists its primary evidence in
`sources`.

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

## 7. Upgrade, repair, and idempotency

When a memory root already exists:

- keep its stable IDs and working paths;
- fill missing core responsibilities rather than replacing the tree;
- repair navigation and frontmatter in place;
- preserve an equivalent adoption decision's stable ID and path, add
  `projipsa_adoption: true`, and do not create a second page;
- do not append duplicate init log entries;
- keep exactly one pointer block per root instruction file, replacing its
  contents in place when the memory root moves or the layer rules change;
- create a root `CLAUDE.md` on repair when Claude Code would otherwise never
  see the memory root;
- treat user customizations as intentional unless evidence shows otherwise;
- report divergence from the default instead of normalizing it automatically.

### Upgrade an existing Projipsa root

Treat an upgrade as a capability audit, not as a schema rewrite. Project memory
does not carry a reliable installed-plugin version, and its shape may include
intentional customizations, so compare the existing behavior with the current
contract instead of inferring a version from file or field presence.

For the 0.3.x to 0.4.0 transition:

1. Preserve `wiki/project/overview.md`,
   `wiki/questions/open-questions.md`, and stated `type`, `status`,
   `confidence`, or `related` fields. They became optional, not deprecated.
2. Never bulk-remove fields or pages merely to match the smaller minimum. A
   no-op is a successful upgrade when the existing tree already validates and
   its operating rules are current.
3. Merge the ownership, current-state eviction, and post-merge Integrate rules
   into the project's existing `<memory-root>/AGENTS.md`; do not replace that
   project-specific file wholesale from the latest template.
4. Preserve monthly chronology by default. Switch only when concurrent writers
   make one append target unsafe: choose a cutover date, leave old logs in
   place, start day-and-slug per-writer files, update `index.md`, and record the
   choice in the existing adoption decision or a new focused decision.
5. Do not rename or split historical logs. The 0.4.0 validator now checks every
   Markdown file under `logs/**`; report newly visible broken links,
   placeholders, and empty files as pre-existing migration findings before
   repairing them.
6. Apply current-state eviction claim by claim. Move history only to an
   existing or justified destination, prune a source only with the claim it
   supported, and preserve stable IDs and links.
7. Replace the marked root pointer block only when its discovery path or layer
   rules changed, and preserve every surrounding instruction.
8. Append one upgrade chronology entry only when the run actually changes the
   project memory. Do not add duplicate adoption or initialization entries.

The upgrade does not run when the plugin is installed or refreshed. It requires
an explicit `$projipsa:projipsa-init` or `/projipsa:projipsa-init` migration,
audit, or repair request, preserving the Skill's docs-only and explicit-only
authority boundary.

## 8. Validation

Run:

```bash
python3 <plugin-root>/codex-skills/projipsa/scripts/validate_memory.py <memory-root>
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
