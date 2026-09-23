# Operations

## Query

Use Query to answer a project question without changing files.

1. Read the memory index.
2. Read `wiki/project/current-state.md`.
3. Find directly relevant decisions, constraints, prior failures, and open
   questions using the index, links, and project vocabulary. Search titles or
   short excerpts first; open full pages when relevant. Broaden a thin search
   before concluding that knowledge is missing.
4. Follow linked decisions, questions, assumptions, risks, areas, procedures,
   external dependencies, deliveries, or milestones when relevant.
5. Open raw sources only when a claim needs verification or provenance.
6. Check whether current state contradicts older logs or sources. Verify
   volatile implementation, installation, deployment, or external claims
   against their live source when the task depends on them. State the observed
   date or revision when it changes the claim's meaning.
7. Answer with confirmed facts first, followed by assumptions, stale risks,
   disputed claims, and open questions.

Do not treat a log as current truth when a maintained page or newer decision
supersedes it.

For a task briefing or changed-source impact, use the read-only helper in
[context and evidence](context-and-evidence.md). Follow its excerpts to the
original pages; surface review candidates, supersession, and unchecked external
evidence in the answer. Use its Mermaid view when the user needs a relationship
diagram. Query does not write or refresh evidence checkpoints.

## Ingest

Use Ingest for a new research artifact, meeting note, user feedback,
conversation output, external article, source document, or field observation.

1. Classify the artifact before copying it:
   - link a stable repository path, URL, commit, or durable external record;
   - retain unique, durable evidence under `raw/YYYY-MM/` or the established
     equivalent;
   - place a replaceable current visual in the project's maintained asset area
     when its `docs/AGENTS.md` defines one;
   - do not add temporary, intermediate, or reproducible captures to project
     memory.
2. Preserve retained evidence as closely as practical. Add provenance metadata
   only when it helps identify origin, date, or scope.
3. Identify affected maintained pages. Classify the new evidence as supporting,
   extending, correcting, superseding, or conflicting with existing claims.
   Reconcile the same claim in place; similarity alone does not establish that
   two claims concern the same entity, decision, or conditions.
4. Update existing pages or create focused new pages.
5. Link new or changed claims to the source.
6. Update the index only when navigation changed.
7. Append the chronology log.

Summarize only project impact in maintained pages. Do not make future agents
read large raw sources by default.

## Update after work

Use Update after a work session, planning session, research pass,
meeting, review, or handoff.

1. Establish what actually changed and what explicitly did not.
2. Identify the evidence supporting every new confirmed claim.
3. Retain only durable, unique evidence that future work may need to verify a
   live claim. Link a stable versioned project path instead of copying it, and
   leave temporary, intermediate, or reproducible captures out of memory.
4. Update `sources` frontmatter on affected maintained pages.
5. Replace the affected parts of `wiki/project/current-state.md`, and move out
   what no longer steers the next session.
6. Update only affected maintained pages.
7. Add or supersede decision pages for meaningful choices. Preserve the reason,
   alternatives, applicability, observed outcome, and a useful revisit condition
   when available. Separate the original expectation from later evidence.
8. Update assumptions, risks, mitigations, and open questions.
9. Record validation evidence and residual gaps.
10. Update a relevant milestone or existing task record when work must resume
    in another session. Link decisions and evidence rather than copying them.
11. Append a compact factual entry to the chronology log.

Example:

```md
## [2026-07-28] update | Project memory refreshed

- updated: wiki/project/current-state.md
- added: wiki/decisions/2026-07-28-example.md
- evidence: focused tests and reviewed diff
```

Do not turn an unverified implementation claim into confirmed current state.
An observed correction or a failed approach may change future work even when
no implementation changed. Record the conditions and evidence in the relevant
decision, area, or procedure. Repetition alone does not confirm a claim, and
one successful use does not establish a universal rule. Flag unresolved
contradictions; do not silently select the newest statement as true.

If established project instructions authorize routine memory maintenance,
perform this update as part of finishing the work. If no durable understanding
changed, avoid a redundant page edit or log entry. Do not introduce a background
capture service or expand into other projects as part of Update.

When evidence was reviewed, finish affected pages and chronology before saving
their scoped [evidence checkpoints](context-and-evidence.md#evidence-checkpoints).
Do not clear candidates for pages that were merely retrieved. Connect purpose,
workflow, constraints, rejected alternatives, and observed outcomes where this
helps the next worker understand the project; preserve unknowns explicitly.

### Keep current state current

Current state is a replaced page, not an appended one. It is the mirror of the
chronology rule: logs never replace current state, and current state never
becomes a second log. Every session reads it, so its length is a recurring cost
paid by every future agent.

An item leaves when it stops changing what the next session does. That is a
lower bar than becoming false, and the difference is the whole reason this page
grows: most of what accumulates here stays true, and a rule keyed on truth
never reaches it. Ask what a cold session would do differently for having read
the line. When the answer is nothing, move it and leave at most a link:

| Item | Destination |
|---|---|
| finished work | the chronology entry that already records it |
| resumable work or a completed handoff | its existing task artifact or milestone |
| the reasoning behind a choice | a decision page |
| a checkpoint worth reconstructing | a milestone page |
| a standing fact that no longer steers work | an area page for its workstream, or the overview when it is project-wide |

Prune `sources` with the claims: the list is the evidence for what the page
says now, not a ledger of everything the page ever said. Delete an entry when
the claim it supported has left the page, and check that no remaining claim
still depends on it.

A growing `Completed` section, an entry that restates a log line, and a
`sources` list longer than the page's live claims are all the same signal. So
is one section swelling past the rest, which usually means a workstream has
outgrown its line on this page and wants
[an area page](page-types.md). The memory validator warns when current state is
long or has lost its sections, but it cannot tell which lines still steer the
work; that judgment is part of Update.

### Write from one owner when work runs in parallel

Update assumes one writer. When work is split across branches, worktrees,
sessions, or agents, the maintained tree gains integration points with several
writers, and the shared synthesis pages are exactly the files every writer
touches. Assign ownership before the parallel work starts, the same way a
project assigns one owner to a shared manifest, schema, or lockfile.

| Page | Owner |
|---|---|
| `index.md`, `wiki/project/current-state.md`, `wiki/questions/open-questions.md` | the integrating branch, updated once after merge |
| a task record or milestone | its assigned writer |
| a decision, risk, assumption, or area page | the branch that created it, or the branch named as its owner before the split |
| the chronology entry for a session | a log file that branch alone appends |

A page that already existed has no owner by creation, so name one before the
split. Two branches amending the same decision or area page conflict exactly as
two branches rewriting current state do, and ownership reaches that case only
when it is assigned rather than inferred.

A parallel writer records its work in the pages it owns, and reports that the
integration pages will need the post-merge Integrate. The integrator then writes
current state once, from the merged result, which is also the only point where
that page can be accurate.

These pages conflict on the same lines rather than in separate regions — a
rewritten summary, a single `updated:` field, a tail-appended list — so merge
tooling cannot resolve what ownership prevents. When the split makes a shared
page unavoidable, stop and agree who writes it before working, and use a
per-writer chronology unit from
[page types](page-types.md).

## Integrate

Use Integrate after parallel work merges, on the branch holding the merged
result. Update records what one writer did; Integrate records what is true once
several writers' work sits in one tree. The inputs differ, so the operation
differs: it reads the chronology that landed since current state was last
written, not the session that just ended.

Run it when a merge brings in work from writers that owned only their own
pages. The memory validator warns when per-writer chronology is newer than the
last shared-state or `integrate` watermark, but the warning may also appear on
the writer branch before merge. Confirm that the current branch holds the
merged result; otherwise report Integrate as pending instead of running it.

1. Read `wiki/project/current-state.md`, then every chronology entry dated
   after it.
2. Read the milestone, decision, risk, and area pages those entries created or
   changed. They are merged and already correct; do not rewrite them.
3. Decide what is true of the merged result. A claim that held on one branch
   may not survive beside another branch's work, and that contradiction is the
   thing only this step can see.
4. Replace the affected parts of current state, applying the eviction rule
   above. Do not append one summary per merged writer; that recreates the
   completed-history problem in a new shape.
5. Prune and extend `sources` so the list matches the claims the page now makes.
6. Resolve, add, or re-scope the open questions the merged work settled or
   raised.
7. Update `index.md` only when the merged work changed the reading path.
8. Append one chronology entry for the integration, naming the work it absorbed.
   Its heading uses the operation token `integrate`, as in
   `## [2026-08-14] integrate | Writer memory absorbed`. This append-only entry
   is the integration watermark when the merged work correctly leaves current
   state unchanged.
9. Run the memory validator and report its errors and warnings.

Do not run Integrate on a feature branch. Its output is exactly the single-owner
pages from the ownership table, so writing them anywhere but the integrating
branch recreates the conflict that ownership prevents.

When the Maker asks to wrap up, close out, or finish rather than naming an
operation, choose between Update and Integrate instead of asking: a writer
finishing its own work runs Update, and a branch holding merged work that no
shared page has absorbed runs Integrate. A session that did both runs Update
first.

## Lint

Check:

- missing or invalid frontmatter;
- duplicate page IDs;
- stale active pages;
- important claims without sources;
- orphan maintained pages;
- decisions not reflected in current state;
- assumptions without validation plans;
- risks without mitigation or rationale;
- resolved questions still presented as open;
- current state carrying lines that no longer steer the next session, or
  `sources` entries no longer supporting any claim on the page;
- per-writer chronology newer than the last shared-state or `integrate`
  watermark, which means post-merge Integrate may still be pending; confirm the
  writer logs have merged before treating it as outstanding;
- duplicate claims likely to drift;
- raw sources edited instead of appended;
- optional page families without a real project need;
- resumable task records whose state, evidence, or next action has drifted;
- changed or retracted evidence whose dependent claims still appear current;
- a date or `confirmed` label being used as a substitute for checking a
  volatile claim; age alone does not make a durable decision false;
- a missing, duplicated, or stale `projipsa:memory-pointer` block in the root
  instruction files, including a root `CLAUDE.md` that never points at the
  memory root;
- pages marked `confirmed` whose `sources` list is empty;
- broken relative links.

Report findings first. Fix them only when repair is authorized. Use
`scripts/validate_memory.py` for deterministic structural checks, then apply
judgment for freshness, provenance quality, and semantic contradictions. The
script also prints `warning:` lines for drift it can measure but not decide,
such as a current-state page that has grown past a readable briefing, or
chronology dated after that page was last written. A warning never fails
validation; treat it as a lint finding to report.

## Repair

Use Repair after Lint identifies contract drift in a project that has already
adopted Projipsa, or when the user explicitly asks to upgrade its memory rules.

1. Read the project's `docs/AGENTS.md` or equivalent profile before the plugin
   defaults. Preserve intentional local paths, roles, and conventions.
2. Inventory the exact findings and separate required repairs from optional
   normalization. A valid customized tree is not damage.
3. Preserve stable IDs, links, chronology, retained evidence, and unrelated
   user work.
4. Apply the smallest authorized fixes. Do not recreate the adoption decision
   or rerun Init.
5. Run the memory validator, inspect the diff, and append one repair or upgrade
   chronology entry only when files actually changed.

Read [repair and upgrade](repair-and-upgrade.md) for version-specific
preservation rules. Repair does not authorize binary cleanup. When the finding
is mainly size, repeated captures, or obsolete assets, route to the explicit
Compact workflow instead.

## Snapshot

Use Snapshot before a milestone, handoff, long pause, major transition, review,
launch, or restart.

Create or update a milestone page containing:

- scope;
- current state;
- completed work;
- explicitly incomplete or excluded work;
- validation and evidence reviewed;
- active assumptions and risks;
- open questions and important decisions;
- the exact next useful action.

Link an existing task artifact when it already holds resumable state. Link the
milestone from the index when it should remain discoverable and append the
project's chronology. Preserve existing delivery records without introducing
an execution lifecycle or inferring acceptance.
