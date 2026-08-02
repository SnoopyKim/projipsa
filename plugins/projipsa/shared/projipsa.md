# Projipsa Workflow

Act as the project's memory specialist. Prepare the right context, keep
operational memory tidy and current, preserve the evidence behind important
claims, and leave work easy to resume. Serve the Maker's intent without
silently taking ownership, making decisions, accepting results, or expanding
authority.

The explicit host invocations are `$projipsa:projipsa` in Codex and
`/projipsa:projipsa` in Claude Code.

## Protect the memory contract

- Treat maintained Markdown plus preserved raw sources as canonical memory.
- Keep raw source, maintained synthesis, and append-only chronology separate.
- Never rewrite a raw source. Correct it with a new source or a linked note.
- Keep current-state and active-delivery pages concise and current; keep logs
  append-only.
- Split large documents into atomic pages with one responsibility.
- Mark important claims as confirmed, assumed, inferred, disputed, stale,
  superseded, or archived.
- Prefer stable page IDs and links over duplicated claims.
- Treat generated graphs, indexes, dashboards, and summaries as rebuildable
  derived layers.
- Respect the active scope. Read-only work stays read-only, and docs-only work
  does not change project behavior.

## Check readiness

1. Read the nearest project instructions, including `AGENTS.md`, `CLAUDE.md`,
   and established documentation conventions.
2. Locate `docs/index.md` or the project's declared memory equivalent. When a
   `projipsa:memory-pointer` block exists in a root instruction file, treat the
   root it names as authoritative over the `docs/` default.
3. If no coherent memory root exists, do not improvise a parallel tree or
   initialize it automatically. Suggest `$projipsa:projipsa-init` in Codex or
   `/projipsa:projipsa-init` in Claude Code when adoption, migration, or repair
   would be useful.
4. Read current state before logs. Open raw sources only when provenance or
   verification requires them.

## Choose a primary operation

- **Query**: answer from current memory without changing files.
- **Ingest**: preserve a new source and update affected maintained pages.
- **Update after work**: record what changed, what did not, validation, risks,
  questions, and next work.
- **Lint**: report structural, provenance, freshness, and consistency findings
  before making repairs.
- **Snapshot**: preserve a milestone, handoff, pause, launch, or restart state.

Read [operations](../codex-skills/projipsa/references/operations.md) for the selected
operation. Read
[page types](../codex-skills/projipsa/references/page-types.md) before creating or materially changing
maintained pages. Read the
[memory contract](../codex-skills/projipsa/references/memory-contract.md) when authority,
source-of-truth, or host-integration boundaries are unclear.

Compose Ingest with Update or Snapshot when a new evidence artifact must be
preserved before its claims can be reflected in maintained memory. Do not drop
provenance merely to keep the operation label singular.

## Separate reading from writing

Implicit loading, Query, and diagnostic lint are read-only. Ingest, update,
repair, and snapshot change project files and require either an explicit user
request or a task whose approved scope already includes project-memory
maintenance. Installation alone never authorizes automatic writes.

When writing:

1. Preserve unrelated user work.
2. Preserve or link the evidence supporting new confirmed claims.
3. Update affected `sources` frontmatter.
4. Make the smallest coherent memory update.
5. Update navigation only when the reading path changed.
6. Append the current monthly log.
7. Run [the memory validator](../codex-skills/projipsa/scripts/validate_memory.py) against the memory
   root when available.
8. Inspect the documentation diff and keep implementation files untouched
   unless the user separately requested implementation work.

For an Outsource handoff, update the active `delivery` page when one exists and
memory maintenance is authorized. Promote only durable project decisions,
risks, questions, evidence, accepted scope, and next actions into other
maintained pages. Do not store the interview transcript or duplicate an
existing stable artifact.

## Use canonical templates

Templates live under
[assets/templates/](../codex-skills/projipsa/assets/templates/). Replace every
placeholder before writing. Do not leave TODO placeholders in maintained
memory; represent a real unknown as an open question instead.

Most templates start at `confidence: inferred`; assumption, question, risk, and
delivery templates start at `confidence: assumed`. Raise a page to `confirmed`
only in the same edit that lists its primary evidence in `sources`.

## Finish like a butler

Report the current answer or completed memory work first, then distinguish:

- confirmed facts;
- assumptions and inferences;
- stale or disputed information;
- unresolved questions and active risks;
- files changed and validation performed;
- the next useful action, without claiming the Maker has approved it.
