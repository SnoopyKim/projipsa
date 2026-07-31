---
id: question.open-questions
type: question
status: active
confidence: assumed
updated: 2026-07-31
sources:
  - plugins/projipsa/skills/projipsa/scripts/validate_memory.py
related:
  - project.current-state
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

## Does Codex tolerate the Claude Code frontmatter key?

`projipsa-init/SKILL.md` carries `disable-model-invocation: true`, which only
Claude Code defines. Two skills installed under `~/.codex/skills` carry keys
Codex has no semantics for and load normally, so the key is expected to be
inert. It has not been confirmed by running Codex against this Plugin.

Resolution: invoke `$projipsa-init` in Codex once and record the result. The
Claude Code side is confirmed: an install from this checkout reports three
Skills, and `projipsa-init` stays out of the model's skill listing.

## Is the narrowed `outsource` trigger correct?

The trigger was narrowed to work that spans milestones or sessions, needs a
durable contract, or is hard to reverse. `outsource` is not in daily use, so
there is no evidence either way.

Resolution: use it, and record cases where it should have fired and did not.

## When should 0.3.0 be released?

The version has never been listed in the marketplace, so nothing has shipped
and no version bump is owed. It is unresolved whether adopting this memory tree
should precede or follow a first listing.

## Should skill triggering be tested automatically?

No validator checks whether a Skill fires at the right moment. The only
evidence so far is a manual skill listing under `claude --plugin-dir`. Official
guidance recommends evaluation scenarios but provides no runner.

Resolution: decide whether an evaluation harness belongs in this repository,
and whether it can run in CI given that it requires model calls.

## Should the memory contract know about public roots?

`operations.md` instructs preserving conversation-only artifacts under `raw/`,
and the contract has no notion of a publicly visible memory root. This project
handles that locally in `AGENTS.md`, which leaves the default pointed the wrong
way for every other public repository that adopts Projipsa.

Resolution: decide whether initialization should ask whether the memory root is
public and record the answer in the adoption decision.
