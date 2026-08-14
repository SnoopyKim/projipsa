---
id: project.current-state
type: project
status: active
confidence: confirmed
updated: 2026-08-14
sources:
  - https://github.com/SnoopyKim/projipsa/pull/7
  - https://github.com/SnoopyKim/projipsa/pull/12
  - https://github.com/SnoopyKim/projipsa/releases/tag/v0.3.2
  - https://github.com/SnoopyKim/projipsa/releases/tag/v0.4.0
  - https://github.com/SnoopyKim/projipsa/issues/9
  - https://github.com/SnoopyKim/projipsa/issues/10
  - https://github.com/SnoopyKim/projipsa/issues/11
  - README.md
  - CONTRIBUTING.md
  - plugins/projipsa/.claude-plugin/plugin.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/codex-skills/projipsa/references/page-types.md
  - plugins/projipsa/codex-skills/projipsa/references/operations.md
  - plugins/projipsa/codex-skills/projipsa-init/references/initialization.md
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - plugins/projipsa/shared/projipsa.md
  - plugins/projipsa/shared/outsource.md
  - plugins/projipsa/codex-skills/outsource/references/verification.md
  - plugins/projipsa/codex-skills/projipsa/assets/templates/delivery.md
  - scripts/validate_package.py
  - tests/test_package_contract.py
  - tests/test_validate_memory.py
  - https://github.com/mattpocock/skills
  - wiki/decisions/2026-08-13-rules-must-earn-their-place.md
  - wiki/decisions/2026-08-12-parallel-safe-memory-tree.md
  - wiki/decisions/2026-08-11-qa-oriented-verification-claims.md
  - wiki/decisions/2026-08-02-host-adapter-separation.md
  - .agents/plugins/marketplace.json
  - .claude-plugin/marketplace.json
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.plugin-ship-boundary.2026-07-30
  - decision.host-adapter-separation.2026-08-02
  - decision.qa-oriented-verification-claims.2026-08-11
  - decision.parallel-safe-memory-tree.2026-08-12
  - decision.rules-must-earn-their-place.2026-08-13
  - question.open-questions
---

# Current State

## Summary

0.4.0 was merged through PR 12, tagged, published as a GitHub Release, and
installed in both the Codex and Claude Code user caches on 2026-08-14. It
answers adopter feedback issues
[9](https://github.com/SnoopyKim/projipsa/issues/9),
[10](https://github.com/SnoopyKim/projipsa/issues/10), and
[11](https://github.com/SnoopyKim/projipsa/issues/11) with a memory tree that
survives parallel worktrees, and then shrinks the memory contract itself: a rule
is kept only when a future reader would otherwise reach a wrong conclusion. See
[the parallel-safe memory
decision](../decisions/2026-08-12-parallel-safe-memory-tree.md) and [the rule
criterion](../decisions/2026-08-13-rules-must-earn-their-place.md).

It is a minor rather than a patch release because the required surface shrank
and a project that already kept nested chronology sees findings in files it
never touched.

The project's stated purpose was corrected on 2026-08-03. Projipsa exists so
that project understanding survives the session and substantial work can be
delegated against it; the memory is the durable shared state that delegated
work runs on. Cross-host support is a distribution constraint, not the goal.
See [the overview](overview.md).

## Confirmed Current

- Three public Skills ship: `projipsa`, `projipsa-init`, and `outsource`.
- Outsource verification starts from the service user, artifact consumer,
  operator, or QA perspective and traces the actual user or data path. It
  records `direct`, `proxy`, `reported`, and `not_run` evidence separately and
  does not promote a partial path or early exit into a broader passing claim.
  See [the verification
  decision](../decisions/2026-08-11-qa-oriented-verification-claims.md).
- Preservation prohibitions are negative acceptance criteria when adjacent
  delivery work could violate them. Execution status, verification status, and
  Maker decision are independent fields; Maker acceptance cannot rewrite a
  technical verdict.
- The public workflows are shared, but their harnesses are isolated: Codex
  loads thin adapters from `codex-skills/`, while Claude Code loads thin
  adapters from `claude-skills/`. The package ships no `skills/` directory. See
  [the host-adapter
  decision](../decisions/2026-08-02-host-adapter-separation.md).
- Local installation is separated at the repository boundary too: Codex uses
  `.agents/plugins/marketplace.json`; Claude Code uses
  `.claude-plugin/marketplace.json`.
- Codex plugin invocations are namespace-qualified: `$projipsa:projipsa-init`
  resolves and the shorter `$projipsa-init` does not.
- `projipsa-init` is explicit-only on both hosts, enforced by
  `allow_implicit_invocation: false` for Codex and `disable-model-invocation:
  true` for Claude Code.
- Existing projects upgrade only through explicit `projipsa-init`; 0.3.x pages
  and frontmatter stay valid, and chronology changes require a dated cutover.
- Only `plugins/projipsa/` is shipped. `scripts/validate_package.py` scans that
  tree and the repository README for prose, links, and Skill contracts, and
  additionally reads the two root development marketplace manifests. Nothing
  under `docs/` is in its scope.
- User-facing documentation and contributor documentation are separated:
  `README.md` covers purpose, install, and usage; `CONTRIBUTING.md` covers
  repository layout, the `skills/` invariant, and the validators.
- `validate_memory.py` owns everything under this memory root, including the
  host pointer blocks in the repository's root `AGENTS.md` and `CLAUDE.md`. Its
  pointer checks are incomplete: three gaps were reproduced on 2026-07-31 and
  are recorded in [open questions](../questions/open-questions.md).
- The memory contract states write ownership for parallel work, treats monthly
  chronology as a default rather than the only unit, and defines current state
  as a replaced page whose `sources` are pruned with their claims. The memory
  validator accepts month, day, and per-writer log names, checks every file
  under `logs/**`, and prints non-blocking `warning:` lines for current-state
  drift.
- Each memory rule is stated in one place and reached by a link. The Update
  operation owns the eviction rule and the ownership table; `page-types.md` and
  the shared workflow name them and point. The generated `AGENTS.md` restates
  rules on purpose, because an adopting project reads it without these
  references.
- Integrate is the fifth operation of the `projipsa` Skill, not a fourth Skill.
  It requires the same authorized write scope as Update and writes the
  single-owner shared pages once from a merged result. The validator compares
  per-writer chronology with the later of current state's meaningful update and
  an append-only `integrate` entry; the workflow checks that writer logs have
  actually merged before running Integrate. The comparison is day-granular, so
  a writer update landing after integration on the same day is not detected.
- The contract requires three files and three frontmatter keys: `AGENTS.md`,
  `index.md`, `current-state.md`, and `id`, `updated`, `sources`. `type` is
  read from a page's directory when absent, `status` and `confidence` default
  to `active` and `inferred`, and each dropped field is still validated when a
  page states it. The Projipsa adoption decision stays required as the
  initialization idempotency marker.
- 51 tests pass locally on Python 3.12 and in CI on Python 3.9 and 3.13. The
  three new regressions cover chronology
  navigation, real calendar dates, and an append-only Integrate watermark. The
  release merge commit is `7a420f3`.
- `projipsa` is not listed in the SnoopyDev marketplace. Development installs
  currently use this source checkout: Codex through `.agents/` and Claude Code
  through `.claude-plugin/` at the repository root.
- The Codex and Claude Code caches both hold 0.4.0, contain no legacy `skills/`
  directory, and expose the three manifest-declared Skills. Claude Code reports
  that a restart is required before an already-running session applies the
  update.

## In Progress

- No 0.4.0 release operation remains in progress. Public marketplace listing is
  separate future work.

## Explicitly Not Current

- No public marketplace listing. The SnoopyDev marketplace lists `invee` and
  `outsource`, not `projipsa`; 0.3.2 is distributed from this source repository.
- No `raw/` tree, because every current source has a stable versioned path.
- No `wiki/deliveries/` tree, because no delegated engagement is active.
- `outsource` is not in daily use yet.

## Active Defaults

- A rule enters the memory contract only after it is graded by what a future
  reader loses when it breaks: wrong conclusion is an error, slowed but
  recovering is a warning, unaffected is not a rule. See [the rule
  criterion](../decisions/2026-08-13-rules-must-earn-their-place.md).
- `docs/` is the memory root, and it is public.
- The package validator checks structure, policy, and contract surface only.
  Vocabulary and concept checks do not belong in it: a banned-word scan and a
  required-phrase check on the plugin description were both removed on
  2026-08-03. Documentation carries the concept instead.
- Pages created from a template start below `confirmed`: `inferred` for most
  types, `assumed` for `assumption`, `question`, `risk`, and `delivery`. A page
  is raised to `confirmed` only in the edit that lists its evidence.
- Development can either install this checkout through the root marketplace
  manifest or load the working tree with
  `claude --plugin-dir ./plugins/projipsa`. The installed cache is a
  version-pinned copy, not a live reference, so an edit reaches it only after a
  version bump plus `claude plugin update`.

## Validation

Latest evidence for the current working tree. Earlier runs stay in the
chronology: [August](../../logs/2026-08.md) and [July](../../logs/2026-07.md).

- `python3 scripts/validate_package.py` passes.
- `python3 -m unittest discover -s tests` passes, 51 tests, on Python 3.12.
  The focused cases cover chronology granularity and navigation, recursive
  checking, drift warnings, pending integration, both watermarks, and
  single-writer silence; details are in the August chronology.
- GitHub CI passes the full suite on Python 3.9 and 3.13 for both the pushed
  branch and PR 12.
- `python3 plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py .`
  accepts this memory root and prints no warning.
- `claude plugin validate ./plugins/projipsa --strict` passes.
- No Python 3.9 runtime is available locally; GitHub CI supplies the direct
  runtime evidence for that supported floor.
- The authoritative Codex plugin validator and all three Codex Skill validators
  passed against the 2026-08-02 layout, when Codex adapters were still at
  `skills/`. They have not been re-run against `codex-skills/`; see [open
  questions](../questions/open-questions.md).
- The 0.4.0 tag, GitHub Release, and both host installations were verified on
  2026-08-14 and are recorded in [the August chronology](../../logs/2026-08.md).

## Next Work

- Run explicit `projipsa-init` Upgrade or Repair in an adopting repository only
  when its owner asks for that repository to migrate; Plugin installation alone
  never authorizes memory rewrites.
- Fix the three reproduced `validate_memory.py` gaps: an unparsed root
  declaration, Markdown code regions counted as real imports, and unresolved
  `related` IDs.
- Decide whether the narrowed `outsource` trigger fires appropriately, using
  real usage rather than prediction.
- Decide when to list `projipsa` in the marketplace, and at which commit,
  after re-running the authoritative Codex plugin validator against
  `codex-skills/`.
- Consider a Skill-triggering and workflow-behavior evaluation harness, which
  no static validator covers. Include scenarios that reject helper-only or
  early-exit evidence for broader claims, exercise preservation invariants, and
  keep Maker acceptance separate from technical verdicts.
