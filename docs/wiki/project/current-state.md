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
  - decision.claude-code-only.2026-07-31
  - question.open-questions
---

# Current State

## Summary

Version 0.4.0 exists in the repository and has not been released. Projipsa
targets Claude Code alone, the shipped surface is separated at
`plugins/projipsa/`, and this memory tree is the project's own use of Projipsa
on itself.

## Confirmed Current

- Three public Skills ship: `projipsa`, `projipsa-init`, and `outsource`.
- Claude Code is the only supported host. `.codex-plugin/` and every
  `skills/*/agents/openai.yaml` are deleted, and `validate_package.py` fails if
  either reappears.
- `projipsa-init` is explicit-only, enforced by `disable-model-invocation: true`
  in its frontmatter. That is now the only mechanical loading gate.
- Skill descriptions and the README advertise `/projipsa:name` only. The package
  validator rejects a description that advertises `$name`.
- Only `plugins/projipsa/` is shipped. `scripts/validate_package.py` scans that
  tree and the repository README, nothing else.
- `.claude-plugin/marketplace.json` at the repository root makes this checkout
  installable as the `projipsa` marketplace. `claude plugin details projipsa`
  reports version 0.4.0 with three Skills and no other components.
- The ship boundary is confirmed by an actual install, not only by reasoning:
  `~/.claude/plugins/cache/projipsa/projipsa/0.4.0/` holds `.claude-plugin/`
  and `skills/` and nothing else. `docs/`, `tests/`, and `scripts/` were not
  copied.
- `validate_memory.py` owns everything under this memory root, including the
  pointer blocks in the repository's root `AGENTS.md` and `CLAUDE.md`. Its
  pointer checks are known to be incomplete; see
  [open questions](../questions/open-questions.md).
- 39 tests pass on Python 3.12. CI runs them on 3.9 and 3.13.
- `projipsa` is not listed in the SnoopyDev marketplace, so the only
  installation anywhere is this local source checkout.

## In Progress

- Nothing. The host scope cut and this memory update are the current work, and
  both are complete pending review.

## Explicitly Not Current

- No release. The SnoopyDev marketplace lists `invee` and `outsource`, not
  `projipsa`.
- No Codex support. It was removed rather than deferred.
- No `raw/` tree, because every current source has a stable versioned path.
- No `wiki/deliveries/` tree, because no delegated engagement is active.
- `outsource` is not in daily use yet.

## Active Defaults

- `docs/` is the memory root, and it is public.
- Pages created from a template start below `confirmed`: `inferred` for most
  types, `assumed` for `assumption`, `question`, `risk`, and `delivery`. A page
  is raised to `confirmed` only in the edit that lists its evidence.
- Development installs this checkout through the root marketplace manifest.
  `claude --plugin-dir ./plugins/projipsa` remains available for a single
  session.
- The installed cache is a version-pinned copy, not a live reference to the
  checkout. A later edit under `plugins/projipsa/` reaches an installed copy
  only after a version bump plus `claude plugin update`, or through
  `--plugin-dir` for one session.

## Validation

- `python3 scripts/validate_package.py` passes.
- `python3 -m unittest discover -s tests` passes, 39 tests, on Python 3.12.
- Each new package-validator check was disabled individually and failed only
  its own test: two for foreign-host metadata, one each for the `$name`
  rejection, the stale manifest field, the required manifest fields, and the
  `disable-model-invocation` gate.
- `claude plugin validate ./plugins/projipsa --strict` passes, and
  `claude plugin validate . --strict` passes for the marketplace manifest.
- `python3 plugins/projipsa/skills/projipsa/scripts/validate_memory.py docs`
  passes.
- Three `validate_memory.py` gaps were reproduced in a scratch fixture and are
  recorded as open questions. They are not fixed.

## Next Work

- Fix the three reproduced `validate_memory.py` gaps: an unparsed root
  declaration, Markdown code regions counted as real imports, and unresolved
  `related` IDs.
- Decide whether the narrowed `outsource` trigger fires appropriately, using
  real usage rather than prediction.
- Decide when to list `projipsa` in the marketplace, and at which commit.
- Consider a skill-triggering evaluation harness, which no validator covers.
