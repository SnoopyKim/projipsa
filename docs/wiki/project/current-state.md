---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-07-31
sources:
  - https://github.com/SnoopyKim/projipsa/pull/2
  - https://github.com/SnoopyKim/projipsa/pull/3
  - https://github.com/SnoopyKim/projipsa/pull/4
  - plugins/projipsa/.claude-plugin/plugin.json
  - .claude-plugin/marketplace.json
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.plugin-ship-boundary.2026-07-30
  - question.open-questions
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
  host pointer blocks in the repository's root `AGENTS.md` and `CLAUDE.md`. Its
  pointer checks are incomplete: three gaps were reproduced on 2026-07-31 and
  are recorded in [open questions](../questions/open-questions.md).
- 31 tests pass on Python 3.12 and 3.9.6. CI runs them on 3.9 and 3.13.
- `projipsa` is not listed in the SnoopyDev marketplace. The only installation
  anywhere is this source checkout, installed through
  `.claude-plugin/marketplace.json` at the repository root.
- The ship boundary is confirmed by an actual install, not only by reasoning:
  `~/.claude/plugins/cache/projipsa/projipsa/0.3.0/` holds exactly the plugin
  root — `.claude-plugin/`, `.codex-plugin/`, and `skills/`. `docs/`, `tests/`,
  and `scripts/` were not copied. `claude plugin details projipsa` reports
  three Skills and no agents, hooks, or MCP servers.

## In Progress

- Adopting Projipsa on this repository. This tree is that work.

## Explicitly Not Current

- No release. The marketplace lists `invee` and `outsource`, not `projipsa`.
- No `raw/` tree, because every current source has a stable versioned path.
- No `wiki/deliveries/` tree, because no delegated engagement is active.
- `outsource` is not in daily use yet.

## Active Defaults

- `docs/` is the memory root, and it is public.
- Pages created from a template start below `confirmed`: `inferred` for most
  types, `assumed` for `assumption`, `question`, `risk`, and `delivery`. A page
  is raised to `confirmed` only in the edit that lists its evidence.
- Development can either install this checkout through the root marketplace
  manifest or load the working tree with
  `claude --plugin-dir ./plugins/projipsa`. The installed cache is a
  version-pinned copy, not a live reference, so an edit reaches it only after a
  version bump plus `claude plugin update`.

## Validation

- `python3 scripts/validate_package.py` passes.
- `python3 -m unittest discover -s tests` passes, 31 tests, on Python 3.12 and
  3.9.6.
- `claude plugin validate ./plugins/projipsa --strict` passes.
- Each pointer-validation fix was reverted individually and failed exactly one
  test each time.
- `python3 plugins/projipsa/skills/projipsa/scripts/validate_memory.py docs`
  passes, and three of its gaps were reproduced in a scratch fixture built from
  this tree.

## Next Work

- Fix the three reproduced `validate_memory.py` gaps: an unparsed root
  declaration, Markdown code regions counted as real imports, and unresolved
  `related` IDs.
- Correct `page-types.md`, which states that templates ship
  `confidence: inferred`. Four ship `assumed`. `initialization.md` carried the
  same claim and was corrected; this copy was not.
- Decide whether the narrowed `outsource` trigger fires appropriately, using
  real usage rather than prediction.
- Decide when to list `projipsa` in the marketplace, and at which commit.
- Consider a skill-triggering evaluation harness, which no validator covers.
