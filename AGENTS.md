# Project Instructions

Projipsa is a Claude Code plugin. Only `plugins/projipsa/` is shipped to users;
everything else in this repository stays here. See [the ship boundary
decision](docs/wiki/decisions/2026-07-30-plugin-ship-boundary.md) and [the host
scope decision](docs/wiki/decisions/2026-07-31-claude-code-only.md).

<!-- projipsa:memory-pointer -->
## Project memory

This project keeps operating memory under `docs/`, maintained with Projipsa.

- Read `docs/index.md` first, then `docs/wiki/project/current-state.md`.
- Treat `docs/wiki/**` as maintained synthesis, `docs/raw/**` as preserved
  source material that is never rewritten, and `docs/logs/**` as append-only
  chronology rather than current truth.
- This memory root is public. Full memory rules: `docs/AGENTS.md`.
<!-- /projipsa:memory-pointer -->
