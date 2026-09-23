---
id: question.open-questions
type: question
status: active
confidence: assumed
updated: 2026-09-23
sources:
  - plugins/projipsa/codex-skills/projipsa/scripts/validate_memory.py
  - wiki/decisions/2026-09-23-project-memory-focus.md
  - wiki/areas/project-memory-references.md
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

## Do memory workflows improve work across sessions?

Outsource triggering is no longer an active question after the 2026-09-23
memory-focus decision. Its earlier uncertainty remains in Git history.

No validator checks whether relevant memory is retrieved, a stale fact is
rechecked, a new finding is preserved, or a later task benefits. Package and
memory tests establish structure and compatibility only.

Resolution: run the multi-session scenarios in the September source review,
comparing a baseline agent, the earlier Projipsa, and the revised memory-only
workflow with the same model, tools, and comparable budgets. Record recall
failures and update omissions before choosing hooks, a derived search index,
or automated dependency invalidation.

## Why did the active task expose an older installed Skill surface?

The August record reports a 0.5.0 install, while this 2026-09-23 task was given
cached Skills under 0.3.0. These are different observations, not proof of the
cause. Check current host discovery and task/session refresh behavior during a
separately authorized install/release task; do not infer the active Skill
version from repository manifests.
