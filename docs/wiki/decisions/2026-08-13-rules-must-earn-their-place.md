---
id: decision.rules-must-earn-their-place.2026-08-13
type: decision
status: active
confidence: confirmed
updated: 2026-08-13
sources:
  - https://github.com/mattpocock/skills
  - plugins/projipsa/codex-skills/projipsa/references/memory-contract.md
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - plugins/projipsa/shared/projipsa.md
related:
  - project.current-state
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.parallel-safe-memory-tree.2026-08-12
supersedes: []
superseded_by: []
---

# Grade a rule by the damage a broken one does

## Decision

A rule enters the memory contract only after it is graded by what a future
reader loses when it is broken — six months on, with nobody left who remembers
the work. A reader who reaches a wrong conclusion makes it an error, a reader
who is slowed but recovers makes it a warning, and an unaffected reader means
it is not a rule at all.

The criterion lives in `memory-contract.md` and governs both the shipped
validator and an adopting project's own conventions. It is stated once; the
shared workflow reaches it through a pointer rather than restating it.

## Context

The memory validator enforces roughly thirty-three hard errors, and the shipped
plugin carries about 99 KB of prose against 27 KB of script. Much of that prose
exists to explain the rules, so rule count drives document weight.

Grading the current set against the criterion puts a large share in the third
row. `related` is required on every maintained page and is satisfied by `[]`,
so it costs load on every page and changes nothing. Five required files force a
new project to create `overview.md` and `open-questions.md` before it has
anything to say, and the template text that fills them is the same unresolved
placeholder the validator rejects elsewhere. A required decision page makes a
project with no decisions yet invent one.

The immediate prompt was a comparison with `mattpocock/skills`, whose thirty-five
skills ship no validation script at all and whose own writing guidance names
the failure modes this tree shows: one meaning restated in several files, and
accretion that continues because adding feels safe and removing feels risky.

## Alternatives Considered

- Cut the specific rules now and leave the criterion unstated.
- Keep the rules and reduce only the prose that explains them.
- Adopt the benchmark's shape: many small independent skills, no format
  contract, and the repository's existing artifacts as the memory.
- Make the criterion advice in the workflow rather than part of the contract.

## Reasoning

- Cutting rules without the criterion fixes the count and not the mechanism.
  The set grew because nothing gated additions, so an ungated set grows back.
- Prose weight is downstream of rule count. Removing a rule removes its
  explanations everywhere they were written, which the reverse does not do.
- The benchmark's shape suits skills that act on artifacts the environment
  already owns. This memory is a durable artifact that several branches write
  and every later session reads, and that is the one property that earns a
  format contract at all. It also sets the bound: the contract may enforce what
  keeps the tree readable and sourced, and nothing beyond it.
- A criterion in the workflow would be read while working and forgotten while
  designing. The contract is where the boundary questions already live.
- The error and warning rows match the validator's two existing channels, so
  the grade a rule receives is directly implementable.

## Consequences

- `memory-contract.md` opens with the criterion, and `shared/projipsa.md`
  points at it when a new rule or convention is being weighed.
- The reduction is applied. Required files went from five to three, dropping
  `overview.md` and `open-questions.md`; required frontmatter went from seven
  keys to `id`, `updated`, and `sources`; `type` is read from the page's
  directory when absent; `status` and `confidence` default to `active` and
  `inferred`; the general decision-page requirement and the index link to a
  decision page are gone; and the confirmed-evidence chain is now a warning.
  Every dropped field is still checked when a page states it.
- The Projipsa adoption decision is the deliberate exception. It reads as
  ceremony but carries initialization idempotency, which is why the validator
  rejects a second one. Because it stays required, a tree still ends up with
  one decision page, so dropping the general requirement is a change in what
  the contract means rather than in what a valid tree contains.
- Nothing in the reduction touches what the pending-integration warning needs:
  `updated`, `current-state.md`, and the chronology logs all stay required. An
  append-only `integrate` entry advances the watermark when shared state has no
  meaningful content change, so no new frontmatter field is required.
- Prose deduplication remains separate work. A single meaning restated in five
  files is a writing failure that no rule cut removes.
