---
id: question.open-questions
type: question
status: active
confidence: assumed
updated: 2026-07-31
sources: []
related:
  - project.current-state
---

# Open Questions

## Does Codex tolerate the Claude Code frontmatter key?

`projipsa-init/SKILL.md` carries `disable-model-invocation: true`, which only
Claude Code defines. Two skills installed under `~/.codex/skills` carry keys
Codex has no semantics for and load normally, so the key is expected to be
inert. It has not been confirmed by running Codex against this Plugin.

Resolution: invoke `$projipsa-init` in Codex once and record the result.

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
