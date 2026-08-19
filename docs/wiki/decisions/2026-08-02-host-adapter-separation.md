---
id: decision.host-adapter-separation.2026-08-02
type: decision
status: active
confidence: confirmed
updated: 2026-08-19
sources:
  - .agents/plugins/marketplace.json
  - .claude-plugin/marketplace.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/.claude-plugin/plugin.json
  - scripts/validate_package.py
  - https://docs.x.ai/build/features/skills-plugins-marketplaces
related:
  - project.current-state
  - project.overview
  - decision.plugin-ship-boundary.2026-07-30
  - question.open-questions
supersedes: []
superseded_by: []
---

# Separate host adapters inside one shipped plugin

## Decision

Projipsa remains one shipped plugin under `plugins/projipsa/`. Three supported
hosts use two thin Skill adapter dialects:

- `.agents/plugins/marketplace.json` is the Codex development marketplace;
  `.claude-plugin/marketplace.json` remains the Claude Code marketplace.
- `codex-skills/` is the Codex entry point and contains Codex metadata plus the
  canonical resources used by the shared workflows.
- `claude-skills/` is the Claude Code entry point and contains Claude-compatible
  frontmatter. Grok Build reuses it through its official Claude Code
  compatibility layer.
- `shared/` contains the host-neutral workflow body for each public Skill.
- The package ships no directory named `skills/`, for any host.

Both manifests expose the same four public Skill names. The package validator
checks the two adapter dialects and their loading policies independently; Grok
validation checks the shipped Claude-compatible manifest and adapter surface.

## Context

The original layout made both hosts read the same `SKILL.md`. That kept prose
identical, but also exposed Claude Code's `disable-model-invocation` key to the
Codex package surface.

The first separation, on 2026-08-02, kept Codex at `skills/` and gave Claude
Code `claude-skills/`. That layout exposed every public Skill twice in Claude
Code: `claude plugin details projipsa` reported six Skills, two per name,
because Claude Code adds the manifest-declared directory to its default
`skills/` scan instead of replacing it. The earlier smoke test missed it by
counting `/projipsa:<skill>` commands rather than loaded Skills.

Two probes on 2026-08-03, in an isolated `CODEX_HOME` with codex-cli 0.146.0,
settled the remaining question:

- A plugin declaring `"skills": "./codex-skills/"` installed, and
  `codex debug prompt-input` listed its Skill from that path. Codex accepts a
  non-default Skill directory at runtime.
- With that manifest, a sibling `skills/` directory was ignored entirely. Codex
  resolves only the declared path, so its behaviour is the opposite of Claude
  Code's.

Only one host scans `skills/` implicitly, and only the other one can be moved
off it, so the fix is to leave that name unused.

On 2026-08-19, Grok Build 1.0.5 added no third dialect requirement. Its official
documentation says it automatically reads Claude Code marketplaces, plugins,
Skills, MCPs, agents, hooks, and instruction files. A local validation and
inspection loaded Projipsa's four Skills from `claude-skills/`. Shipping a
separate Grok tree would therefore create another copy to drift without adding
a distinct contract.

The two hosts implement explicit-only loading differently. Sharing workflow
content is useful, but sharing the incompatible adapter surface is not.
Codex also exposes plugin Skills with a plugin-qualified name: the onboarding
Skill is invoked as `$projipsa:projipsa-init`, not `$projipsa-init`. A smoke
test reproduced the shorter text falling through to the general memory Skill,
while the qualified invocation loaded the intended adapter and completed a
docs-only initialization.

## Alternatives Considered

- Keep one shared `SKILL.md` and rely on each host ignoring the other's keys.
- Ship two complete plugin roots, duplicating every workflow and resource.
- Generate two packages from a third source tree before every install.
- Keep Codex at `skills/` and accept duplicate Claude Code Skills.
- Add a third Grok-specific adapter tree despite Grok's Claude compatibility.

## Reasoning

- Thin adapters isolate the host-specific invocation contract while preserving
  one canonical workflow body.
- A host-named directory per adapter makes the duplicate exposure structurally
  impossible rather than something a reviewer must notice.
- One plugin root preserves the existing cache and ship boundary and avoids
  duplicated resource trees that could drift.

## Consequences

- A Skill change may affect a shared workflow, one host adapter, or both; the
  validator must distinguish those surfaces.
- Codex documentation, default prompts, and adapter metadata must use
  `$projipsa:projipsa`, `$projipsa:projipsa-init`, and
  `$projipsa:compact`, and `$projipsa:outsource`; Claude Code and Grok Build
  keep `/projipsa:<skill>`.
- Codex, Claude Code, and Grok Build validation must all pass before release.
- Installing one host still copies the complete plugin root, but only that
  host's manifest-selected adapters are exposed as Skills.
- The Codex adapter tree still holds the canonical references, templates, and
  scripts that every host's shared workflows link to, so Claude-compatible
  readers follow `../codex-skills/...` links. Moving those resources to a
  host-neutral home is deferred, not decided against.
- The earlier claim that Codex requires `skills/` was recorded from a
  publish-time validator run that this repository can no longer reproduce; the
  runtime evidence above governs the layout. Whether a publish-time validator
  still rejects a non-default path is [an open
  question](../questions/open-questions.md) to settle before a first listing.
