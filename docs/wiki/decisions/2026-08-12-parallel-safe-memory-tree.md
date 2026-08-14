---
id: decision.parallel-safe-memory-tree.2026-08-12
type: decision
status: active
confidence: confirmed
updated: 2026-08-13
sources:
  - https://github.com/SnoopyKim/projipsa/issues/9
  - https://github.com/SnoopyKim/projipsa/issues/10
  - https://github.com/SnoopyKim/projipsa/issues/11
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/codex-skills/projipsa/references/page-types.md
  - plugins/projipsa/codex-skills/projipsa/references/memory-contract.md
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - tests/test_validate_memory.py
related:
  - project.current-state
  - project.overview
  - decision.projipsa-adoption.2026-07-31
supersedes: []
superseded_by: []
---

# Make the memory tree survive parallel work

## Decision

The memory contract now states who writes a maintained page, how finely
chronology is split, and that current state is replaced rather than appended.

- **Write ownership.** `index.md`, `wiki/project/current-state.md`, and
  `wiki/questions/open-questions.md` are single-owner integration pages,
  updated by the integrating branch after merge. A delivery page belongs to the
  branch executing that engagement, a decision or risk page to the branch that
  created it, and a chronology entry to a log file its writer alone appends. A
  parallel writer records what it owns and reports that the integration update
  is still outstanding.
- **Chronology granularity.** Monthly stays the default. Day
  (`logs/2026-08-12.md`) and per-writer (`logs/2026-08/2026-08-12-<slug>.md`)
  units are first-class, and the memory validator accepts all three, nested or
  flat. Every Markdown file under `logs/**` is now content-checked.
- **Current-state eviction.** An item leaves when it stops changing what the
  next session does — a lower bar than becoming false, and the one that reaches
  the standing true facts that make this page grow. It goes to chronology, a
  delivery, a decision, a milestone, or an area page, and at most a link stays.
  `sources` lists the evidence for the claims the page makes now, so an entry
  leaves with its claim. The validator prints non-blocking `warning:` lines
  when current state grows past a readable briefing or loses its sections.
- **The post-merge write is an operation.** Integrate is the fifth operation of
  the `projipsa` Skill, not a fourth Skill. It reads the chronology dated after
  current state and writes the single-owner pages once from the merged result. A
  request to finish routes to Update or Integrate without asking, and the
  validator warns while chronology is dated later than current state.

## Context

An adopting project running eight concurrent worktrees reported three issues.
`current-state.md` conflicted in six of six re-merged merge commits and the
monthly log in four of six, because both are written by every branch on the
same lines: a single `updated:` field, a tail-appended `sources` list, a
wholesale-rewritten summary, and an end-of-file append. Its `current-state.md`
had reached 20,428 characters, 59% of it a `Completed` list duplicating log
entries almost one to one, against a 2,097-character overview.

Projipsa already stated the correct rule for code in
`outsource/references/execution-strategies.md` — assign exclusive write
ownership before parallel work, and give integration points one owner — but
never applied it to its own memory tree. The Update operation told every
session to write current state, the monthly log, and `sources` frontmatter,
with no statement of where that write belongs when work is distributed.

Granularity was hard-coded to one file per month across nine prose sites and
the validator, so a flat `logs/2026-08-12.md` was a validation error. A nested
`logs/2026-08/*.md` passed only because `logs_root.glob("*.md")` was
non-recursive: the escape hatch worked by making those files invisible to
frontmatter, link, and placeholder checking.

## Alternatives Considered

- Leave ownership to each adopting project's own conventions.
- Switch the default chronology unit to per-session for every project.
- Reject nested chronology outright instead of validating it.
- Make current-state length a validation error rather than a warning.
- Add a `Completed` section to the current-state template so history has a home
  on the page.
- Ship a fourth Skill for the wrap-up step, invocable on its own.
- Write the shared pages automatically from a merge hook or a CI job.
- Have each parallel writer leave a `pending` marker that the integrator clears.

## Reasoning

- The rule that fixes this already exists for code. Not stating it for memory
  was the defect; the specific page layout is secondary and remains the
  project's choice.
- A shared append target is a conflict target regardless of unit. Day
  granularity does not help two worktrees that finish on the same day, so the
  unit that removes the collision is one file per writer.
- Monthly stays the default because most projects have one writer at a time and
  a single readable file per month is easier to follow than scattered ones.
- A validator that cannot see a file cannot check it. Widening the accepted
  name without walking `logs/**` would have kept the hole open.
- Only the project knows which of its sentences are still true, so page length
  and missing sections are drift signals to report, not structural errors. A
  warning channel keeps the script pass/fail on structure while still naming
  the drift.
- A `Completed` section on the page would legitimize the duplication instead of
  removing it; chronology already answers what happened.
- A Skill is separated by authority boundary, not by stage. `projipsa-init`
  writes where no memory exists and `outsource` carries delegation authority,
  but Integrate writes the pages Update already writes, under the same
  authorization. A fourth Skill would also collide with `projipsa`'s own
  description, which already claims post-work updates and handoff snapshots, so
  the host would route between two overlapping candidates.
- Nothing Projipsa ships executes except the validator, and no agent is running
  when a pull request merges. So detection belongs in the validator and the
  write stays an authorized operation; a hook or CI job that wrote current state
  would perform the one judgment the memory contract reserves for the Maker.
- A `pending` marker would have to be cleared, and clearing it means editing a
  log entry, which chronology's append-only rule forbids. Comparing the latest
  chronology date against `updated:` needs no new convention, edits nothing, and
  clears itself when Integrate writes the page.

## Consequences

- `validate_memory.py` accepts month, day, and per-writer chronology names,
  walks `logs/**` recursively, content-checks every log file, accepts an
  `index.md` link to either a log file or the directory holding it, and prints
  warnings that never change the exit code.
- The Update operation carries an ownership table and an eviction table; Lint
  gains current-state accumulation and stale `sources` entries as findings.
- The generated `docs/AGENTS.md` template tells every adopting project both
  rules, so a project inherits them without reading the reference.
- Existing monthly trees keep validating unchanged, so the change reaches
  adopters without migration.
- The `projipsa` Skill gains an Integrate operation and wrap-up routing, and
  Outsource reports the outstanding integration at engagement close rather than
  writing shared pages from a delivery branch. No new Skill, manifest entry, or
  package surface.
- The outstanding-integration warning is day-granular, so a merge landing the
  same day as an integration is invisible to it. Parsing entry headings for a
  finer signal is possible later; until then the reporting rule in Update
  carries that case.
- The first eviction rule keyed on an item being current, which never reached a
  fact that stays true and simply stops steering the work. That is most of what
  accumulates, so the page grew anyway across two updates until the predicate
  was corrected. `page-types.md` now names the trigger for an area page: a
  section of current state swelling past the rest.
- Static checks still cannot tell whether an agent actually honored ownership
  during parallel work; that remains a behavior question for the evaluation
  harness in [open questions](../questions/open-questions.md).
