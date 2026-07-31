---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-07-31
sources:
  - https://github.com/SnoopyKim/projipsa/pull/2
  - https://github.com/SnoopyKim/projipsa/pull/3
  - plugins/projipsa/.claude-plugin/plugin.json
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.plugin-ship-boundary.2026-07-30
---

# Current State

## Summary

Version 0.3.0 is complete in the repository and has not been released. The
three v0.3 Skills exist, the shipped surface has been separated from the
repository at `plugins/projipsa/`, and this memory tree is the project's first
use of Projipsa on itself.

## Confirmed Current

- Three public Skills ship: `projipsa`, `projipsa-init`, and `outsource`.
- `projipsa-init` is explicit-only on both hosts, enforced by
  `allow_implicit_invocation: false` for Codex and `disable-model-invocation:
  true` for Claude Code. A skill listing under `claude --plugin-dir` confirmed
  Claude Code hides it from the model.
- Only `plugins/projipsa/` is shipped. `scripts/validate_package.py` scans that
  tree and the repository README, nothing else.
- `validate_memory.py` owns everything under this memory root, including the
  host pointer blocks in the repository's root `AGENTS.md` and `CLAUDE.md`.
- 31 tests pass on Python 3.12 and 3.9.6. CI runs them on 3.9 and 3.13.
- `projipsa` is not listed in the SnoopyDev marketplace, so no installation of
  it exists anywhere yet.

## In Progress

- Adopting Projipsa on this repository. This tree is that work.

## Explicitly Not Current

- No release. The marketplace lists `invee` and `outsource`, not `projipsa`.
- No `raw/` tree, because every current source has a stable versioned path.
- No `wiki/deliveries/` tree, because no delegated engagement is active.
- `outsource` is not in daily use yet.

## Active Defaults

- `docs/` is the memory root, and it is public.
- Pages created from a template start at `confidence: inferred` and are raised
  to `confirmed` only in the edit that lists their evidence.
- Development loads the working tree with
  `claude --plugin-dir ./plugins/projipsa` rather than an installed copy.

## Validation

- `python3 scripts/validate_package.py` passes.
- `python3 -m unittest discover -s tests` passes, 31 tests, on Python 3.12 and
  3.9.6.
- `claude plugin validate ./plugins/projipsa --strict` passes.
- Each pointer-validation fix was reverted individually and failed exactly one
  test each time.

## Next Work

- Decide whether the narrowed `outsource` trigger fires appropriately, using
  real usage rather than prediction.
- Decide when to list `projipsa` in the marketplace, and at which commit.
- Consider a skill-triggering evaluation harness, which no validator covers.
