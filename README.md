# Projipsa

> A project butler: durable project memory, and substantial work you can
> delegate on top of it.

An agent rebuilds its understanding of your project at the start of every
session and throws it away at the end. You pay that cost again next time — and
worse, you cannot hand the agent anything long. Work that spans sessions has
nothing to resume from.

Projipsa keeps the project's understanding in Markdown that an agent maintains:
evidence preserved, current synthesis kept current, chronology appended. Because
that memory outlives the session, you can then delegate substantial work against
it — with a contract, verification, and an acceptance step that stays yours.

Those are not two features. **The memory is the shared state the delegated work
runs on.** Agent frameworks keep such state inside the process, so it dies with
the run. Projipsa keeps it in Git, so it survives sessions, hosts, and people.

The name is `project` + `집사` (*jipsa*), Korean for butler. A butler prepares,
remembers, and recommends. A butler does not decide, approve, or accept on your
behalf. That distinction is the whole authority model, and it is enforced
throughout.

## Install

Projipsa is version `0.4.0` and is **not listed in a public marketplace yet**.
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

Restart Claude Code, or start a new Codex task, after installing.

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
in Claude Code, or `$projipsa:projipsa-init` in Codex.

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
the next agent — on either host — finds the memory without being told.

Initialization is docs-only by default: it changes no implementation file. It is
also idempotent, so running it again audits and repairs the existing setup
instead of creating a second tree.

### Upgrading an existing project

Updating the Plugin does not rewrite project memory. Run
`$projipsa:projipsa-init` in Codex or `/projipsa:projipsa-init` in Claude Code
explicitly when you want an existing Projipsa project audited or migrated to
the current contract.

The 0.3.x to 0.4.0 upgrade is preservation-first: existing overview and open
questions pages remain valid, as do stated `type`, `status`, `confidence`, and
`related` fields. Monthly logs remain in place unless real concurrent writers
justify a dated cutover to per-writer files. Init merges the new ownership,
eviction, and Integrate guidance into project-specific rules rather than
replacing customized documentation from a template. The first 0.4.0 validation
may report pre-existing findings in nested `logs/**`, which older validators did
not inspect.

From then on, `/projipsa:projipsa` is the everyday call. Ask it to brief you,
and it reads current state before history. Ask it to record a session, and it
updates the affected pages and appends the log.

## The three Skills

One Plugin, three Skills with deliberately different trigger boundaries:

| Skill | Codex | Claude Code | Loads automatically |
| --- | --- | --- | --- |
| Project memory | `$projipsa:projipsa` | `/projipsa:projipsa` | Yes — read-only context work |
| Onboarding and repair | `$projipsa:projipsa-init` | `/projipsa:projipsa-init` | No |
| Substantial delivery | `$projipsa:outsource` | `/projipsa:outsource` | Yes — qualification only |

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
- lint structure, freshness, links, and evidence;
- capture a milestone, pause, handoff, or restart snapshot;
- persist delivery state for an authorized engagement.

It may load implicitly when you ask for a project briefing, but implicit use
stays read-only. Ingest, Update, Integrate, repair, and Snapshot need either an
explicit request or a task whose approved scope already covers memory
maintenance.

If no coherent memory exists, it says so and may suggest onboarding. It never
initializes a project on its own.

### Onboarding and repair

Explicit and infrequent. Covered in [your first five minutes](#your-first-five-minutes)
above. It never loads merely because memory would be useful — you have to ask
for it.

### Substantial delivery

For work that is broad, ambiguous, risky, multi-milestone, or likely to span
sessions and handoffs. It:

- qualifies the work as Ordinary, Scoped, or Project;
- runs an adaptive interview for consequential uncertainty;
- proposes and versions a Delivery Contract;
- picks the simplest topology that still verifies — direct, sequential,
  parallel, graph, or human-gated;
- verifies from the service user, artifact consumer, or QA perspective by
  tracing the real user or data path and trying consequential regressions;
- records `direct`, `proxy`, `reported`, and `not_run` evidence without
  promoting a partial path or implementer self-check into a broader passing
  claim;
- separates *executed*, *verified*, and *Maker-accepted* outcomes;
- manages feedback, change, pause, review, acceptance, and handoff;
- writes durable outcomes into Projipsa memory when that is authorized.

More on how it uses memory in [delegating substantial work](#delegating-substantial-work).

A host may load it automatically when a request spans multiple milestones or
sessions, needs a durable contract, or is hard to reverse. That trigger is
deliberately narrower than the range of work Outsource can handle: a host that
fires it for anything broad-sounding spends your context on an engagement you
never asked for. The automatic load buys read-only qualification and a
recommendation — nothing else. Even an explicit invocation begins qualification
rather than granting blanket approval for later writes, costs, or acceptance.

Outsource works when Projipsa memory is absent. For Project-mode work it may
recommend onboarding rather than building a competing state system of its own.

## What the memory looks like

Four layers, with different authority:

| Layer | Holds | Rule |
| --- | --- | --- |
| `raw/` | preserved evidence | never rewritten — correct it with a new source or a linked note |
| `wiki/` | maintained synthesis | the project-level source of current truth |
| `logs/` | append-only chronology | never current truth |
| derived | search, graphs, dashboards | must be rebuildable; never the only home for a fact |

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
`milestones/`, `deliveries/`. Empty folders for symmetry are a smell.

Every maintained page carries frontmatter with a stable `id`, an `updated` date,
and a `sources` list. `status` defaults to `active` and `confidence` defaults to
`inferred`; state either when the page departs from that default. A page is
raised to `confirmed` only in the same edit that lists its evidence. Six months
later you can still ask whether a claim was verified or guessed — and get an
answer.

## Delegating substantial work

Delegated work needs somewhere to keep its state: the current contract, what has
been verified, what the Maker said, and the exact next action. Keep that inside
the process and it vanishes when the run ends.

Projipsa keeps it in the memory tree. Each active Project-mode engagement gets
one maintained `wiki/deliveries/<slug>.md` page holding its contract version,
current stage, milestone, acceptance evidence, feedback, risks, approvals, and
next action. Durable decisions, questions, risks, and milestones stay in their
own canonical pages and are linked, not copied — duplication is how this kind of
state rots.

Three consequences follow, and they are the point:

- **A pause is cheap.** State is on disk, so resuming is reading a file.
- **A handoff is possible.** A different agent, on a different host, on a
  different day, can pick the engagement up.
- **Completion means something.** Executed is not verified, and verified is not
  accepted. The engagement does not end because retries were exhausted or
  because an agent reported success.

If memory writes are not authorized, Outsource returns a compact proposed
handoff instead of quietly creating a second long-lived state tree.

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
maintaining a synthesized Markdown wiki over immutable sources, so understanding
compounds instead of being rediscovered per query. See
[Karpathy's llm-wiki sketch](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
and [LangChain's write-up of wiki memory](https://www.langchain.com/blog/wiki-memory).
Projipsa adds append-only chronology, explicit confidence and provenance, and a
cross-host discovery pointer.

Its delivery layer takes the design vocabulary that grew around agent loops and
multi-node agent graphs — see the
[graph engineering guide](https://www.aibuilderclub.com/blog/graph-engineering-guide-2026)
— and answers the question those leave open: where the shared state lives when
the run is over.

## Contributing

Repository layout, the validators, and the packaging invariants live in
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
