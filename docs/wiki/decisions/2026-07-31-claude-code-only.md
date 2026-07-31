---
id: decision.claude-code-only.2026-07-31
type: decision
status: active
confidence: confirmed
updated: 2026-07-31
sources:
  - plugins/projipsa/.claude-plugin/plugin.json
  - scripts/validate_package.py
related:
  - project.overview
  - project.current-state
  - decision.projipsa-adoption.2026-07-31
  - question.open-questions
supersedes: []
superseded_by: []
---

# Target Claude Code only

## Decision

Projipsa targets Claude Code alone. The Codex manifest, the per-Skill
`agents/openai.yaml` loading policies, and the `$name` invocations are removed
from the shipped tree, and `scripts/validate_package.py` now validates a
single-host package.

## Context

The dual-host package had one physical `SKILL.md` per Skill serving two hosts
that use different control points: Claude Code reads `disable-model-invocation`
from `SKILL.md` frontmatter, and Codex reads `allow_implicit_invocation` from
`agents/openai.yaml`. `projipsa-init` therefore shipped a Claude-only
frontmatter key that Codex has no semantics for.

That coupling was never verified against Codex. It also made every review of
the package argue about which host's contract was authoritative, because the
project's own validator asserted alignment that no Codex run had confirmed.
Nothing was installed anywhere yet, so the cost of narrowing was zero.

## Alternatives Considered

- Keep both hosts and split the harness: separate `SKILL.md` files, manifest
  entrypoints, and validators per host, sharing only references, scripts, and
  templates.
- Keep both hosts and record the shared-`SKILL.md` coupling as technical debt.
- Keep both hosts and verify Codex tolerance of the Claude-only key first.

## Reasoning

- The Maker works in Claude Code. A second host was an unverified ambition, not
  a use in progress.
- Splitting the harness doubles the surface a single maintainer keeps aligned,
  and the alignment is what the project's own validator kept getting wrong.
- Deleting the second host resolves the contradiction rather than documenting
  it. There is no debt left to track.
- Narrowing is reversible while nothing is installed. Re-adding Codex later
  means adding files, not unwinding claims already made to users.

## Consequences

- `plugins/projipsa/.codex-plugin/` and all three `skills/*/agents/openai.yaml`
  are deleted. `disable-model-invocation` is now the only mechanical
  loading-policy gate, and `validate_package.py` fails if another host's
  metadata reappears in the shipped tree.
- Skill descriptions and the README advertise `/projipsa:name` only. The
  validator rejects a description that advertises `$name`, because Claude Code
  cannot trigger it.
- The version is `0.4.0`. Nothing was released at `0.3.0`, so no installed copy
  changes behavior.
- Root `AGENTS.md` still carries the canonical memory-pointer block and root
  `CLAUDE.md` still imports it. `AGENTS.md` is kept as the portable convention
  other coding agents read, not as Codex support. `validate_memory.py` is
  unchanged.
- The open question about whether Codex tolerates the Claude-only frontmatter
  key is resolved as moot rather than answered.
