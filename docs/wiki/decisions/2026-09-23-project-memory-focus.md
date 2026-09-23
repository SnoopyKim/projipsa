---
id: decision.project-memory-focus.2026-09-23
type: decision
status: active
confidence: confirmed
updated: 2026-09-23
sources:
  - README.md
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/codex-skills/projipsa/references/repair-and-upgrade.md
  - plugins/projipsa/.codex-plugin/plugin.json
  - scripts/validate_package.py
  - logs/2026-09.md
related:
  - project.overview
  - project.current-state
  - area.project-memory-references
supersedes:
  - decision.qa-oriented-verification-claims.2026-08-11
---

# Concentrate Projipsa on project memory

## Decision

On 2026-09-23 the Maker directed that Outsource be excluded and Projipsa focus
on being the project's memory specialist. The 0.6.0 source package exposes
three Skills: `projipsa`, `projipsa-init`, and `compact`.

The host agent owns execution. Projipsa maintains current understanding,
decision rationale, evidence, history, corrections, and resumable context.
It does not qualify delivery engagements, run interviews or contracts, select
an execution topology, or manage acceptance.

## Context and reasoning

The desired outcome is that a new session can recover a project maintainer's
important context, check it against current evidence, and preserve what it
learns for the next session. The Maker selected this narrower role as a better
fit for the project's purpose and name.

Execution scaffolding is no longer part of the product scope. This decision
does not claim an experiment established that Outsource reduces performance;
no such comparison has been run.

The [September source review](../areas/project-memory-references.md) separates
observed mechanisms from adoption proposals. Its immediate contributions are
small workflow improvements: task-relevant retrieval, reconciliation with
existing claims, checking volatile state, and outcome-aware decision records.
Infrastructure proposals remain unimplemented and unevaluated.

## Consequences

- Remove both Outsource adapters, its shared workflow and references, and the
  delivery-contract template from the shipped package.
- Preserve older adopter delivery pages as valid project records. New handoffs
  may link an existing task artifact or use a milestone snapshot.
- Keep Markdown, retained evidence, and Git-compatible files as canonical
  memory; derived indexes remain optional and rebuildable.
- Preserve the distinction between an implementation report, direct evidence,
  and user acceptance when recording outcomes, without retaining the old
  delivery lifecycle.
- Preserve chronological logs. Historical source references to removed files
  resolve to the 0.5.0 tag rather than losing the original evidence.
- Release status belongs in current state and chronology. A later request
  authorized implementing evidence-aware context and publishing 0.6.0; see the
  [implementation decision](2026-09-23-evidence-aware-context.md).

## Outcome and revisit

Package and structural validation can establish consistency and compatibility,
not improved agent judgment. The next evidence should come from multi-session
recall and update scenarios in the research report. Consider additional
retrieval or capture tooling only after observing concrete failures that the
current host-driven workflow cannot reliably resolve.
