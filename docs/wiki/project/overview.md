---
id: project.overview
type: project
status: active
confidence: confirmed
updated: 2026-09-23
sources:
  - README.md
  - CONTRIBUTING.md
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/memory-contract.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/.codex-plugin/plugin.json
  - wiki/decisions/2026-09-23-project-memory-focus.md
related:
  - project.current-state
  - decision.project-memory-focus.2026-09-23
  - area.project-memory-references
---

# Project Overview

## Purpose

Projipsa is a project memory butler. It helps each new agent session recover
what the project knows, why important choices were made, what the evidence
supports, and what remains uncertain. Work should leave useful understanding
for the next session instead of requiring the Maker to explain it again.

Project knowledge lives in maintained Markdown linked to evidence and
append-only chronology. An agent can inspect and edit it with ordinary tools;
it survives sessions, hosts, and people.

The host agent handles implementation and execution. Projipsa's scope narrowed
on 2026-09-23: Outsource is no longer included. See the
[memory-focus decision](../decisions/2026-09-23-project-memory-focus.md).
Cross-host compatibility remains a distribution constraint, not the purpose.

## Scope

- Three Skills: everyday memory and repair, explicit first adoption, and
  explicit memory compaction.
- Evidence, Events, Synthesis, and rebuildable Views mapped to project paths.
- Current context, decisions and rationale, findings, observed outcomes,
  unresolved questions, and resumable handoff records.
- Task-relevant lookup, reconciliation of new evidence, and verification of
  volatile claims when they affect work.
- Deterministic package and memory validators, with semantic judgment left to
  the host agent.

## Boundaries

No execution orchestration, delivery contracts, acceptance lifecycle, background
session recorder, mandatory database, hosted memory service, or model API.
Installation alone does not authorize project-memory writes. Existing project
instructions may establish ongoing maintenance scope.

Existing optional page families, including pre-0.6.0 delivery records, remain
valid. Upgrades preserve useful knowledge and history.

## Design references

The original memory approach follows an agent-maintained, source-backed wiki.
The [September 2026 source review](../areas/project-memory-references.md) records
further references for selective retrieval, evidence reconciliation, temporal
validity, and feedback. External performance claims were not independently
reproduced; proposed infrastructure is separate from shipped behavior.
