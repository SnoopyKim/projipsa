# Root Instruction Pointer

Maintain this block in the project's root `AGENTS.md` and root `CLAUDE.md` so
every host finds the memory root without being told. Replace `docs` with the
selected memory root. On a later run, replace the existing block in place and
never append a second copy.

## Pointer block

```markdown
<!-- projipsa:memory-pointer -->
## Project memory

This project keeps operating memory under `docs/`, maintained with Projipsa.

- Read `docs/index.md` first, then `docs/wiki/project/current-state.md`.
- Treat `docs/wiki/**` as maintained synthesis, `docs/raw/**` as preserved
  source material that is never rewritten, and `docs/logs/**` as append-only
  chronology rather than current truth.
- Full memory rules: `docs/AGENTS.md`.
<!-- /projipsa:memory-pointer -->
```

## New root CLAUDE.md

Claude Code does not read `AGENTS.md`. When the project has no `CLAUDE.md`,
create one that imports the file both hosts should share:

```markdown
# Project Instructions

@AGENTS.md
```

## Existing root CLAUDE.md

When `CLAUDE.md` already exists, do not inject an import that would duplicate
curated instructions. Add the pointer block itself, preserving every surrounding
line the Maker wrote.
