# Projipsa

> A project butler for durable, source-backed project understanding.

Projipsa helps an agent recover the project's context, understand why decisions
were made, and leave useful knowledge for the next session. It maintains
readable Markdown: evidence stays traceable, current understanding gets
reconciled, and history remains available.

The name is `project` + `집사` (*jipsa*), Korean for butler. Its responsibility
is the project's memory: decisions, constraints, findings, observed outcomes,
open questions, and continuity across people, sessions, and agent hosts.
The host agent handles implementation and execution.

## Install

This source package is version `0.6.0` and is **not listed in a
public marketplace yet**. Published versions are on the
[releases page](https://github.com/SnoopyKim/projipsa/releases).
Install it from a source checkout:

```bash
git clone https://github.com/SnoopyKim/projipsa
```

Claude Code:

```bash
claude plugin marketplace add /path/to/projipsa
claude plugin install projipsa@projipsa
```

Codex:

```bash
codex plugin marketplace add /path/to/projipsa
codex plugin add projipsa@projipsa
```

Grok Build automatically discovers an enabled Claude Code installation through
its official compatibility layer, so do not install a second copy when you use
both hosts. For a Grok-only local installation instead:

```bash
grok plugin install /path/to/projipsa/plugins/projipsa --trust
grok plugin enable projipsa
```

Restart Claude Code, or start a new Codex or Grok task, after installing.

The installed copy is version-pinned rather than a live reference, so a later
edit under `plugins/projipsa/` reaches it only after a version bump plus the
host's install refresh. To load the working tree for a single Claude Code
session instead:

```bash
claude --plugin-dir /path/to/projipsa/plugins/projipsa
```

Projipsa requires no environment variables, database, background daemon, MCP
server, or hosted state service. It uses the filesystem and the host
capabilities you already have.

## Your first five minutes

Open an existing project and run onboarding explicitly — `/projipsa:projipsa-init`
in Claude Code or Grok Build, or `$projipsa:projipsa-init` in Codex.

It inventories what documentation you already have, picks `docs/` (or an
established durable equivalent) as the memory root, and writes the minimum
useful core:

```text
docs/
  AGENTS.md                              how this project's memory works
  index.md                               the reading entry point
  wiki/project/current-state.md          what is true right now
  wiki/decisions/YYYY-MM-DD-projipsa-adoption.md
  logs/YYYY-MM.md
```

An overview page and an open-questions page get added when the project has
something verified to put in them, rather than on day one.

It also adds a short pointer block to your root `AGENTS.md` and `CLAUDE.md` so
the next agent — on any supported host — finds the memory without being told.

Initialization is docs-only by default: it changes no implementation file. It
can resume an interrupted first adoption without creating a second tree. Once
the adoption marker exists, Init stops; ongoing repair belongs to the everyday
Project memory Skill.

### Upgrading an existing project

Updating the Plugin does not rewrite project memory. Run
`$projipsa:projipsa` in Codex or `/projipsa:projipsa` in Claude Code or Grok
Build when you want an already adopted project linted, repaired, or upgraded to
the current contract. Init is reserved for first adoption, including migration
of general project documentation into Projipsa.

Upgrades remain preservation-first: optional pages and frontmatter stay valid,
stable IDs and working paths remain in place, and monthly logs remain unless
real concurrent writers justify a dated cutover. Repair merges earned contract
changes into project-specific `docs/AGENTS.md` rules rather than replacing
customized documentation from a template.

From then on, `/projipsa:projipsa` is the everyday call. Ask it to brief you,
and it reads current state before history. Ask it to record a session, and it
updates the affected pages and appends the log.

## The three Skills

One Plugin, three Skills with deliberately different trigger boundaries:

| Skill | Codex | Claude Code | Grok Build | Loads automatically |
| --- | --- | --- | --- | --- |
| Project memory | `$projipsa:projipsa` | `/projipsa:projipsa` | `/projipsa:projipsa` | Yes — read-only context work |
| First adoption | `$projipsa:projipsa-init` | `/projipsa:projipsa-init` | `/projipsa:projipsa-init` | No |
| Memory compaction | `$projipsa:compact` | `/projipsa:compact` | `/projipsa:compact` | No |

**Automatic loading is not authority.** It helps the host notice the right
workflow. It does not authorize writes, external effects, costs, deployment,
publication, or acceptance.

In Codex the plugin namespace is part of the invocation: the colon in
`$projipsa:projipsa-init` is real, and the shorter `$projipsa-init` selects a
different Skill.

### Project memory

The everyday Skill once a project has adopted Projipsa. It can:

- answer questions from current memory without writing anything;
- ingest new source material with its provenance;
- update current state, decisions, risks, questions, and next work;
- integrate shared memory once parallel writer branches have merged;
- lint and repair structure, freshness, links, evidence, and contract drift;
- capture a milestone, pause, handoff, or restart snapshot;
- preserve findings, outcome evidence, and resumable project context.
- trace source dependencies and related decisions, detect evidence changes,
  and prepare bounded task briefings or relationship diagrams.

It may load implicitly when you ask for a project briefing, but implicit use
stays read-only. Ingest, Update, Integrate, Repair, and Snapshot need either an
explicit request or a task whose approved scope already covers memory
maintenance.

If no coherent memory exists, it says so and may suggest onboarding. It never
initializes a project on its own.

### Related context and changed evidence

Ask Projipsa to brief a task, find records affected by a source change, or draw
the relationships around a decision. The bundled Python helper reads existing
Markdown and frontmatter; it needs no server, graph database, or external API:

```bash
python3 plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py docs brief --query "release policy"
python3 plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py docs brief --source README.md
python3 plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py docs graph --page project.current-state --format mermaid
python3 plugins/projipsa/codex-skills/projipsa/scripts/memory_context.py docs review
```

These commands are read-only. Briefings retain source paths, supersession and
historical labels, and review status. They use lexical matching and explicit
relations; read the original when excerpts are incomplete.

After reviewing evidence in an authorized memory update, Projipsa can checkpoint
the specific pages in `docs/.projipsa/evidence-baseline.json`. Later byte or
citation changes create review candidates without invalidating conclusions.
No checkpoint means unknown freshness. External URL contents are not fetched.
See [context and evidence](plugins/projipsa/codex-skills/projipsa/references/context-and-evidence.md)
for commands, budgets, and the checkpoint contract.

### First adoption

Explicit and infrequent. Covered in [your first five minutes](#your-first-five-minutes)
above. It creates a new memory root or adopts existing general documentation.
It never loads merely because memory would be useful, and it does not repair an
already adopted root.

### Memory compaction

Also explicit and infrequent. `$projipsa:compact` in Codex and
`/projipsa:compact` in Claude Code or Grok Build first run a read-only Audit:
file and byte inventory, exact image hashes, local references, Git
recoverability, and conservative groups that need semantic or visual review.

Audit is not deletion approval. Compact produces an exact path plan, protects
the only evidence for an active claim, and requires separate explicit approval
before Apply. Unmodified tracked files are tied to a Git baseline; modified or
untracked files require a separate recovery path or acknowledged unrecoverable
deletion. Removing working-tree files does not shrink existing Git history.

### Moving from 0.5.0

`outsource` is no longer included. Projipsa concentrates on project memory;
execution strategy, work orchestration, and acceptance stay with the host and
user. Existing delivery pages remain valid project records. Updating the plugin
never deletes them or rewrites adopter memory. Use a milestone or an existing
task artifact for new handoffs.

## What the memory looks like

Four roles, with different authority. The default folders implement them, but a
project records its own mapping and visual-asset policy in `docs/AGENTS.md`:

| Role | Default | Holds | Rule |
| --- | --- | --- | --- |
| Evidence | `raw/` or stable links | material needed to verify claims | retain durable, unique evidence; link stable artifacts instead of copying |
| Events | `logs/` | append-only chronology | never current truth |
| Synthesis | `wiki/` | maintained project understanding | the project-level source of current truth |
| Views | derived assets | search, graphs, dashboards, summaries | rebuildable; never the only home for a fact |

Normal memory maintenance never overwrites or deletes retained raw evidence.
The explicit Compact workflow can remove a whole artifact only after an active
evidence check, exact path plan, recoverability review, and approval. Temporary,
intermediate, or readily reproducible captures should not enter memory in the
first place.

The universal core:

```text
docs/
  AGENTS.md
  index.md
  wiki/project/current-state.md
  wiki/decisions/
  logs/YYYY-MM.md
```

`raw/YYYY-MM/`, `wiki/project/overview.md`, and `wiki/questions/` join it when
the project has real source material, a purpose worth stating apart from its
current state, or genuine unknowns.

Chronology defaults to one file per month. A project whose work runs in
parallel branches or worktrees switches to one file per writer
(`logs/2026-08/2026-08-12-<slug>.md`), because a shared append target is a
merge-conflict target. Those branches leave the shared pages alone; asking
Projipsa to finish after the merge writes them once from the merged result. The
memory validator reports newer per-writer chronology, while Projipsa checks that
the current branch actually holds the merge before running Integrate.

Optional page families get added only when a project actually needs them —
`wiki/areas/`, `assumptions/`, `risks/`, `procedures/`, `external/`,
`milestones/`. Existing custom page families remain valid. Empty folders for
symmetry are a smell.

Every maintained page carries frontmatter with a stable `id`, an `updated` date,
and a `sources` list. `status` defaults to `active` and `confidence` defaults to
`inferred`; state either when the page departs from that default. A page is
raised to `confirmed` only in the same edit that lists its evidence. Six months
later you can still ask whether a claim was verified or guessed — and get an
answer.

## Make memory useful in everyday work

Before meaningful work, retrieve the relevant decisions, constraints, earlier
failures, and open questions. Start with short context and follow links when
needed. Check changing facts against the current checkout or live source.

After work, preserve what changes the next session's understanding: a decision
and its reason, a verified finding, an unsuccessful approach and its conditions,
a correction, or a next action. Reconcile existing pages before adding another.
Observed outcomes can refine earlier decisions without erasing their history.

A project may explicitly authorize routine post-work memory maintenance in its
instructions. Projipsa honors that established scope without asking again.
Installation itself grants no write scope. This package has no background
capture hook, daemon, or automatic session recorder; its operations are carried
out by the host agent.

## Cross-host discovery

A memory root only helps if the next agent opens it, and the two hosts read
different files. Codex reads `AGENTS.md`. Claude Code reads `CLAUDE.md` and does
not read `AGENTS.md` at all.

So initialization maintains one marked block in the project's root instruction
files:

```text
<!-- projipsa:memory-pointer -->
names the memory root, the reading entry point, the layer rules,
and where the full memory rules live
<!-- /projipsa:memory-pointer -->
```

Root `AGENTS.md` carries the block. Root `CLAUDE.md` is created as an
`@AGENTS.md` import when it does not exist, or receives the same block when it
already exists and should not be disturbed. A later run replaces that block in
place instead of appending a second copy.

## Authority and privacy

- Read-only work stays read-only.
- Docs-only work does not change project behavior.
- Initialization touches root `AGENTS.md` and root `CLAUDE.md`, reports both
  paths, and changes no implementation file.
- Installation grants no additional runtime permissions.
- Automatic Skill loading is neither delegation nor consent.
- External, costly, sensitive, and hard-to-reverse actions stay separately gated
  by you and the host.
- Secrets stay in an approved secret store.
- Project memory does not silently become a reusable personal preference.
- Private strategy and raw customer data are not promoted into reusable Plugin
  protocol.
- Changes to Projipsa itself require an inspectable diff and authorization.

## Background

Projipsa's memory layer follows the LLM-wiki pattern — an agent incrementally
maintaining a synthesized Markdown wiki over retained evidence, so understanding
compounds instead of being rediscovered per query. See
[Karpathy's llm-wiki sketch](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
and [LangChain's write-up of wiki memory](https://www.langchain.com/blog/wiki-memory).
Projipsa adds append-only chronology, explicit confidence and provenance, and a
cross-host discovery pointer.

The [September 2026 source review](docs/wiki/areas/project-memory-references.md)
records further design references and the distinction between adopted workflow
changes and proposed infrastructure. It is repository research, outside the
shipped plugin.

## Contributing

Repository layout, the validators, and the packaging invariants live in
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
