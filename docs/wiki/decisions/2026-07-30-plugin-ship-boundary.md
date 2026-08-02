---
id: decision.plugin-ship-boundary.2026-07-30
type: decision
status: active
confidence: confirmed
updated: 2026-07-31
sources:
  - https://github.com/SnoopyKim/projipsa/pull/2
  - scripts/validate_package.py
related:
  - project.overview
  - decision.projipsa-adoption.2026-07-31
  - decision.host-adapter-separation.2026-08-02
supersedes: []
superseded_by: []
---

# Shipped content lives under plugins/projipsa

## Decision

Only `plugins/projipsa/` holds shipped content. The repository root holds
everything else, and `scripts/validate_package.py` scans the shipped tree plus
the repository README, nothing more.

## Context

Installing a plugin copies its plugin root into a local cache, and Claude Code
has no ignore mechanism for that copy. With the repository root as the plugin
root, tests, CI, and any memory tree this repository adopted would all ship.
The same conflation made the package validator walk the whole repository, so
documentation content could fail package validation.

## Alternatives Considered

- Keep the repository root as the plugin root and add exclusions to the
  validator.
- Keep the repository root as the plugin root and narrow the exposed set with
  `strict: false` plus an explicit `skills` list in the marketplace entry.

## Reasoning

- An exclusion list is maintained by hand and silently admits anything added
  later. A directory boundary answers the question structurally.
- `strict` controls which components load, not which files are copied, so the
  marketplace allowlist would not have stopped the cache copy.
- The layout matches `anthropics/claude-code`, which uses
  `"source": "./plugins/agent-sdk-dev"` in its own repository, and matches
  `SnoopyKim/Outsource`, which already used `plugins/<name>/`.

## Consequences

- The plugin root for local development is `./plugins/projipsa`, not the
  repository root.
- A marketplace listing must point at the subdirectory, not the repository.
- This memory tree can live at `docs/` without shipping and without gating
  package validation.
