---
id: decision.projipsa-adoption.2026-07-31
type: decision
status: active
confidence: confirmed
updated: 2026-07-31
projipsa_adoption: true
sources:
  - https://github.com/SnoopyKim/projipsa/pull/4
  - README.md
  - https://github.com/SnoopyKim/projipsa/pull/2
related:
  - project.current-state
  - decision.plugin-ship-boundary.2026-07-30
  - question.open-questions
supersedes: []
superseded_by: []
---

# Adopt Projipsa in its own repository

## Decision

`docs/` is this project's memory root, maintained by Projipsa itself. The
memory root is public, and `docs/AGENTS.md` carries the rules that follow from
that.

## Context

Projipsa manages project memory for other projects. Applying it here makes the
dogfood the eval: the provenance rules, the pointer blocks, and the template
defaults get exercised on a real project rather than on fixtures. It also
publishes a working example of the Plugin's own output.

This became safe only after [the ship
boundary](2026-07-30-plugin-ship-boundary.md) moved shipped content under
`plugins/projipsa/`. Before that, a memory tree here would have been copied to
every installer and would have gated package validation.

## Canonical layer relationship

- `wiki/**` is maintained synthesis and the project-level source of truth.
- `logs/**` is append-only chronology, never current truth.
- `raw/**` preserves source material that has no stable versioned path. None
  exists yet, because this project's evidence is merged pull requests, commits,
  CI runs, and files under `plugins/`, all of which are cited directly.

## The memory root is public

`SnoopyKim/projipsa` is a public repository, so this memory is readable by
anyone. Two consequences are recorded in `docs/AGENTS.md`: prefer citing a
stable path over copying content into `raw/`, and write for a public reader
rather than recording assessments of people or other products.

The alternative — keeping memory out of version control — was rejected. The
memory validator resolves every `sources` entry, so an ignored tree fails for
anyone who clones it, and an agent opening a fresh clone would find no memory
at all, which defeats the purpose.

## Legacy paths and optional families

No documentation was migrated. The repository had no `docs/` tree and no root
instruction files before this decision; `README.md` remains the product
overview and was not moved. No optional page families were created. In
particular `wiki/deliveries/` is absent until a delegated engagement needs
durable state.

## Known gaps

- Whether a public memory root should be a first-class concept in the memory
  contract, rather than a per-project rule, is unresolved. See
  [open questions](../questions/open-questions.md).
- No evaluation harness covers whether a Skill triggers at the right moment.
- `validate_memory.py` accepts three classes of broken pointer and reference,
  all reproduced on 2026-07-31 and recorded in
  [open questions](../questions/open-questions.md). This tree is valid under a
  validator that is weaker than the contract it enforces.

## Consequences

- Root `AGENTS.md` and root `CLAUDE.md` now exist and carry the host pointer
  block, so both hosts can find this tree.
- Memory health is checked by `validate_memory.py`, separately from the package
  contract, so documentation drift can never block a release.
