# Projipsa

> A project butler for memory, onboarding, and substantial delivery.

Projipsa helps Codex and Claude Code understand an existing project, keep its
operating context current, and manage substantial work through verified review
and handoff.

It is one Plugin containing three portable Skills with deliberately different
trigger boundaries:

```text
projipsa
├── projipsa         frequent project-memory work
├── projipsa-init    explicit, infrequent onboarding and repair
└── outsource        substantial or long-running delivery
```

| Skill | Codex | Claude Code Plugin | Automatic loading |
| --- | --- | --- | --- |
| Project memory | `$projipsa:projipsa` | `/projipsa:projipsa` | Yes, read-only context work |
| Project onboarding | `$projipsa:projipsa-init` | `/projipsa:projipsa-init` | No |
| Substantial delivery | `$projipsa:outsource` | `/projipsa:outsource` | Yes, qualification only |

Automatic loading is not additional authority. It helps the host notice the
right workflow, but does not authorize writes, external effects, costs,
deployment, publication, acceptance, or other actions outside the user's
request and host approvals.

Each host enforces that loading policy with its own thin adapter instead of
sharing incompatible harness metadata. Codex uses
`allow_implicit_invocation` in
`plugins/projipsa/skills/<name>/agents/openai.yaml`; Claude Code uses
`disable-model-invocation` in
`plugins/projipsa/claude-skills/<name>/SKILL.md`. Both adapters load the same
workflow under `plugins/projipsa/shared/`, and
`scripts/validate_package.py` fails when their policies or public Skill names
drift apart.

Codex qualifies plugin Skills with the plugin namespace. The colon in
`$projipsa:projipsa-init`, for example, is part of the actual invocation; the
shorter `$projipsa-init` text does not select that plugin Skill.

## `$projipsa:projipsa`: project memory

`projipsa` is the everyday Skill after a project has adopted Projipsa. It
supports:

- querying current project context without writing;
- ingesting source material with provenance;
- updating current state, decisions, risks, questions, and next work;
- linting structure, freshness, links, and evidence;
- creating milestone, pause, handoff, and restart snapshots;
- persisting authorized Outsource delivery state.

It may load implicitly for project briefing or memory lookup, but implicit use
remains read-only. Ingest, update, repair, and snapshot require an explicit
request or an already authorized memory-maintenance scope.

If no coherent Projipsa memory exists, the Skill reports that state and may
suggest `$projipsa:projipsa-init` in Codex or `/projipsa:projipsa-init` in
Claude Code; it does not initialize a project automatically.

Maintained Markdown and preserved source material are the canonical memory
layer. Search indexes, graphs, dashboards, and summaries remain optional
derived layers.

## `$projipsa:projipsa-init`: onboarding and repair

`projipsa-init` is an explicit, infrequent workflow for adopting Projipsa in an
existing project. It:

- inventories current instructions and documentation;
- selects `docs/` or an established durable equivalent as the memory root;
- creates the minimum useful project-memory core;
- reorganizes existing docs without changing project behavior;
- preserves raw sources and chronology;
- maintains a marked memory pointer in the project's root instruction files;
- records the adoption decision and validates the result.

Initialization is idempotent. A later run audits and repairs the existing setup
instead of creating a second memory tree. The Skill does not load merely
because memory would be useful, and its default boundary is docs-only.

## `$projipsa:outsource`: substantial delivery

`outsource` is for work that is broad, ambiguous, risky, multi-milestone,
likely to span sessions or handoffs, or likely to benefit from a durable
delivery contract. It:

- qualifies work as Ordinary, Scoped, or Project;
- runs an adaptive Deep Interview for consequential uncertainty;
- proposes and versions a Delivery Contract;
- selects direct, sequential, parallel, graph, or human-gated execution;
- separates executed, verified, and Maker-accepted outcomes;
- manages feedback, change, pause, review, acceptance, and handoff;
- integrates durable outcomes with Projipsa memory when available and
  authorized.

Outsource loads each operating reference when the step it governs is next,
rather than loading all five before the engagement mode is known.

Codex or Claude Code may load `outsource` automatically when a request spans
multiple milestones or sessions, needs a durable delivery contract, or is hard
to reverse. That trigger is deliberately narrower than the range of work
Outsource can handle: a host that loads it for anything broad-sounding spends
the Maker's context on an engagement they never asked for. The automatic load
authorizes only read-only qualification and a recommendation. Before starting a
Deep Interview or treating a Delivery Contract as active, the Maker must opt in.

Explicit `$projipsa:outsource` invocation begins qualification, not blanket
approval for every later write, external effect, cost, deployment, publication,
or acceptance decision.

Outsource works independently when Projipsa memory is absent. Project-mode work
may recommend `$projipsa:projipsa-init` in Codex or
`/projipsa:projipsa-init` in Claude Code rather than creating a competing
long-lived state system.

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

## Cross-host discovery

A memory root only helps if the next agent opens it, and the two hosts read
different instruction files. Codex reads `AGENTS.md`. Claude Code reads
`CLAUDE.md` and does not read `AGENTS.md` at all. Initialization therefore
maintains one marked block in the project's root instruction files:

```text
<!-- projipsa:memory-pointer -->
names the memory root, the reading entry point, the layer rules,
and where the full memory rules live
<!-- /projipsa:memory-pointer -->
```

Root `AGENTS.md` carries the block. Root `CLAUDE.md` is created as an
`@AGENTS.md` import when it does not exist, or receives the same block when it
already exists and should not be disturbed. A later initialization run replaces
the block in place rather than appending a second copy.

`plugins/projipsa/skills/projipsa/scripts/validate_memory.py` enforces all of
that: it fails on a
missing instruction file, a missing block, a second appended block, and a block
that names a different root than the one being validated.

## Authority and privacy

- Read-only work remains read-only.
- Docs-only work does not change project behavior.
- Initialization maintains a marked pointer block in root `AGENTS.md` and root
  `CLAUDE.md`, and reports both paths. It changes no implementation file.
- Installation grants no additional runtime permissions.
- Automatic Skill loading is not delegation or consent.
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

## Repository layout

Installing the Plugin copies its plugin root into a local cache, and Claude Code
has no ignore mechanism for that copy. The ship boundary is therefore a
directory boundary:

```text
plugins/projipsa/                 shipped plugin root
  .codex-plugin/                  Codex manifest
  .claude-plugin/                 Claude Code manifest
  skills/                         Codex adapters and shared resources
  claude-skills/                  Claude Code adapters
  shared/                         host-neutral workflow bodies
docs/                 this project's own Projipsa memory
scripts/  tests/      validators and their tests
.github/              CI
```

`scripts/validate_package.py` scans the shipped tree and this README, nothing
else. Everything under `docs/` belongs to the memory validator instead, so this
project can adopt Projipsa on itself without its notes gating package
validation, and without shipping those notes to everyone who installs the
Plugin.

## Development validation

The bundled validators require Python 3.9 or newer and otherwise use only the
standard library.

```bash
python3 scripts/validate_package.py
python3 -m unittest discover -s tests
claude plugin validate ./plugins/projipsa --strict
```

`scripts/validate_package.py` checks cross-host alignment: shared manifest
fields, matching loading policies, documented invocations for both hosts, and
the guardrails each Skill contract must keep. `tests/test_memory_fixture.py`
builds the minimum useful core from the shipped templates and requires the
shipped memory validator to accept it, so a template cannot drift out of
contract with its own validator. GitHub Actions runs both on Python 3.9 and
3.13.

Validate all three public Skills with the host skill validator and validate the
Plugin with the Codex plugin validator before publishing.

## v0.3 invocation migration

Version 0.3 replaces the v0.2 router modes with three independent Skills:

| v0.2 | v0.3 |
| --- | --- |
| `$projipsa memory` | `$projipsa:projipsa` |
| `$projipsa init` | `$projipsa:projipsa-init` |
| `$projipsa outsource` | `$projipsa:outsource` |
| `/projipsa:projipsa memory` | `/projipsa:projipsa` |
| `/projipsa:projipsa init` | `/projipsa:projipsa-init` |
| `/projipsa:projipsa outsource` | `/projipsa:outsource` |

The split keeps the frequent memory workflow short and broadly useful, keeps
one-time initialization out of implicit routing, and lets hosts notice when
Outsource fits without mistaking that notice for Maker delegation.

## Install from the SnoopyDev marketplace

Codex:

```bash
codex plugin marketplace add SnoopyKim/marketplace --ref main
codex plugin add projipsa@snoopydev
```

Claude Code:

```bash
claude plugin marketplace add SnoopyKim/marketplace
claude plugin install projipsa@snoopydev
```

Start a new Codex task or restart Claude Code after installation. The public
source is [`SnoopyKim/projipsa`](https://github.com/SnoopyKim/projipsa), and
the marketplace pins a reviewed source commit at the plugin root
`plugins/projipsa`.

The marketplace entry is not published yet, so until it is, install a source
checkout through this repository's own marketplace manifest.

Codex:

```bash
codex plugin marketplace add /path/to/projipsa
codex plugin add projipsa@projipsa
```

Claude Code:

```bash
claude plugin marketplace add /path/to/projipsa
claude plugin install projipsa@projipsa
```

The installed copy is version-pinned, so a later edit under
`plugins/projipsa/` requires the host's marketplace/install refresh. Published
releases must bump the plugin version. To load the working tree for one Claude
Code session instead, use
`claude --plugin-dir /path/to/projipsa/plugins/projipsa`.

The `outsource` Skill was integrated from
[`SnoopyKim/Outsource`](https://github.com/SnoopyKim/Outsource) at commit
`c4a5292e9579b67ecf6eda74558a9785f6305c77`. That repository may remain as a
temporary compatibility and migration surface, but Projipsa is the intended
canonical home for the integrated capability.

## License

MIT
