---
id: decision.explicit-memory-compaction.2026-08-17
type: decision
status: active
confidence: confirmed
updated: 2026-08-17
sources:
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/shared/projipsa-init.md
  - plugins/projipsa/shared/compact.md
  - plugins/projipsa/codex-skills/compact/scripts/audit_compaction.py
  - plugins/projipsa/codex-skills/projipsa/references/repair-and-upgrade.md
  - tests/test_compact_audit.py
related:
  - project.current-state
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.rules-must-earn-their-place.2026-08-13
supersedes: []
superseded_by: []
---

# Separate first adoption, routine repair, and explicit compaction

## Decision

Projipsa 0.5.0 separates three authority and frequency boundaries:

- `projipsa-init` creates a memory root or adopts existing general
  documentation. Once the adoption marker exists, Init stops.
- `projipsa` owns ongoing Query, Ingest, Update, Integrate, Lint, Repair, and
  Snapshot work, including preservation-first contract upgrades.
- `compact` is a fourth public Skill for explicit, infrequent compaction. Its
  default operation is read-only Audit. Apply requires an exact path plan and
  separate explicit approval.

The memory model is expressed as Evidence, Events, Synthesis, and Views. These
are roles, not a mandatory replacement folder schema. Each adopting project's
`docs/AGENTS.md` or equivalent is the first project profile: it maps local paths
and may define a replaceable visual-asset policy.

Normal memory maintenance never overwrites or deletes retained raw Evidence.
Compact may remove a whole artifact only after checking active evidence,
references, recoverability, and exact user approval. It does not rewrite a
surviving original or repository history.

## Context

Routine restructuring is part of keeping synthesis current, so a separate
restructure Skill would split one everyday responsibility across two triggers.
Init had the opposite problem: it accumulated first adoption, migration,
ongoing audit, repair, and version upgrade despite being an explicit onboarding
workflow.

Binary evidence has a different risk and cost profile from Markdown. Old
screenshots and edited variants can dominate working-tree size, while the
duplicates that matter are often semantic rather than byte-identical. File age,
size, naming, or hash equality cannot establish that a particular image is safe
to remove or choose which copy should survive.

## Alternatives Considered

- Keep repair and compaction inside Init.
- Add a general Restructure Skill for both routine synthesis and binary cleanup.
- Automatically deduplicate exact image hashes during Update.
- Introduce a mandatory project-profile YAML schema before supporting Compact.
- Keep raw sources permanently immutable, including a ban on whole-artifact
  removal under any workflow.

## Reasoning

- First adoption has a clear completion marker. Repair has no such terminal
  point and belongs beside the ongoing operations that detect drift.
- Compact alone crosses the deletion boundary and needs a trigger that cannot
  load implicitly. Keeping its Audit and Apply phases together makes the
  approval target inspectable without granting Apply by invoking the Skill.
- Exact hashes are useful inventory but weak deletion policy. Semantic groups
  require visual review, and every candidate requires an active-claim evidence
  check.
- Existing projects already have `docs/AGENTS.md`; making that file the profile
  adds no mandatory artifact and lets local conventions precede plugin
  defaults.
- Whole-artifact removal can be safe when the tracked file's current bytes are
  recoverable from a recorded Git baseline. Modified tracked and untracked
  files need a separate recovery path or acknowledged unrecoverable approval.

## Consequences

- The package exposes four Skills. `compact` and `projipsa-init` are
  explicit-only on both hosts.
- A standard-library analyzer reports bytes, exact image duplicate groups,
  references, Git baseline and tracking, and conservative semantic-review
  groups without changing files.
- Future Ingest classifies sources before copying: link stable artifacts,
  retain durable unique evidence, manage replaceable current visuals by project
  policy, and omit temporary or reproducible captures.
- Existing adopters are never rewritten by a plugin update. They receive these
  rules only through an authorized Projipsa Repair or Compact Apply.
- Compact reports working-tree savings separately from Git-history size.
