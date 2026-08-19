---
id: question.open-questions
type: question
status: active
confidence: assumed
updated: 2026-08-17
sources:
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - plugins/projipsa/codex-skills/outsource/references/verification.md
  - plugins/projipsa/.codex-plugin/plugin.json
  - tests/test_package_contract.py
related:
  - project.current-state
  - decision.host-adapter-separation.2026-08-02
---

# Open Questions

## Should `validate_memory.py` parse the declared root instead of scanning for it?

Reproduced on 2026-07-31 in a scratch fixture: a pointer block naming
`archive/docs/` passed validation of a real root at `docs/`. `names_root`
matches the declared root as a whole path segment, which rejects
`docs-archive/` but accepts any longer path ending in the root name, because the
preceding `/` is not part of its lookbehind.

This is the defect [pull request 3](https://github.com/SnoopyKim/projipsa/pull/3)
intended to fix, so the fix was incomplete rather than absent.

Resolution: parse the root the block declares, normalize it, and compare it to
the root being validated. Add a fixture for a block naming a path that contains
the real root as a trailing segment.

## Should Markdown code regions be excluded before the `CLAUDE.md` import check?

Reproduced on 2026-07-31 in the same fixture: a root `CLAUDE.md` whose only
`@AGENTS.md` occurrence sat inside a fenced code block passed validation. Claude
Code ignores imports inside code spans and fenced blocks, so a documentation
example is currently accepted as a working import.

Resolution: run `AGENTS_IMPORT` against `prose_only(text)` rather than the raw
text. That helper already strips both fenced blocks and code spans; the import
check simply does not use it. Add a fixture whose only occurrence is fenced.

## Should `related` IDs be resolved?

Reproduced on 2026-07-31: adding `project.does-not-exist` to a page's `related`
list produced no error. Links inside page bodies are checked, but frontmatter
`related` entries are not resolved against known page IDs, so a renamed or
deleted page leaves silent dangling references in every page that named it.

Resolution: collect every declared `id` in the memory root and fail on a
`related` entry that matches none of them. Decide first whether a forward
reference to a page that does not exist yet should be an error or a warning.

## Does a publish-time Codex validator still require `skills/`?

The 2026-08-02 layout kept Codex at `skills/` because an official Codex plugin
validator had rejected `codex-skills/`. On 2026-08-03, codex-cli 0.146.0
installed a plugin declaring `"skills": "./codex-skills/"` and listed its Skill
from that path in `codex debug prompt-input`, so the runtime accepts it. The
validator that produced the original rejection is not available in this
repository, so it could not be re-run.

Resolution: re-run the authoritative Codex plugin validator against
`plugins/projipsa/` before a first marketplace listing, and record whether
runtime acceptance and publish-time acceptance agree.

## Is the narrowed `outsource` trigger correct?

The trigger was narrowed to work that spans milestones or sessions, needs a
durable contract, or is hard to reverse. `outsource` is not in daily use, so
there is no evidence either way.

Resolution: use it, and record cases where it should have fired and did not.

## Should Skill triggering and workflow behavior be tested automatically?

No validator checks whether a Skill fires at the right moment or whether a
model follows its semantic workflow. The package tests preserve the 0.3.2
verification reference and delivery-state surface, but they cannot determine
whether a verifier rejects helper-only or early-exit evidence for a broader
claim. Triggering evidence remains a manual skill listing under
`claude --plugin-dir`. Official guidance recommends evaluation scenarios but
provides no runner.

Resolution: decide whether an evaluation harness belongs in this repository,
and whether it can run in CI given that it requires model calls. Include both
triggering cases and verification-behavior regressions covering actual paths,
preservation invariants, proxy evidence, and Maker-versus-technical verdicts.
