---
id: decision.host-adapter-separation.2026-08-02
type: decision
status: active
confidence: confirmed
updated: 2026-08-02
sources:
  - .agents/plugins/marketplace.json
  - .claude-plugin/marketplace.json
  - plugins/projipsa/.codex-plugin/plugin.json
  - plugins/projipsa/.claude-plugin/plugin.json
  - scripts/validate_package.py
related:
  - project.current-state
  - project.overview
  - decision.plugin-ship-boundary.2026-07-30
supersedes: []
superseded_by: []
---

# Separate host adapters inside one shipped plugin

## Decision

Projipsa remains one shipped plugin under `plugins/projipsa/`, but Codex and
Claude Code use separate thin Skill adapters:

- `.agents/plugins/marketplace.json` is the Codex development marketplace;
  `.claude-plugin/marketplace.json` remains the Claude Code marketplace.
- `skills/` is the Codex entry point and contains Codex metadata plus the
  canonical resources used by the shared workflows.
- `claude-skills/` is the Claude Code entry point and contains Claude-only
  frontmatter.
- `shared/` contains the host-neutral workflow body for each public Skill.

Both manifests expose the same three public Skill names. The package validator
checks the two adapters and their loading policies independently.

## Context

The original layout made both hosts read the same `SKILL.md`. That kept prose
identical, but also exposed Claude Code's `disable-model-invocation` key to the
Codex package surface. A first separation attempt moved Codex adapters to
`codex-skills/`; the official Codex plugin validator rejected that because its
Skill entry point must resolve to `skills/`.

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

## Reasoning

- Thin adapters isolate the host-specific invocation contract while preserving
  one canonical workflow body.
- Keeping Codex at the standard `skills/` path satisfies its authoritative
  plugin validator.
- Claude Code accepts the manifest-declared `claude-skills/` path, so it does
  not need to scan or load the Codex adapters.
- One plugin root preserves the existing cache and ship boundary and avoids
  duplicated resource trees that could drift.

## Consequences

- A Skill change may affect a shared workflow, one host adapter, or both; the
  validator must distinguish those surfaces.
- Codex documentation, default prompts, and adapter metadata must use
  `$projipsa:projipsa`, `$projipsa:projipsa-init`, and
  `$projipsa:outsource`; Claude Code keeps `/projipsa:<skill>`.
- Codex and Claude Code validation must both pass before release.
- Installing one host still copies the complete plugin root, but only that
  host's manifest-selected adapters are exposed as Skills.
