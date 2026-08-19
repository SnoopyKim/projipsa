---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-08-19
sources:
  - AGENTS.md
  - https://github.com/SnoopyKim/projipsa/releases/tag/v0.4.0
  - https://docs.x.ai/build/features/skills-plugins-marketplaces
  - README.md
  - CONTRIBUTING.md
  - plugins/projipsa/.claude-plugin/plugin.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/shared/projipsa-init.md
  - plugins/projipsa/shared/compact.md
  - plugins/projipsa/shared/outsource.md
  - plugins/projipsa/codex-skills/projipsa/references/memory-contract.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/codex-skills/projipsa/references/repair-and-upgrade.md
  - plugins/projipsa/codex-skills/projipsa-init/references/initialization.md
  - plugins/projipsa/codex-skills/compact/scripts/audit_compaction.py
  - plugins/projipsa/codex-skills/outsource/references/verification.md
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - scripts/validate_package.py
  - tests/test_compact_audit.py
  - tests/test_package_contract.py
  - tests/test_validate_memory.py
  - wiki/decisions/2026-08-17-explicit-memory-compaction.md
  - wiki/decisions/2026-08-13-rules-must-earn-their-place.md
  - wiki/decisions/2026-08-12-parallel-safe-memory-tree.md
  - wiki/decisions/2026-08-11-qa-oriented-verification-claims.md
  - wiki/decisions/2026-08-02-host-adapter-separation.md
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.host-adapter-separation.2026-08-02
  - decision.qa-oriented-verification-claims.2026-08-11
  - decision.parallel-safe-memory-tree.2026-08-12
  - decision.rules-must-earn-their-place.2026-08-13
  - decision.explicit-memory-compaction.2026-08-17
  - question.open-questions
---

# Current State

## Summary

0.5.0 is implemented in the local working tree but is not committed or
released. It separates first adoption, routine repair, and explicit compaction;
adds a fourth `compact` Skill whose default is read-only Audit; changes future
ingestion so temporary or reproducible captures do not automatically
accumulate under `raw/`; and supports Codex, Claude Code, and Grok Build through
two adapter dialects. See [the compaction
decision](../decisions/2026-08-17-explicit-memory-compaction.md).

0.4.0 remains the latest published release. Claude Code reports its installed
copy as 0.4.0; the Codex development marketplace exposes the local 0.5.0
working tree, and Grok Build's Claude compatibility discovers the same local
four-Skill surface. Its release history and validation evidence are in [the
August chronology](../../logs/2026-08.md).

Projipsa exists so project understanding survives session boundaries and
substantial work can be delegated against that durable state. Cross-host
support is a distribution constraint, not the purpose. See [the
overview](overview.md).

## Confirmed Current

- The 0.5.0 source package exposes four public Skills: `projipsa`,
  `projipsa-init`, `compact`, and `outsource`.
- `projipsa` may load implicitly for read-only context work and owns ongoing
  Query, Ingest, Update, Integrate, Lint, Repair, and Snapshot. Writes still
  require authorized project-memory scope.
- `projipsa-init` is explicit-only and first-adoption-only. It creates a memory
  root, adopts existing general documentation, or resumes an interrupted first
  adoption. An existing `projipsa_adoption: true` marker routes Repair and
  Upgrade back to `projipsa`.
- `compact` is explicit-only. Its default Audit reports size, exact image
  duplicate groups, local references, Git baseline and tracking, and
  conservative semantic-review groups without modifying files. Apply requires
  an exact path plan and separate explicit approval; a modified tracked or
  untracked artifact also needs a recovery path or acknowledged unrecoverable
  approval.
- Compact never treats age, size, filename, missing references, or hash equality
  as sufficient deletion authority. It protects the only evidence for an
  active claim and reports working-tree savings separately from Git history.
- Memory is modeled by Evidence, Events, Synthesis, and rebuildable Views.
  These are roles rather than mandatory folders; each project's
  `docs/AGENTS.md` or equivalent is the initial project profile.
- Future Ingest links stable project or external artifacts, retains durable
  unique evidence, follows project policy for replaceable current visuals, and
  omits temporary or reproducible captures. Normal maintenance never
  overwrites or deletes retained raw evidence.
- Existing 0.3.x and 0.4.x adopters upgrade only through authorized Repair.
  Stable IDs, useful optional pages, customized rules, and chronology remain;
  plugin installation alone never rewrites adopter memory.
- Parallel work gives shared synthesis pages one writer, lets each writer own
  its own chronology, and runs Integrate only on the branch that contains the
  merged result. Current state is replaced rather than appended, using whether
  a line changes the next session as its eviction test. See [the parallel-safe
  decision](../decisions/2026-08-12-parallel-safe-memory-tree.md).
- The minimum memory contract requires `AGENTS.md`, `index.md`,
  `wiki/project/current-state.md`, an adoption decision, chronology, and the
  `id`, `updated`, and `sources` frontmatter keys. Optional pages and fields
  stay valid when present. Rules are retained only when breaking them would
  mislead or materially slow a future reader. See [the rule
  criterion](../decisions/2026-08-13-rules-must-earn-their-place.md).
- Outsource verification starts from the service user, artifact consumer,
  operator, or QA perspective and traces the actual user or data path. It keeps
  execution, technical verification, and Maker acceptance independent. See
  [the verification
  decision](../decisions/2026-08-11-qa-oriented-verification-claims.md).
- Only `plugins/projipsa/` ships. Codex uses its isolated thin adapter; Claude
  Code and Grok Build use the Claude-compatible adapter over the same shared
  workflow per Skill. The package contains no default `skills/` directory. See
  [the host adapter
  decision](../decisions/2026-08-02-host-adapter-separation.md).
- `scripts/validate_package.py` checks the shipped package, README, and the two
  development marketplace manifests. `validate_memory.py` separately owns an
  adopter's memory root. The Compact analyzer is inventory-only and does not
  implement deletion.

## In Progress

- 0.5.0 changes are present only in the local working tree. Commit,
  push, tag, release, installed-host refresh, and public marketplace listing
  are separate operations and have not been performed.

## Explicitly Not Current

- No adopter memory has been migrated, repaired, or compacted by this
  implementation.
- No public marketplace listing exists. Development installs still use this
  source checkout.
- This repository has no `raw/` or replaceable visual asset tree because its
  evidence already has stable versioned paths.
- No `wiki/deliveries/` tree exists because no delegated engagement is active.
- Claude Code still reports its installed copy as 0.4.0. Codex and Grok Build
  can see the 0.5.0 development tree, but that is not release publication or a
  pinned 0.5.0 install.

## Active Defaults

- `docs/` is this public repository's memory root. Prefer a pull request,
  commit, CI run, or repository path over copying an artifact into memory.
- Read current state before chronology. Open retained evidence only when a
  claim needs verification or provenance.
- A docs-only task does not change implementation. Automatic Skill loading is
  neither write authority, delegation, acceptance, nor deletion approval.
- Pages created from a template start below `confirmed`. Raise one to
  `confirmed` only in the edit that lists its primary evidence.
- The installed copy is version-pinned. Working-tree changes reach a host only
  after a version bump and a separately authorized install refresh.

## Validation

Latest local working-tree evidence; released 0.4.0 evidence stays in [the
chronology](../../logs/2026-08.md).

- `python3 scripts/validate_package.py` passes.
- `python3 -m unittest discover -s tests` passes: 58 tests on the local Python
  3.12 runtime, including six Compact analyzer tests and the Grok adapter-root
  contract test.
- `python3 plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  docs` passes after current-state restructuring.
- `claude plugin validate ./plugins/projipsa --strict` passes.
- `grok plugin validate ./plugins/projipsa` passes, and filtered runtime
  inspection exposes all four Skills from the Claude-compatible adapter.
- `git diff --check` passes.
- The skill-creator quick validator was attempted but could not run because its
  separate runtime dependency `PyYAML` is absent. The repository package
  validator independently checks both Compact adapters, loading policies,
  metadata, links, resources, and contract guardrails.
- Python 3.9 and 3.13 CI have not run against 0.5.0 because nothing has been
  committed or pushed.

## Next Work

- Publish the authorized 0.5.0 release, run supported-version CI, and refresh
  the three host surfaces without creating a duplicate native Grok install.
- Fix the three reproduced `validate_memory.py` gaps recorded in [open
  questions](../questions/open-questions.md).
- Decide whether the narrowed Outsource trigger fires appropriately and whether
  Skill triggering and semantic workflow behavior need a model-backed
  evaluation harness.
