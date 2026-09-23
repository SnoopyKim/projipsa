---
id: decision.evidence-aware-context.2026-09-23
type: decision
status: active
confidence: confirmed
updated: 2026-09-23
sources:
  - plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py
  - plugins/projipsa/codex-skills/projipsa/references/context-and-evidence.md
  - plugins/projipsa/shared/projipsa.md
  - tests/test_memory_context.py
related:
  - decision.project-memory-focus.2026-09-23
  - area.project-knowledge-views
  - project.current-state
---

# Evidence-aware project context in 0.6.0

## Decision

The Maker requested that the relationship, evidence-change, and task-briefing
proposals be implemented and included in the 0.6.0 release. Keep the three-Skill
surface and ship a standard-library Python helper through the existing
Projipsa workflow. Markdown remains canonical.

## Implementation

- `graph` extracts explicit frontmatter relations and ordinary Markdown links,
  provides source provenance, and emits bounded JSON or Mermaid views.
- `brief` selects lexical matches and related records, follows reverse source
  dependencies, and returns bounded excerpts with paths, historical/superseded
  labels, and evidence review state. It does not infer new claims.
- `review` compares page and reachable local-evidence hashes with per-page
  checkpoints. Missing or changed evidence produces candidates, not automatic
  invalidation. URL contents remain externally unchecked.
- `checkpoint --page` is the only write command. It records explicit reviewed
  pages under `.projipsa/evidence-baseline.json` with locking and atomic
  replacement, preserving checkpoints for other pages.

## Reasoning and alternatives

Existing `sources`, `related`, and supersession metadata already carries useful
relationships. Deriving them avoids requiring a graph database, rewritten Wiki
link syntax, external models, or a background service. A source-file change can
be traced through a maintained area page to the decisions that depend on it.

Automatically accepting all current hashes on retrieval would hide unreviewed
changes. Scoped checkpoints instead follow actual evidence review within an
authorized memory update. This optional operational state is not a disposable
View: losing it loses the comparison baseline, not the canonical knowledge.

## Limits and revisit conditions

- Character budgets are not token budgets. JSON metadata is outside the
  Markdown text budget, and omitted records are reported.
- Lexical selection is not semantic recall. Broaden misses and read originals
  before resolving conditions or conflicting claims.
- Local hashes cover whole files, so unrelated edits can produce candidates.
  Line-scoped comparison is a future option if false positives become costly.
- Remote content changes behind an unchanged URL need live host verification.
- Explicit links do not prove that a source entails a claim. No model-backed
  cross-session memory benchmark has been completed.

Tests cover retrieval, direct and indirect source changes, cycles, missing
files, external revision changes, read-only queries, scoped checkpoints,
failed atomic writes, historical records, budgets, and diagram escaping.
