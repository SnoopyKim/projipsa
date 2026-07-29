# Projipsa

> A project butler for durable, source-backed project memory.

Projipsa helps Codex and Claude Code understand an existing project, keep its
operating context current, and leave it ready to resume. It treats maintained
Markdown and preserved source material as the canonical memory layer. Search
indexes, graphs, dashboards, and summaries remain optional derived layers.

Projipsa serves the project without silently taking authority from its Maker.
It prepares relevant context, remembers decisions, notices stale assumptions,
keeps evidence close to claims, and makes unfinished work explicit.

## Skills

### `projipsa`

Use the primary skill after a project has adopted Projipsa. It supports:

- querying project memory;
- ingesting source material;
- updating memory after work;
- linting structure and freshness;
- creating milestone and handoff snapshots.

Read-only operations may inspect memory when relevant. Mutating operations run
only when the user requested memory maintenance or the active task explicitly
includes documentation updates.

### `projipsa-init`

Use the initialization skill once when onboarding an existing project. It:

- inventories current project instructions and documentation;
- selects `docs/` or an established equivalent as the memory root;
- creates the minimum useful project-memory core;
- reorganizes existing docs without changing project behavior;
- preserves raw sources and chronology;
- records the adoption decision and validates the result.

Initialization is idempotent. Running it again audits and repairs an incomplete
setup instead of creating a second memory tree.

## Default project layout

```text
docs/
  AGENTS.md
  index.md
  raw/YYYY-MM/
  wiki/project/
  wiki/decisions/
  wiki/questions/
  logs/YYYY-MM.md
```

Optional page families are added only when the project needs them.

## Development validation

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests
```

Validate each skill with the host's skill validator and validate the plugin
with the Codex and Claude Code plugin validators before publishing.

## Distribution

The public source is `SnoopyKim/projipsa`. Publication through the
SnoopyDev marketplace is a separate release step; marketplace manifests should
pin a reviewed commit SHA.

## License

MIT
