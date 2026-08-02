---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-08-03
sources:
  - https://github.com/SnoopyKim/projipsa/pull/2
  - https://github.com/SnoopyKim/projipsa/pull/3
  - https://github.com/SnoopyKim/projipsa/pull/4
  - plugins/projipsa/.claude-plugin/plugin.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/codex-skills/projipsa/references/page-types.md
  - scripts/validate_package.py
  - wiki/decisions/2026-08-02-host-adapter-separation.md
  - .agents/plugins/marketplace.json
  - .claude-plugin/marketplace.json
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.plugin-ship-boundary.2026-07-30
  - decision.host-adapter-separation.2026-08-02
  - question.open-questions
---

# Current State

## Summary

Version 0.3.1 is complete in the repository and has not been released. The
three v0.3 Skills exist, the shipped surface has been separated from the
repository at `plugins/projipsa/`, and this memory tree is the project's first
use of Projipsa on itself. 0.3.1 is a packaging fix: it stops Claude Code from
exposing every public Skill twice.

## Confirmed Current

- Three public Skills ship: `projipsa`, `projipsa-init`, and `outsource`.
- The public workflows are shared, but their harnesses are isolated: Codex
  loads thin adapters from `codex-skills/`, while Claude Code loads thin
  adapters from `claude-skills/`. The package ships no `skills/` directory. See
  [the host-adapter
  decision](../decisions/2026-08-02-host-adapter-separation.md).
- Claude Code adds its manifest-declared Skill directory to the default
  `skills/` scan rather than replacing it. While Codex adapters sat in
  `skills/`, `claude plugin details projipsa` reported six Skills, two per
  public name. Codex does the opposite: it loads only the declared directory
  and ignores a sibling `skills/`.
- Local installation is separated at the repository boundary too: Codex uses
  `.agents/plugins/marketplace.json`; Claude Code uses
  `.claude-plugin/marketplace.json`.
- Codex plugin invocations are namespace-qualified. In particular,
  `$projipsa:projipsa-init` loaded the correct explicit-only Skill in a fresh
  process; the shorter `$projipsa-init` did not.
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
- 35 tests pass on Python 3.12. The preceding 31-test suite also passed on
  Python 3.9.6, and CI runs the current suite on 3.9 and 3.13.
- `projipsa` is not listed in the SnoopyDev marketplace. Development installs
  currently use this source checkout: Codex through `.agents/` and Claude Code
  through `.claude-plugin/` at the repository root.
- The ship boundary is confirmed by an actual Claude Code install: its cache
  holds the plugin root while repository `docs/`, `tests/`, and `scripts/`
  remain outside the installed copy.

## In Progress

- The 0.3.1 packaging fix that renames the Codex adapter directory to
  `codex-skills/` is committed on a branch and not yet merged.

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
- `python3 -m unittest discover -s tests` passes, 35 tests, on Python 3.12.
  Two of them fail if the package reintroduces a `skills/` directory or if the
  two manifests name the same one.
- `claude plugin validate ./plugins/projipsa --strict` passes.
- The authoritative Codex plugin validator and all three Codex Skill validators
  passed against the 2026-08-02 layout, when Codex adapters were still at
  `skills/`. They have not been re-run against `codex-skills/`; see [open
  questions](../questions/open-questions.md).
- codex-cli 0.146.0 installed a probe plugin declaring
  `"skills": "./codex-skills/"` into an isolated `CODEX_HOME` and listed its
  Skill from that path in `codex debug prompt-input`. With that manifest, a
  sibling `skills/` directory was ignored.
- A fresh Codex process invoked `$projipsa:projipsa-init`, created only the
  minimum memory core in a temporary repository, and passed the shipped memory
  validator with 4 maintained pages.
- A Claude Code 2.1.220 process loaded the working-tree plugin through
  `--plugin-dir`, exposed exactly the three Projipsa commands, and resolved
  `/projipsa:projipsa-init` without tools or writes. Counting commands that way
  hid the duplicate Skills; `claude plugin details projipsa` counts loaded
  Skills and is the check that found it.
- Each pointer-validation fix was reverted individually and failed exactly one
  test each time.
- `python3 plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py docs`
  passes, and three of its gaps were reproduced in a scratch fixture built from
  this tree.

## Next Work

- Fix the three reproduced `validate_memory.py` gaps: an unparsed root
  declaration, Markdown code regions counted as real imports, and unresolved
  `related` IDs.
- Decide whether the narrowed `outsource` trigger fires appropriately, using
  real usage rather than prediction.
- Decide when to list `projipsa` in the marketplace, and at which commit,
  after re-running the authoritative Codex plugin validator against
  `codex-skills/`.
- Consider a skill-triggering evaluation harness, which no validator covers.
