---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-09-23
sources:
  - README.md
  - CONTRIBUTING.md
  - plugins/projipsa/.claude-plugin/plugin.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/codex-skills/projipsa/references/repair-and-upgrade.md
  - plugins/projipsa/codex-skills/projipsa/assets/templates/decision.md
  - plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py
  - plugins/projipsa/codex-skills/projipsa/references/context-and-evidence.md
  - tests/test_memory_context.py
  - scripts/validate_package.py
  - tests/test_validate_memory.py
  - research/2026-09-23-github-memory-snapshot.json
  - logs/2026-08.md
  - logs/2026-09.md
related:
  - project.overview
  - decision.project-memory-focus.2026-09-23
  - decision.evidence-aware-context.2026-09-23
  - area.project-memory-references
  - area.project-knowledge-views
  - question.open-questions
---

# Current State

## Summary

The working tree prepares **0.6.0, unreleased**, with a project-memory-only
scope. It removes Outsource and keeps `projipsa`, `projipsa-init`, and `compact`.
The latest recorded published release is 0.5.0. No new release or installed-host
refresh has been performed yet. The Maker has authorized including the new
context/evidence helper and publishing 0.6.0 in this task.

The purpose is to carry project understanding across sessions: current facts,
decision rationale, evidence, corrections, and next work. See the
[memory-focus decision](../decisions/2026-09-23-project-memory-focus.md).

## Confirmed current

- Both host adapter trees and package metadata expose three Skills; Grok uses
  the Claude-compatible adapter. Only `plugins/projipsa/` ships.
- The memory workflow now emphasizes relevant decisions and prior failures,
  selective reading, reconciliation of new evidence, current verification of
  volatile facts, and observed outcomes with revisit conditions.
- The bundled `memory_context.py` provides explicit relations and reverse
  dependencies, bounded task briefings, evidence-change candidates, and Mermaid
  views. Only scoped `checkpoint --page` writes optional review state. See the
  [implementation decision](../decisions/2026-09-23-evidence-aware-context.md).
- Existing authorized project-memory scope can cover routine post-work updates.
  Implicit lookup stays read-only; installation grants no new write scope.
- Existing adopter delivery pages remain valid records. The plugin no longer
  ships a delivery template or manages an execution/acceptance lifecycle.
- Evidence, append-only Events, maintained Synthesis, and rebuildable Views
  remain the memory roles. Keep shared synthesis to one writer and integrate
  from merged work.
- [September research](../areas/project-memory-references.md) records ten
  candidates, nine focused implementation reviews, and 21 pinned core source
  references. GitHub totals and dated attention signals are separate; exact
  September star-growth totals were unavailable.
  [The knowledge-view addendum](../areas/project-knowledge-views.md) covers the
  two user-supplied repositories and a Wiki-format compatibility probe.

## In progress

- This is a local source change, not a published or installed release.
- Model-backed evaluation of recall, freshness, and post-work updates remains
  unperformed. Structural checks do not establish improved agent behavior.

## Active defaults

- `docs/` is this public repository's memory root. Read current state before
  chronology; follow evidence when needed.
- Link stable artifacts. The research API snapshot is retained evidence under
  `docs/research/`; external code is referenced at immutable commits.
- Keep current state concise and move historical detail to the existing log,
  decision, milestone, or area page.
- No background capture service, vector index, graph database, automated
  reflection, or runtime enforcement has been introduced.
- The current Codex CLI reports `projipsa@personal` 0.3.0 from a separate local
  plugin source, not this checkout. Publishing this repository will not update
  that installation. Keep source publication separate from changing its source.

## Validation

Validation for this change is recorded in [September chronology](../../logs/2026-09.md).
The August release and installation evidence remains in
[August chronology](../../logs/2026-08.md).

## Next work

- Run the multi-session scenarios in the research report before adding memory
  infrastructure or claiming a behavioral improvement.
- Fix the three previously reproduced memory-validator gaps in
  [open questions](../questions/open-questions.md).
- Finish the authorized 0.6.0 publication and record the actual release result.
