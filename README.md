# Projipsa

> A project butler for memory, coordination, and delegated delivery.

Projipsa helps Codex and Claude Code understand an existing project, keep its
operating context current, coordinate the next work, and manage substantial
explicitly delegated work through verified review and handoff.

It is one Plugin and one portable Skill entry point with four focused modes:

```text
projipsa
├── default           front-door routing and consolidated reporting
├── init              existing-project onboarding and repair
├── memory            source-backed project memory
└── outsource         explicitly delegated substantial delivery
```

The public Skill lives under `skills/projipsa/`; canonical mode procedures live
under `capabilities/` and are loaded only when the router selects that mode.
Using one public entry point prevents Codex and Claude Code from applying
different automatic-invocation rules to overlapping specialist entry points.

Invoke the same capability with each host's native syntax:

| Capability | Codex | Claude Code Plugin |
| --- | --- | --- |
| Main project butler | `$projipsa` | `/projipsa:projipsa` |
| Project onboarding | `$projipsa init` | `/projipsa:projipsa init` |
| Project memory | `$projipsa memory` | `/projipsa:projipsa memory` |
| Delegated delivery | `$projipsa outsource` | `/projipsa:projipsa outsource` |

Projipsa serves the project without silently taking authority from its Maker.
It may prepare context, recommend a route, preserve evidence, and surface
decisions. It never treats a recommendation as approval or a passing check as
Maker acceptance.

## How the modes work together

### `$projipsa`

Use the main Skill when you want one project-butler entry point. It:

- reads project instructions and current context;
- briefs current state and meaningful unknowns;
- routes onboarding to `init`;
- routes project-memory work to `memory`;
- routes explicitly delegated substantial work to `outsource`;
- leaves ordinary domain work in the host's normal specialist workflow;
- returns one consolidated project report.

Projipsa may recommend Outsource mode, but it does not begin a Deep Interview or
Delivery Contract solely because a task is complex.

### `$projipsa init`

Use the initialization mode once when onboarding an existing project. It:

- inventories current instructions and documentation;
- selects `docs/` or an established durable equivalent as the memory root;
- creates the minimum useful project-memory core;
- reorganizes existing docs without changing project behavior;
- preserves raw sources and chronology;
- records the adoption decision and validates the result.

Initialization is idempotent. A later run audits and repairs the existing setup
instead of creating a second memory tree.

### `$projipsa memory`

Use the memory mode after a project has adopted Projipsa. It supports:

- querying project context without writing;
- ingesting source material with provenance;
- updating current state, decisions, risks, questions, and next work;
- linting structure, freshness, links, and evidence;
- creating milestone, pause, handoff, and restart snapshots;
- persisting authorized Outsource delivery state.

Maintained Markdown and preserved source material are the canonical memory
layer. Search indexes, graphs, dashboards, and summaries remain optional
derived layers.

### `$projipsa outsource`

Use Outsource only when the Maker explicitly delegates substantial work. It:

- routes ordinary work out and qualifies Scoped or Project engagement weight;
- runs an adaptive Deep Interview for consequential uncertainty;
- proposes and versions a Delivery Contract;
- selects direct, sequential, parallel, graph, or human-gated execution;
- separates executed, verified, and Maker-accepted outcomes;
- manages feedback, change, pause, review, acceptance, and handoff;
- hands durable outcomes back to project memory when authorized.

Project-mode delivery uses a maintained Projipsa `delivery` page when memory
writes are authorized. It does not create a competing long-lived state system.

## Shared project-memory layout

The universal core is:

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

Add optional page families only when the project needs them:

```text
wiki/areas/
wiki/assumptions/
wiki/risks/
wiki/procedures/
wiki/external/
wiki/milestones/
wiki/deliveries/
```

Each active Project-mode Outsource engagement may use one maintained
`wiki/deliveries/<slug>.md` page for its current contract, outer state,
evidence, Maker review, and exact next action. Durable decisions, risks,
questions, sources, and milestones stay in their own canonical pages and are
linked rather than duplicated.

## Authority and privacy

- Read-only work remains read-only.
- Docs-only work does not change project behavior.
- Installation grants no additional runtime permissions.
- External, costly, sensitive, and hard-to-reverse actions remain separately
  gated by the Maker and host.
- Secrets stay in an approved secret store.
- Project memory does not automatically become a reusable Maker preference.
- Private Maker strategy and raw customer data are not promoted into reusable
  Plugin protocol.
- Projipsa source changes require an inspectable diff and authorization.

Projipsa requires no environment variables, database, background daemon, MCP
server, or hosted state service. It uses the filesystem and host capabilities
already available to Codex or Claude Code.

## Development validation

The bundled validators require Python 3.9 or newer and otherwise use only the
standard library.

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests
```

Validate the public Skill with the host skill validator and validate the Plugin
with the Codex and Claude Code plugin validators before publishing.

## v0.1 invocation migration

Version 0.2 intentionally replaces the separate `$projipsa-init`,
`$projipsa-memory`, and `$outsource` entry points with `$projipsa init`,
`$projipsa memory`, and `$projipsa outsource`. Claude Code uses the same mode
names after `/projipsa:projipsa`.

Projipsa does not ship legacy alias Skills because Claude Code would discover
those aliases as additional model-invocable entry points, recreating the
routing overlap this version removes.

## Distribution

The public source is
[`SnoopyKim/projipsa`](https://github.com/SnoopyKim/projipsa). Publication
through the SnoopyDev marketplace is a separate release step; marketplace
manifests should pin a reviewed commit SHA.

For a source checkout, Claude Code can load the Plugin directly during
development with `claude --plugin-dir /path/to/projipsa`. Codex installation
should use the reviewed marketplace entry once that separate publication step
is complete.

The `outsource` mode was integrated from
[`SnoopyKim/Outsource`](https://github.com/SnoopyKim/Outsource) at commit
`c4a5292e9579b67ecf6eda74558a9785f6305c77`. That repository may remain as a
temporary compatibility and migration surface, but Projipsa is the intended
canonical home for the integrated capability.

## License

MIT
